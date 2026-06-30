# RelayStack A/B 测试最终报告（2026-06-29）

- 生成时间：2026-06-29T19:25:00+08:00
- 正式统计来源：
  - `reports/blind-old-20260629/raw-runs.jsonl`
  - `reports/blind-new-20260629/raw-runs.jsonl`
- 对比组：`no_handoff` vs `rs_handoff`
- 判定方式：两组使用同一 runner、同一 `test.sh` oracle。
- 覆盖率结论：旧题 10/10 条结果完整；新题 40/40 条结果完整。

## 核心结论

1. 旧题 `task-001..005` 两组均 5/5 通过。
   `rs_handoff` 总耗时减少 39.4%，总 tokens 减少 30.5%。

2. 新题 `task-006..025` 两组均 19/20 通过。
   两组都只在 `task-016` 失败；`rs_handoff` 总耗时减少 12.7%，
   但总 tokens 增加 5.8%。

3. 全量 25 题合并看，两组均 24/25 通过。
   `rs_handoff` 总耗时减少 19.3%，总 tokens 减少 3.3%。

4. 题源可追溯性需要分层看：
   旧题是 `verified_public`，逐题绑定公开 GitHub PR，许可证明确，
   更适合作为对外展示的说服力样本。
   新题是 `scenario_only`，属于项目自建工程场景题，适合做回归和覆盖面补强，
   但不能单独声称为第三方公开评测结果。

## 总览

| 题库 | provenance | Runner | 完成 | 通过率 | 总耗时 | 总 tokens | 失败任务 |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 旧题 `task-001..005` | `verified_public` | `no_handoff` | 5/5 | 100.0% | 1366.659s | 2,047,554 | - |
| 旧题 `task-001..005` | `verified_public` | `rs_handoff` | 5/5 | 100.0% | 828.520s | 1,422,758 | - |
| 新题 `task-006..025` | `scenario_only` | `no_handoff` | 20/20 | 95.0% | 4210.382s | 6,127,518 | `task-016` |
| 新题 `task-006..025` | `scenario_only` | `rs_handoff` | 20/20 | 95.0% | 3673.815s | 6,481,893 | `task-016` |
| 全量 `task-001..025` | mixed | `no_handoff` | 25/25 | 96.0% | 5577.041s | 8,175,072 | `task-016` |
| 全量 `task-001..025` | mixed | `rs_handoff` | 25/25 | 96.0% | 4502.335s | 7,904,651 | `task-016` |

## 题库来源与可追溯性

### 旧题：公开 PR 题

- 范围：`task-001..005`
- 状态：`verified_public`
- 来源类型：`github_pr`
- 许可证：MIT
- 可追溯性判断：
  - 有公开上游 PR 链接。
  - 有明确 repo、PR、license 字段。
  - 可追溯性强，适合作为对外说明中的主要证据。

### 新题：自建场景题

- 范围：`task-006..025`
- 状态：`scenario_only`
- 来源类型：`engineering_scenario`
- 来源：`local:tasks/task-XXX/instruction.md`
- 许可证：`Project-local fixture; no external upstream license claimed`
- 可追溯性判断：
  - 题目覆盖常见工程缺陷与维护场景，适合做内部回归和能力对比。
  - 未绑定具体上游 issue/PR，不应单独称为第三方公开题库。
  - 报告中必须继续保留 `scenario_only` 标注，避免误导。

### 第三方公开评测集方案

仓库已新增两套第三方公开评测集 manifest：

```text
suites/authoritative/swe-bench-lite.json
suites/authoritative/multi-swe-bench.json
```

SWE-bench Lite：

- 数据集：`princeton-nlp/SWE-bench_Lite`
- 主页：https://www.swebench.com/
- 数据集：https://huggingface.co/datasets/princeton-nlp/SWE-bench_Lite
- 仓库：https://github.com/SWE-bench/SWE-bench
- 论文：https://openreview.net/forum?id=VTF8yNQM66
- 许可证：MIT

Multi-SWE-bench：

- 数据集：`ByteDance-Seed/Multi-SWE-bench`
- 主页：https://multi-swe-bench.github.io/
- 仓库：https://github.com/multi-swe-bench/multi-swe-bench
- 论文：https://arxiv.org/abs/2504.02605
- 许可证：Apache License 2.0

SWE-bench Lite 当前状态是 `adopted_manifest_only`：
已经记录第三方评测集元数据和字段映射，但本次未运行官方 harness。

Multi-SWE-bench 已进一步完成 1 个 flash 样本的官方 harness A/B。
该结果只说明官方 harness 链路已跑通，不应包装成完整 benchmark 排名。

## 第三方公开题源盲测状态

已对 Multi-SWE-bench 跑通 1 个官方 flash 样本：

```text
reports/authoritative-ab-20260629.json
reports/authoritative-ab-20260629.zh-CN.md
```

