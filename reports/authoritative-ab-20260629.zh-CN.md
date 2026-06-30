# Multi-SWE-bench A/B 盲测报告（2026-06-29）

- 第三方公开题源：Multi-SWE-bench
- 数据集切片：`ByteDance-Seed/Multi-SWE-bench-flash`
- suite manifest：`suites/authoritative/multi-swe-bench.json`
- 本地 25 题分类：`suites/local-25.json`
- 本次状态：**已产生官方 harness A/B 结果**

## 结论

此前“缺 upstream-compatible patch JSONL”的结论已经过期。

本次已为同一个 Multi-SWE-bench 实例生成两组预测 patch JSONL，并使用
Multi-SWE-bench 官方 harness 完成评估：

```text
baseline              1/1 resolved
relaystack_handoff    1/1 resolved
```

这 1 个样本不能代表完整 Multi-SWE-bench 分数，但它已经证明：

1. 本地 25 题与第三方公开题源已分离。
2. patch JSONL 生成链路已跑通。
3. RelayStack handoff 协议可以接到官方 issue-resolving harness 上。

## 样本来源

- instance：`darkreader__darkreader-7241`
- 语言：TypeScript
- 上游仓库：https://github.com/darkreader/darkreader
- 原始 issue：https://github.com/darkreader/darkreader/issues/7238
- 原始 PR：https://github.com/darkreader/darkreader/pull/7241
- base commit：`991883df4d5910851130e3dc0e21fcbce604ea7d`
- 题目：`Fix: parser should ignore Base64 padding within CSS`
- 上游许可证：MIT

题目来自 Multi-SWE-bench flash 数据集，oracle 使用官方 harness 注入的
`test_patch` 与 `npm run test:ci` 判定，不使用本地自建 oracle。

## A/B 结果

| 组别 | patch JSONL | completed | resolved | unresolved | error |
| --- | --- | ---: | ---: | ---: | ---: |
| `baseline` | `reports/multi-swe-one-20260629/baseline.jsonl` | 1 | 1 | 0 | 0 |
| `relaystack_handoff` | `reports/multi-swe-one-20260629/relaystack_handoff.jsonl` | 1 | 1 | 0 | 0 |

官方报告文件：

```text
reports/multi-swe-one-20260629/baseline-output/final_report.json
reports/multi-swe-one-20260629/relaystack_handoff-output/final_report.json
```

两组逐实例报告均显示新增回归测试从 `FAIL` 变为 `PASS`：

```text
tests/generators/utils/parse.tests.ts:Base64 in CSS
run=NONE, test=FAIL, fix=PASS
```

## 生成链路

本次链路分为两层：

```text
官方数据集实例
  → baseline agent 生成 fix_patch
  → reports/.../baseline.jsonl
  → 官方 harness 判定

官方数据集实例
  → RelayStack handoff
  → continuation agent 生成 fix_patch
  → reports/.../relaystack_handoff.jsonl
  → 官方 harness 判定
```

生成摘要：

- `baseline`：agent returncode 0，耗时 `460.699s`，patch `1016` bytes
- `relaystack_handoff`：agent returncode 0，耗时 `754.863s`，patch `548` bytes

## 过程与成本指标

agent 侧指标来自 `codex exec --json` 的 `turn.completed.usage` 和事件流。

| 组别 | agent 耗时 | total tokens | input | cached input | output | reasoning output | 估算非缓存 input | command 启动 | 子代理/协作启动 | file changes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | 460.699s | 1,353,559 | 1,343,800 | 1,137,792 | 9,759 | 3,763 | 206,008 | 36 | 3 | 2 |
| `relaystack_handoff` | 754.863s | 1,416,911 | 1,406,305 | 1,195,648 | 10,606 | 4,136 | 210,657 | 35 | 4 | 1 |

对比：

- `relaystack_handoff` agent 多耗时 `294.164s`。
- `relaystack_handoff` 多用 `63,352` total tokens。
- `relaystack_handoff` patch 少 `468` bytes。
- `baseline` patch 更宽，`relaystack_handoff` patch 更贴近官方 fix。

## 协议审计

这次不能解释为“用了 RelayStack 技能所以更慢”。

从原始 agent 事件流看，`baseline` 不是 clean baseline：

- `baseline` 明确加载了 `ponytail` skill。
- `baseline` 也启动了 2 个只读 explorer 子代理。
- `baseline` 因 `npx` / 本地依赖问题做过失败验证和替代验证。

`relaystack_handoff` 额外做了更多流程工作：

- 读取 `rs-handoff`。
- 加载 `rs-issue`、`ponytail`、`typescript-write`。
- 启动 2 个只读 explorer 子代理。
- 为了跑锁定版本检查，执行过 `npm ci --ignore-scripts`。
- 最终跑通本地 `jest`、`eslint`、`git diff --check`。

所以本次耗时增加更像是**流程和验证开销**，不是 handoff 能力本身的纯效应。
如果要测“本技能是否更快”，下一轮需要固定 clean baseline：

```text
baseline: 禁用项目技能、禁用子代理、只给上游 problem statement
handoff: 只增加 RelayStack handoff 输入，其余验证预算与工具权限一致
```

官方 harness 耗时：

| 组别 | harness 开始 | harness 结束 | harness 耗时 | 说明 |
| --- | --- | --- | ---: | --- |
| `baseline` | 20:57:03.208 | 21:14:57.013 | 1073.805s | 包含首次 Docker 镜像构建 |
| `relaystack_handoff` | 21:15:59.312 | 21:16:03.257 | 3.945s | 复用已构建镜像 |

因此本次不能用官方 harness 耗时比较两组开发效率；它主要证明 oracle
完成与否。开发成本应看 agent 耗时、tokens、步骤和 patch 大小。

## 重要说明

- `baseline` 也 resolved，但 patch 比官方修复更宽，额外把 `{2,}` 改为 `{3,}`。
- `relaystack_handoff` patch 更接近官方 fix，只锚定 `indexSitesFixesConfig`
  的 delimiter regex。
- 这次只跑 1 个样本，结果只说明官方 harness 链路已跑通，不应包装成完整 benchmark 排名。
- `multi_swe_bench` 和 `datasets` 依赖安装在 `/private/tmp/multi-swe-bench-deps`，
  通过 `PYTHONPATH` 运行；不是全局 Python 环境安装。
- 首次运行曾因 Docker Hub 拉取 `node:18` token 超时失败；手动补拉
  `node:18` 后，官方 harness 已成功完成两组评估。

## 原始产物

- dataset：`reports/multi-swe-one-20260629/dataset.jsonl`
- baseline patch：`reports/multi-swe-one-20260629/baseline.patch`
- handoff patch：`reports/multi-swe-one-20260629/relaystack_handoff.patch`
- baseline JSONL：`reports/multi-swe-one-20260629/baseline.jsonl`
- handoff JSONL：`reports/multi-swe-one-20260629/relaystack_handoff.jsonl`
- baseline agent 事件流：`reports/multi-swe-one-20260629/baseline-agent-output.jsonl`
- handoff agent 事件流：`reports/multi-swe-one-20260629/relaystack_handoff-agent-output.jsonl`
- 执行汇总：`reports/multi-swe-one-20260629/summary.json`
- 机器可读汇总：`reports/authoritative-ab-20260629.json`

## 下一步

下一轮应从 1 个样本扩到 3-5 个 Multi-SWE-bench flash 样本，并固定随机种子、
实例选择规则、镜像预拉取步骤和重跑策略。
