---
doc_type: dev-guide
slug: benchmark-evaluation
component: relaystack-benchmark
status: current
summary: RelayStack 最小 A/B benchmark 的题源、测试标准、评分标准和运行流程。
tags: [benchmark, handoff, evaluation]
last_reviewed: 2026-06-24
---

# RelayStack 最小 A/B Benchmark 说明

本文档记录当前最小实战 benchmark 的题目来源、测试标准、评分标准和完整执行流程。

目标不是先接入完整评测平台，而是用接近 Terminal-Bench 的轻量结构，先确认
RelayStack handoff 是否能在真实小任务上和无 handoff 基线拉开差异。

当前目录结构：

```text
tasks/
  task-001/
    initial-repo/
    instruction.md
    handoff.md
    test.sh
runners/
  no_handoff.py
  rs_handoff.py
reports/
  *.jsonl
```


## 1. 题目来源

第一版题目已经从私有项目场景迁移为公开 GitHub 来源，避免把私有仓库上下文发送给外部模型服务。

题目选择标准：

1. 来源是公开 GitHub PR 或 issue，方便追溯真实需求。
2. 场景接近真实维护任务，而不是纯算法题。
3. 可以裁剪成很小的 fixture，不依赖完整仓库安装。
4. `test.sh` 能独立判定行为，不靠人工主观判断。
5. 任务难度足够小，适合先跑 5-10 个样本观察信号。

当前 5 个任务：

| 任务 | 公开来源 | 场景 | 核心验收点 |
| --- | --- | --- | --- |
| `task-001` | `https://github.com/vitejs/vite/pull/22715` | Vite 环境状态缓存误把 falsy 值当未缓存 | `false`、`0` 这类 falsy 状态只初始化一次，并保持环境隔离 |
| `task-002` | `https://github.com/vitejs/vite/pull/22714` | Vite public middleware 遇到 malformed URI 会抛错 | 非法 URI 不抛异常，转交 `next()`；正常 public 文件仍能命中 |
| `task-003` | `https://github.com/markedjs/marked/pull/3984` | Marked 空列表项解析缺失 | `- `、`* `、`1. ` 能生成空 `li`，后续段落不被吞掉 |
| `task-004` | `https://github.com/remix-run/react-router/pull/11861` | React Router Vite optimizeDeps 处理 optional dependency | 缺失的 optional dependency 被跳过，存在的 optional dependency 仍加入优化列表 |
| `task-005` | `https://github.com/markedjs/marked/pull/3967` | Marked CLI 同时支持文件参数和 stdin | 有文件参数时优先读文件；无文件参数时读 stdin；跳过 `node` 和脚本路径 |

每个任务的真实代码面都被裁剪到 `initial-repo/`：

```text
task-001/initial-repo/packages/vite/src/node/server/environmentState.js
task-002/initial-repo/packages/vite/src/node/server/middlewares/servePublicMiddleware.js
task-003/initial-repo/src/listParser.js
task-004/initial-repo/packages/router-dev/vite/optimizeDeps.js
task-005/initial-repo/bin/marked.js
```


## 2. 测试标准

每个任务包含三类输入：

1. `instruction.md`
   - 给 agent 的需求说明。
   - 描述用户目标、允许修改范围和验收方式。

2. `handoff.md`
   - 给 RelayStack 组使用的交接信息。
   - 只包含当前任务相关的已知入口、行为线索和测试线索。

3. `test.sh`
   - 最终自动判定脚本。
   - runner 会在临时工作区执行它。

Runner 的判定方式：

1. 复制 `initial-repo/` 到临时工作区。
2. 生成 prompt，并把工作区路径放入 `RS_BENCH_WORKDIR`。
3. 调用 agent 在临时工作区修改代码。
4. 在同一个临时工作区执行 `bash test.sh`。
5. `test.sh` 退出码为 `0` 时，记为 `passed=true`。

关键边界：

- `agent_returncode` 和 `test_returncode` 分开记录。
- 通过测试只看 `test_returncode == 0`。
- `--keep-workdir` 会保留每个任务的临时目录，方便复盘 agent 的实际改动。
- 当前 fixture 不跑全仓依赖安装、全仓 lint 或全仓 TypeScript 检查。
- 当前验证目标是小切片行为正确，不代表原始上游项目完整回归通过。


## 3. A/B 组定义