样本：

- instance：`darkreader__darkreader-7241`
- 仓库：`darkreader/darkreader`
- issue：https://github.com/darkreader/darkreader/issues/7238
- PR：https://github.com/darkreader/darkreader/pull/7241
- base commit：`991883df4d5910851130e3dc0e21fcbce604ea7d`
- 许可证：MIT

结果：`official_evaluated`。

| 组别 | completed | resolved | unresolved | error |
| --- | ---: | ---: | ---: | ---: |
| `baseline` | 1 | 1 | 0 | 0 |
| `relaystack_handoff` | 1 | 1 | 0 | 0 |

patch JSONL 已生成并被官方 harness 使用：

```text
reports/multi-swe-one-20260629/baseline.jsonl
reports/multi-swe-one-20260629/relaystack_handoff.jsonl
```

官方报告：

```text
reports/multi-swe-one-20260629/baseline-output/final_report.json
reports/multi-swe-one-20260629/relaystack_handoff-output/final_report.json
```

过程与成本指标：

| 组别 | agent 耗时 | total tokens | output tokens | reasoning output | command 启动 | 协作启动 | patch bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | 460.699s | 1,353,559 | 9,759 | 3,763 | 36 | 3 | 1016 |
| `relaystack_handoff` | 754.863s | 1,416,911 | 10,606 | 4,136 | 35 | 4 | 548 |

官方 harness 耗时：

- `baseline`：1073.805s，包含首次 Docker 镜像构建。
- `relaystack_handoff`：3.945s，复用已构建镜像。

这组 harness 耗时不能直接比较 agent 效率；成本比较应优先看 agent
耗时、tokens、步骤数和 patch 大小。

协议审计：

- 当前 `baseline` 不是 clean baseline。原始事件流显示它加载了 `ponytail`，
  也启动了 2 个只读 explorer 子代理。
- `relaystack_handoff` 额外加载 `rs-handoff`、`rs-issue`、`typescript-write`，
  并执行过 `npm ci --ignore-scripts` 后跑本地 `jest` / `eslint`。
- 因此本次不能证明“用了 RelayStack 技能导致更慢”。更准确的解释是：
  handoff 组做了更多流程和验证工作。
- 若要测纯净技能收益，需要下一轮固定 clean baseline：禁用项目技能、禁用子代理，
  只给上游 problem statement；handoff 组只增加 handoff 输入，其余预算一致。

补充说明：

- 两组均 resolved，但仅代表 1 个样本。
- `baseline` patch 更宽，额外改动了另一处 `{2,}` 分隔逻辑。
- `relaystack_handoff` patch 更接近官方 fix，只改目标 delimiter regex。
- 首次运行曾因 Docker Hub 拉取 `node:18` token 超时失败；补拉基础镜像后
  官方 harness 已完成两组评估。

## 旧题逐题明细

| 任务 | no_handoff | rs_handoff | PR | license |
| --- | --- | --- | --- | --- |
| `task-001` | 通过 / 196.535s / 265,672 | 通过 / 201.751s / 347,607 | https://github.com/vitejs/vite/pull/22715 | MIT |
| `task-002` | 通过 / 316.916s / 536,804 | 通过 / 155.462s / 269,279 | https://github.com/vitejs/vite/pull/22714 | MIT |
| `task-003` | 通过 / 279.221s / 442,723 | 通过 / 147.829s / 267,536 | https://github.com/markedjs/marked/pull/3984 | MIT |
| `task-004` | 通过 / 340.163s / 493,451 | 通过 / 161.217s / 270,334 | https://github.com/remix-run/react-router/pull/11861 | MIT |
| `task-005` | 通过 / 233.824s / 308,904 | 通过 / 162.261s / 268,002 | https://github.com/markedjs/marked/pull/3967 | MIT |

## 新题逐题明细

