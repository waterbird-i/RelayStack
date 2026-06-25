# 扩展版 Terminal-Bench A/B 报告

生成时间：2026-06-25

![扩展评测结果表格](assets/benchmark-results-table.png)

## 范围

- 新增 20 道 benchmark 任务：`task-006` 到 `task-025`。
- 难度分布：5 道 easy、10 道 medium、5 道 hard。
- 场景覆盖：dotenv 解析、Zip Slip 防护、Retry-After 解析、promise cache 恢复、依赖排序、front matter 解析、CSV 导入清洗、feature flag 优先级、cursor pagination、token bucket、SQL filter、日志脱敏、路由匹配、migration 排序、JUnit 汇总、business day、deep merge、semver caret range、NDJSON streaming、部署 reconciler。
- A/B 变量：
  - `no_handoff`：完全 prompt 驱动。
  - `rs_handoff`：RelayStack 工作流，先生成 rs-handoff snapshot/context packet，再继续接手实现。

## 原始 A/B 结果

| Runner | 运行数 | 通过数 | 通过率 | 总耗时 | 平均耗时 | 总 Token | 平均 Token | 平均步骤 | 重复已知信息 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `no_handoff` | 20 | 18 | 90.0% | 2367.293 | 118.365 | 9,391,563 | 469,578.2 | 7.0 | 4 |
| `rs_handoff` | 20 | 19 | 95.0% | 1791.844 | 89.592 | 7,209,958 | 360,497.9 | 6.6 | 0 |

`rs_handoff` 在原始运行中领先：

- 完成度：多通过 1 道题。
- 耗时：总耗时少 575.449 秒。
- Token：报告 token 少 2,181,605。
- 重复探索：`repeated_known_info` 为 0，`no_handoff` 为 4。

已知遥测限制：`task-015` 两组 token 都异常（`no_handoff=0`、`rs_handoff=3`）。盲评时已要求 reviewer 不把这组 token 当成真实优势。

## 失败分布

- `no_handoff` 失败：`task-007`、`task-016`。
- `rs_handoff` 失败：`task-016`。
- `task-007` 是最明显的差异样本：prompt-only 组未通过 Zip Slip 路径安全任务，RelayStack handoff 组通过。
- `task-016` 两组都失败，后续如果把题库长期化，应优先复查预期输出或题目边界。

## 盲评胜场

| Reviewer | 关注点 | `no_handoff` 胜场 | `rs_handoff` 胜场 |
| --- | --- | ---: | ---: |
| `efficiency_reviewer` | 耗时、步骤、重复探索 | 3 | 17 |
| `quality_token_reviewer` | 完成度、diff 聚焦、token | 4 | 16 |
| `debug_handoff_reviewer` | 可诊断性、可交接性 | 0 | 20 |

盲评平均分：

- `efficiency_reviewer`：`no_handoff=6.40`，`rs_handoff=7.95`。
- `quality_token_reviewer`：`no_handoff=7.81`，`rs_handoff=8.38`。
- `debug_handoff_reviewer`：`no_handoff=7.43`，`rs_handoff=8.595`。

## 盲测检查

- `packets.jsonl` 有 40 条匿名记录，不暴露 `runner`、`snapshot_generated`、`context_packet_summary`。
- `debug-packets.jsonl` 保留 debugger/handoff 上下文，但仍不暴露 runner 名称。
- `unblind-map.json` 是唯一把匿名 candidate 映射回真实 runner 的文件。
- `reviews.jsonl` 有 120 行：3 个 reviewer x 20 个 pair x 2 个 candidate。

## 结论

扩展后的题库比原始 5 题更能拉开差距：prompt-only 不再 100% 通过。RelayStack handoff 在完成度、总耗时、报告 token 和 debugger/handoff 盲评上都更强。

最核心的产品信号是交接面：reviewer 明显偏好带有明确 context packet、root-cause hint 和 validation summary 的 candidate，尤其是在后续接手和失败诊断场景中。

## 主要产物

- `reports/no_handoff-expanded-20260625.jsonl`
- `reports/rs_handoff-expanded-20260625.jsonl`
- `reports/blind-expanded-20260625/raw-runs.jsonl`
- `reports/blind-expanded-20260625/packets.jsonl`
- `reports/blind-expanded-20260625/debug-packets.jsonl`
- `reports/blind-expanded-20260625/reviews.jsonl`
- `reports/blind-expanded-20260625/unblind-map.json`
- `reports/blind-expanded-20260625/final.generated.md`