当前只比较两组：

```text
无 handoff 组
  instruction.md
    ↓
  agent
    ↓
  test.sh

RelayStack handoff 组
  handoff.md + instruction.md
    ↓
  agent
    ↓
  test.sh
```

### 3.1 no_handoff

入口：`runners/no_handoff.py`

Prompt 只包含：

- `instruction.md`
- benchmark metrics 写入要求

这组模拟 agent 从普通需求说明开始自行探索。

### 3.2 rs_handoff

入口：`runners/rs_handoff.py`

Prompt 包含：

- RelayStack 生成的 handoff snapshot
- `handoff.md`
- `instruction.md`
- benchmark metrics 写入要求

这组模拟 agent 接手时已经拿到结构化交接信息。


## 4. 指标与打分标准

第一版只保留 5 类指标，避免评测系统过早变重。

### 4.1 原始指标

1. 是否通过测试
   - 字段：`passed`
   - 判定：`test_returncode == 0`
   - 这是硬门槛。

2. 总耗时
   - 字段：`elapsed_seconds`
   - 同时看单任务耗时和整组总耗时。

3. token / 调用成本
   - 字段：`total_tokens`、`cost_usd`
   - 如果 provider 没有返回成本，`cost_usd` 可以为 `null`。

4. 接手后执行步数
   - 字段：`steps_after_handoff`
   - 由 agent 写入 `RS_BENCH_METRICS`。
   - 未来用于衡量 handoff 是否让执行更直接。

5. 是否重复探索明显已知信息
   - 字段：`repeated_known_info`
   - 由 agent 写入 `RS_BENCH_METRICS`。
   - 如果 handoff 已明确给出入口和结论，但 agent 又重新扫描同一信息，记为 `true`。

### 4.2 推荐打分口径

单任务建议用 100 分制：

```text
正确性              50 分
耗时效率            20 分
token / 成本效率    15 分
handoff 纪律        10 分
改动质量             5 分
```

具体规则：

1. 正确性 50 分
   - `passed=true` 得 50 分。
   - `passed=false` 得 0 分。
   - 如果测试没通过，单任务总分不应高于 50 分。

2. 耗时效率 20 分
   - 同一任务内做 A/B 相对比较。
   - 更快的一组得满分。
   - 较慢的一组按 `更快耗时 / 本组耗时` 折算。

3. token / 成本效率 15 分
   - 优先使用 `total_tokens`。
   - 如果 `cost_usd` 有值，可同时看成本。
   - 更低的一组得满分，另一组按比例折算。

4. handoff 纪律 10 分
   - `steps_after_handoff` 越低越好。
   - `repeated_known_info=false` 是基本要求。
   - 当前如果字段为 `null`，这项不参与正式结论。

5. 改动质量 5 分
   - 改动聚焦于任务文件。
   - 不修改测试脚本来绕过测试。
   - 不引入无关依赖、无关重构或大范围格式化。

### 4.3 批量结论口径

批量看结果时按这个顺序判断：

1. 先看两组通过率。
   - 如果一组未通过，正确性优先于耗时和 token。

2. 通过率相同时，看总耗时和总 token。
   - 这是当前第一版最稳定的信号。

3. 再看 `steps_after_handoff` 和 `repeated_known_info`。
   - 这两个字段需要 agent 主动写 metrics。
   - 已完成的历史 run 如果没有这些字段，不做事后补填。


## 5. 完整测试流程

### 5.1 准备任务

1. 从公开 GitHub PR 或 issue 选择真实维护场景。
2. 裁剪最小 `initial-repo/`。
3. 编写 `instruction.md`，只描述需求和允许范围。
4. 编写 `handoff.md`，只放 RelayStack 接手时应复用的信息。
5. 编写 `test.sh`，用退出码表达成功或失败。

### 5.2 本地轻量校验

推荐校验：

```bash
python3 -m py_compile runners/_runner.py runners/no_handoff.py runners/rs_handoff.py
bash -n tasks/task-001/test.sh
bash -n tasks/task-002/test.sh
bash -n tasks/task-003/test.sh
bash -n tasks/task-004/test.sh
bash -n tasks/task-005/test.sh
git diff --check
```

如果要确认任务不再包含私有上下文，可补充：

```bash
rg -n "comate|Comate|icode|隐藏空间|迁移空间|devops/icode|comatemobile|useCurrentUserName|knowledgebaseUuid" tasks
```