| 任务 | no_handoff | rs_handoff | provenance | issue/PR | license |
| --- | --- | --- | --- | --- | --- |
| `task-006` | 通过 / 297.677s / 355,935 | 通过 / 146.956s / 311,596 | `scenario_only` | 无 | Project-local fixture |
| `task-007` | 通过 / 181.200s / 228,655 | 通过 / 189.785s / 310,356 | `scenario_only` | 无 | Project-local fixture |
| `task-008` | 通过 / 218.534s / 345,228 | 通过 / 188.166s / 308,664 | `scenario_only` | 无 | Project-local fixture |
| `task-009` | 通过 / 146.867s / 265,985 | 通过 / 147.052s / 307,165 | `scenario_only` | 无 | Project-local fixture |
| `task-010` | 通过 / 219.355s / 344,732 | 通过 / 169.158s / 283,258 | `scenario_only` | 无 | Project-local fixture |
| `task-011` | 通过 / 243.196s / 308,248 | 通过 / 235.167s / 432,948 | `scenario_only` | 无 | Project-local fixture |
| `task-012` | 通过 / 182.038s / 266,931 | 通过 / 195.312s / 350,829 | `scenario_only` | 无 | Project-local fixture |
| `task-013` | 通过 / 137.093s / 225,131 | 通过 / 177.009s / 347,517 | `scenario_only` | 无 | Project-local fixture |
| `task-014` | 通过 / 248.665s / 309,633 | 通过 / 214.396s / 389,178 | `scenario_only` | 无 | Project-local fixture |
| `task-015` | 通过 / 150.399s / 0 | 通过 / 154.776s / 0 | `scenario_only` | 无 | Project-local fixture |
| `task-016` | 失败 / 169.145s / 267,606 | 失败 / 269.709s / 599,759 | `scenario_only` | 无 | Project-local fixture |
| `task-017` | 通过 / 283.446s / 390,131 | 通过 / 129.696s / 230,210 | `scenario_only` | 无 | Project-local fixture |
| `task-018` | 通过 / 264.027s / 393,822 | 通过 / 191.695s / 309,232 | `scenario_only` | 无 | Project-local fixture |
| `task-019` | 通过 / 170.731s / 316,418 | 通过 / 134.602s / 266,872 | `scenario_only` | 无 | Project-local fixture |
| `task-020` | 通过 / 431.849s / 634,398 | 通过 / 296.919s / 441,532 | `scenario_only` | 无 | Project-local fixture |
| `task-021` | 通过 / 162.522s / 274,994 | 通过 / 160.796s / 309,774 | `scenario_only` | 无 | Project-local fixture |
| `task-022` | 通过 / 187.328s / 317,701 | 通过 / 176.930s / 386,702 | `scenario_only` | 无 | Project-local fixture |
| `task-023` | 通过 / 157.467s / 266,043 | 通过 / 138.273s / 268,386 | `scenario_only` | 无 | Project-local fixture |
| `task-024` | 通过 / 201.602s / 347,694 | 通过 / 148.807s / 270,988 | `scenario_only` | 无 | Project-local fixture |
| `task-025` | 通过 / 157.241s / 268,233 | 通过 / 208.611s / 356,927 | `scenario_only` | 无 | Project-local fixture |

## 完整报告字段

runner 已在结果中写入以下 provenance 字段：

- `suite_id`
- `suite_name`
- `provenance_status`
- `source_type`
- `source_url`
- `repo_url`
- `issue_url`
- `pr_url`
- `original_commit`
- `license`
- `license_url`
- `citation`
- `provenance`

字段定义来源：`tasks/provenance.schema.json`。

## 原始数据文件

- 旧题 blind 原始结果：`reports/blind-old-20260629/raw-runs.jsonl`
- 新题 blind 原始结果：`reports/blind-new-20260629/raw-runs.jsonl`
- 旧题 no_handoff report：`reports/no_handoff-real-20260629.jsonl`
- 旧题 rs_handoff report：`reports/rs_handoff-real-20260629.jsonl`
- 新题 no_handoff report：`reports/no_handoff-expanded-20260629.jsonl`
- 新题 rs_handoff report：`reports/rs_handoff-expanded-20260629.jsonl`
- 本地 25 题 suite：`suites/local-25.json`
- 第三方评测集方案：`suites/authoritative/swe-bench-lite.json`
- 第三方评测集方案：`suites/authoritative/multi-swe-bench.json`
- Multi-SWE-bench A/B 汇总：`reports/authoritative-ab-20260629.json`
- Multi-SWE-bench A/B 报告：`reports/authoritative-ab-20260629.zh-CN.md`
- Multi-SWE-bench dataset：`reports/multi-swe-one-20260629/dataset.jsonl`
- Multi-SWE-bench baseline patch JSONL：`reports/multi-swe-one-20260629/baseline.jsonl`
- Multi-SWE-bench handoff patch JSONL：`reports/multi-swe-one-20260629/relaystack_handoff.jsonl`
- Multi-SWE-bench 执行汇总：`reports/multi-swe-one-20260629/summary.json`
- Multi-SWE-bench baseline agent 事件流：`reports/multi-swe-one-20260629/baseline-agent-output.jsonl`
- Multi-SWE-bench handoff agent 事件流：`reports/multi-swe-one-20260629/relaystack_handoff-agent-output.jsonl`

## 注意事项

- `task-015` 两组 tokens 均为 0，表示该次 Codex JSON 输出没有可用 token 统计；
  通过率和耗时不受影响，但 token 汇总会低估这道题。
- `task-016` 两组均失败，说明它更可能暴露题目难度、oracle 要求或提示设计问题，
  不能作为某一组单独退化的证据。
- Multi-SWE-bench 当前只跑 1 个样本。下一步应扩到 3-5 个 flash 样本，
  并固定样本选择规则、镜像预拉取步骤和重跑策略。
