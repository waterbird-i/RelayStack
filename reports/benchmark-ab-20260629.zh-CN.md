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

4. 权威性需要分层看：
   旧题是 `verified_public`，逐题绑定公开 GitHub PR，许可证明确，
   更适合作为对外展示的说服力样本。
   新题是 `scenario_only`，属于项目自建工程场景题，适合做回归和覆盖面补强，
   但不能单独声称为第三方权威评测。

## 总览

| 题库 | provenance | Runner | 完成 | 通过率 | 总耗时 | 总 tokens | 失败任务 |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 旧题 `task-001..005` | `verified_public` | `no_handoff` | 5/5 | 100.0% | 1366.659s | 2,047,554 | - |
| 旧题 `task-001..005` | `verified_public` | `rs_handoff` | 5/5 | 100.0% | 828.520s | 1,422,758 | - |
| 新题 `task-006..025` | `scenario_only` | `no_handoff` | 20/20 | 95.0% | 4210.382s | 6,127,518 | `task-016` |
| 新题 `task-006..025` | `scenario_only` | `rs_handoff` | 20/20 | 95.0% | 3673.815s | 6,481,893 | `task-016` |
| 全量 `task-001..025` | mixed | `no_handoff` | 25/25 | 96.0% | 5577.041s | 8,175,072 | `task-016` |
| 全量 `task-001..025` | mixed | `rs_handoff` | 25/25 | 96.0% | 4502.335s | 7,904,651 | `task-016` |

## 题库来源与权威性

### 旧题：公开 PR 题

- 范围：`task-001..005`
- 状态：`verified_public`
- 来源类型：`github_pr`
- 许可证：MIT
- 权威性判断：
  - 有公开上游 PR 链接。
  - 有明确 repo、PR、license 字段。
  - 可追溯性强，适合作为对外说明中的主要证据。

### 新题：自建场景题

- 范围：`task-006..025`
- 状态：`scenario_only`
- 来源类型：`engineering_scenario`
- 来源：`local:tasks/task-XXX/instruction.md`
- 许可证：`Project-local fixture; no external upstream license claimed`
- 权威性判断：
  - 题目覆盖常见工程缺陷与维护场景，适合做内部回归和能力对比。
  - 未绑定具体上游 issue/PR，不应单独称为第三方权威题库。
  - 报告中必须继续保留 `scenario_only` 标注，避免误导。

### 第三方公开评测集方案

仓库已新增 `suites/authoritative/swe-bench-lite.json` 作为可采用方案：

- 数据集：`princeton-nlp/SWE-bench_Lite`
- 主页：https://www.swebench.com/
- 数据集：https://huggingface.co/datasets/princeton-nlp/SWE-bench_Lite
- 仓库：https://github.com/SWE-bench/SWE-bench
- 论文：https://openreview.net/forum?id=VTF8yNQM66
- 许可证：MIT

当前状态是 `adopted_manifest_only`：
已经记录第三方评测集元数据和字段映射，但本次 A/B 没有跑 SWE-bench
官方 harness。因此本报告不声称取得 SWE-bench 分数。

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
- 第三方评测集方案：`suites/authoritative/swe-bench-lite.json`

## 注意事项

- `task-015` 两组 tokens 均为 0，表示该次 Codex JSON 输出没有可用 token 统计；
  通过率和耗时不受影响，但 token 汇总会低估这道题。
- `task-016` 两组均失败，说明它更可能暴露题目难度、oracle 要求或提示设计问题，
  不能作为某一组单独退化的证据。
- 若需要更强对外说服力，下一步应接入 SWE-bench Lite 官方 harness，
  生成 upstream-compatible predictions 后再报告 SWE-bench 分数。