期望结果是没有命中。

### 5.3 跑 no_handoff 组

示例命令：

```bash
python3 runners/no_handoff.py \
  tasks/task-001 \
  tasks/task-002 \
  tasks/task-003 \
  tasks/task-004 \
  tasks/task-005 \
  --keep-workdir \
  --report reports/no_handoff-real-20260624.jsonl \
  --agent-cmd '/Applications/Codex.app/Contents/Resources/codex exec --json --ephemeral --skip-git-repo-check --sandbox workspace-write -C "$RS_BENCH_WORKDIR" - < "$RS_BENCH_PROMPT"'
```

### 5.4 跑 rs_handoff 组

示例命令：

```bash
python3 runners/rs_handoff.py \
  tasks/task-001 \
  tasks/task-002 \
  tasks/task-003 \
  tasks/task-004 \
  tasks/task-005 \
  --keep-workdir \
  --report reports/rs_handoff-real-20260624.jsonl \
  --agent-cmd '/Applications/Codex.app/Contents/Resources/codex exec --json --ephemeral --skip-git-repo-check --sandbox workspace-write -C "$RS_BENCH_WORKDIR" - < "$RS_BENCH_PROMPT"'
```

### 5.5 读取报告

每个报告是 JSONL：

- 每行对应一个任务。
- 任务字段包括耗时、退出码、测试结果、token 和临时工作区。
- 后续可以用脚本聚合，也可以先人工读 5 条结果。

常用字段：

```text
task
passed
elapsed_seconds
agent_returncode
test_returncode
total_tokens
cost_usd
steps_after_handoff
repeated_known_info
workdir
```


## 6. 2026-06-24 实跑结果

本轮使用外部 Codex 执行同一套 5 个公开 synthetic task。

### 6.1 汇总

| 组别 | 通过率 | 总耗时 | 总 token | 成本 |
| --- | ---: | ---: | ---: | ---: |
| no_handoff | 5/5 | 466.965s | 1,920,236 | `null` |
| rs_handoff | 5/5 | 360.556s | 1,498,660 | `null` |

差异：

- rs_handoff 同样 5/5 通过。
- rs_handoff 少用 106.409s，约快 22.8%。
- rs_handoff 少用 421,576 tokens，约少 22.0%。

### 6.2 单任务结果

| 任务 | no_handoff 耗时 | no_handoff token | rs_handoff 耗时 | rs_handoff token |
| --- | ---: | ---: | ---: | ---: |
| `task-001` | 79.847s | 383,173 | 63.528s | 276,203 |
| `task-002` | 84.214s | 288,050 | 77.581s | 289,888 |
| `task-003` | 101.619s | 346,883 | 70.487s | 280,089 |
| `task-004` | 118.501s | 553,913 | 71.322s | 361,406 |
| `task-005` | 82.784s | 348,217 | 77.638s | 291,074 |

### 6.3 本轮不能下的结论

本轮 `steps_after_handoff` 和 `repeated_known_info` 是 `null`。

原因是这次真实 run 完成后，runner 才补充了要求 agent 写入 `RS_BENCH_METRICS` 的 prompt。
因此这两个字段不能事后补填，也不参与本轮正式判断。

当前可确认的结论只有：

1. 两组正确性都通过。
2. RelayStack handoff 组在这 5 个任务上耗时和 token 更低。
3. 样本数仍然太小，只能作为继续扩样的初步信号。


## 7. 已知限制

1. 当前任务是公开来源的 synthetic fixture。
   - 来源真实，但不是完整上游仓库。

2. `test.sh` 只覆盖任务目标行为。
   - 它不等价于上游项目完整测试集。

3. token 和成本依赖 provider 输出。
   - provider 不返回成本时，`cost_usd` 为空。

4. `steps_after_handoff` 和 `repeated_known_info` 依赖 agent 自报。
   - 后续如果要更严谨，需要结合 transcript 或工具调用日志做二次判定。

5. 样本数只有 5 个。
   - 足够判断 runner 是否能跑通。
   - 不足以支撑产品级效果宣称。


## 8. 后续建议

下一步不急着接 Inspect AI 或 Braintrust。

更合理的推进顺序：

1. 继续扩到 10-20 个公开真实来源任务。
2. 每个任务保留来源链接、fixture 裁剪说明和测试覆盖说明。
3. 对同一批任务重复跑 2-3 次，观察结果是否稳定。
4. 把 `steps_after_handoff` 和 `repeated_known_info` 补齐到报告中。
5. 当通过率、耗时、token、重复探索四类信号都稳定后，再接正式评测平台。


## 9. 相关文件

- 任务目录：`tasks/task-001` 到 `tasks/task-005`
- 无 handoff runner：`runners/no_handoff.py`
- RelayStack handoff runner：`runners/rs_handoff.py`
- runner 公共逻辑：`runners/_runner.py`
- 本轮无 handoff 报告：`reports/no_handoff-real-20260624.jsonl`
- 本轮 RelayStack handoff 报告：`reports/rs_handoff-real-20260624.jsonl`


## 10. 2026-06-24 扩展题库

本次把题库从 5 道扩展到 25 道，新增 `task-006` 到 `task-025`。

新增题不复制完整上游仓库，只裁剪成可离线验证的最小 fixture。来源分两类：

1. 公开 GitHub / 开源维护问题的等价切片。
2. 企业真实研发中高频出现的维护场景。

难度分布：

```text
easy    5
medium 10
hard    5
```

新增 20 个任务：

| 任务 | 来源/场景 | 难度 | 核心验收点 |
| --- | --- | --- | --- |
| `task-006` | dotenv / 企业配置解析 | easy | value 保留后续 `=`；quoted `#` 不被当注释；空值保留 |
| `task-007` | Zip Slip / 归档解压安全 | medium | `../`、绝对路径、sibling prefix fail fast |
| `task-008` | HTTP client Retry-After | easy | 同时支持纯秒数和 HTTP-date；非法值返回 0 |
| `task-009` | API client promise cache | medium | 并发共享 in-flight；rejected promise 不永久缓存 |
| `task-010` | 发布/包管理依赖排序 | hard | 拓扑排序依赖优先；循环依赖报出路径 |
| `task-011` | Markdown front matter | easy | 只在文件首行 `---` 时解析 front matter |
| `task-012` | CSV 用户导入 | medium | UTF-8 BOM、邮箱大小写去重、空邮箱跳过 |
| `task-013` | Feature flag 灰度开关 | easy | 显式 `False`/`0` 不被 default 覆盖；env 优先 |
| `task-014` | Feed cursor pagination | hard | cursor 基于 `(created_at, id)`，插入新数据后不重复 |
| `task-015` | API gateway token bucket | medium | 小数秒补 token；时钟回拨不补负 token |
| `task-016` | 后台 SQL filter builder | medium | falsy 条件保留；参数化；未知字段拒绝 |
| `task-017` | 日志脱敏 | medium | header 大小写不敏感；URL query secret 脱敏 |
| `task-018` | Router path matching | easy | 忽略 query/hash；非 root trailing slash 归一 |
| `task-019` | DB migration planner | medium | 数字版本排序；重复版本和非法文件名报错 |
| `task-020` | CI JUnit XML 汇总 | medium | 支持嵌套 testsuites 和 testcase 子节点统计 |
| `task-021` | Business day scheduler | medium | 跳过周末和节假日；`days=0` 原样返回 |
| `task-022` | 配置 deep merge | medium | dict 递归合并；list 替换；不修改输入对象 |
| `task-023` | Semver caret range | hard | 正确处理 `^1.x`、`^0.2.x`、`^0.0.x` 上界 |
| `task-024` | NDJSON streaming parser | hard | 保留跨 chunk 半行；末尾无换行仍解析 |
| `task-025` | 部署 reconciler | hard | 按 service name diff；重排不产生假更新 |

这些题故意覆盖不同能力：

- 配置/解析：`task-006`、`task-011`、`task-012`、`task-022`
- 安全/边界：`task-007`、`task-016`、`task-017`
- HTTP/API：`task-008`、`task-009`
- 调度/缓存/分页：`task-014`、`task-015`、`task-021`
- 工程工具链：`task-010`、`task-019`、`task-020`、`task-023`
- 流式/部署：`task-024`、`task-025`

新增题的本地轻量检查：

```bash
for task in tasks/task-{006..025}; do bash -n "$task/test.sh"; done
git diff --check
```

完整 A/B 扩样运行仍沿用现有 runner：

```bash
python3 runners/no_handoff.py \
  tasks/task-{006..025} \
  --keep-workdir \
  --report reports/no_handoff-expanded-20260624.jsonl \
  --blind-dir reports/blind-expanded-20260624 \
  --seed expanded-20260624 \
  --agent-cmd '/Applications/Codex.app/Contents/Resources/codex exec --json --ephemeral --skip-git-repo-check --sandbox workspace-write -C "$RS_BENCH_WORKDIR" - < "$RS_BENCH_PROMPT"'

python3 runners/rs_handoff.py \
  tasks/task-{006..025} \
  --keep-workdir \
  --report reports/rs_handoff-expanded-20260624.jsonl \
  --blind-dir reports/blind-expanded-20260624 \
  --seed expanded-20260624 \
  --agent-cmd '/Applications/Codex.app/Contents/Resources/codex exec --json --ephemeral --skip-git-repo-check --sandbox workspace-write -C "$RS_BENCH_WORKDIR" - < "$RS_BENCH_PROMPT"'
```


## 11. A/B 盲评扩展

扩样后的 A/B 不直接把 runner 名称暴露给 reviewer。

```text
task-006..025
  │
  ├── no_handoff runner      -> 原始 report
  ├── rs_handoff runner      -> 原始 report + snapshot
  │
  ├── blind packet builder   -> candidate_x / candidate_y
  │
  ├── 3 个 blind reviewer
  │      ├── efficiency_reviewer
  │      ├── quality_token_reviewer
  │      └── debug_handoff_reviewer
  │
  └── aggregator             -> 解盲、汇总、输出结论
```

三类 reviewer：

1. `efficiency_reviewer`
   - 看耗时、工具步骤、文件探索摘要。
   - 重点判断是否少走弯路、是否重复扫描已知入口。

2. `quality_token_reviewer`
   - 看 `passed`、diff 摘要、测试输出摘要、token/cost。
   - 重点判断完成度、最小改动、token 是否浪费。

3. `debug_handoff_reviewer`
   - 看匿名接手上下文包和 transcript 摘要。
   - 重点判断前一个 agent 的 handoff 是否足够让后一个 agent 继续。

单任务评分仍用 100 分制，但盲评时 reviewer 只看 `candidate_id`：

```text
正确性              45 分
改动质量            15 分
耗时效率            15 分
token / 成本效率    10 分
探索纪律            10 分
handoff/debug 完整度 5 分
```

推荐报告文件：

```text
reports/blind/raw-runs.jsonl       # 原始 runner 结果，含真实组别
reports/blind/packets.jsonl        # 效率/质量 reviewer 脱敏输入包
reports/blind/debug-packets.jsonl  # debug/handoff reviewer 输入包
reports/blind/reviews.jsonl        # 3 个 reviewer 输出
reports/blind/unblind-map.json     # candidate_id -> runner
reports/blind/final.md             # 解盲后的结论
reports/blind/final.generated.md   # 汇总脚本生成的结论
reports/blind/runs/<run_id>/       # prompt、agent output、test output、diff
```

当前 runner 传入 `--blind-dir` 后会额外采集：

- `raw-runs.jsonl`
- `packets.jsonl`
- `debug-packets.jsonl`
- `unblind-map.json`
- `runs/<run_id>/agent-output.txt`
- `runs/<run_id>/test-output.txt`
- `runs/<run_id>/diff-summary.txt`
- `runs/<run_id>/diff.patch`
- `runs/<run_id>/prompt.md`
- `runs/<run_id>/snapshot.md`，仅 RelayStack handoff 组存在

`packets.jsonl` 不包含 `runner`、`workdir`、`snapshot` 或 `snapshot_generated`，
用于效率和质量 reviewer。`debug-packets.jsonl` 额外包含匿名接手上下文摘要，
只给 debug/handoff reviewer 使用。

仍然缺的严格审计字段：

- 结构化 tool step 明细
- 打开文件列表
- transcript 中重复探索的自动判定

这些字段需要解析具体 agent JSON 输出。当前先保留原始 `agent-output.txt`，
由 reviewer 或后续 packet builder 二次提取，避免 runner 过早绑定某个 agent
输出格式。

盲评完成后，用汇总脚本生成解盲结论：

```bash
python3 scripts/summarize_blind_benchmark.py \
  reports/blind-expanded-20260624 \
  --output reports/blind-expanded-20260624/final.generated.md
```
