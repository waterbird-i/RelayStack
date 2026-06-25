# 盲评 Benchmark 报告

## 范围

- 任务：`task-001` 到 `task-005`
- Candidate：每个 pair 匿名为 `cand-a` / `cand-b`
- Reviewer：`efficiency_reviewer`、`quality_token_reviewer`、`debug_handoff_reviewer`
- 数据来源：已有的 2026-06-24 真实 runner 报告

扩展题库 `task-006` 到 `task-025` 已准备好，但不属于这份 5 题基线盲评报告。

## Reviewer 结果

Efficiency reviewer：

- `cand-a` 赢 3 个 pair。
- `cand-b` 赢 2 个 pair。
- 因为当时没有步骤数和重复探索字段，reviewer 只使用耗时和 token 判断。

Quality/token reviewer：

- token 维度：`cand-a` 赢 4 个 pair。
- token 维度：`cand-b` 赢 1 个 pair。
- 所有 candidate 都通过，因此正确性打平。
- 缺少 diff 和测试输出证据，所以改动质量评分保持保守。

Debug/handoff reviewer：

- 带匿名 context packet 和 snapshot 的 candidate 赢下全部 5 个 pair。
- 其中 4 个 pair 同时耗时更少、token 更少。
- `pair-002` token 略高，但更快，并且有 handoff artifact。

## 解盲汇总

解盲后：

- `rs_handoff`：5/5 通过，总耗时 360.556s，1,498,660 tokens。
- `no_handoff`：5/5 通过，总耗时 466.965s，1,920,236 tokens。

差异：

- `rs_handoff` 快 106.409s，约 22.8%。
- `rs_handoff` 少用 421,576 tokens，约 22.0%。

## 结论

在第一批 5 个任务上，两组都通过。RelayStack handoff 组整体更快、token 更少；盲评中的 debug/handoff reviewer 在每个 pair 都更偏好带匿名 context packet 和 snapshot 的 candidate。

这仍然只是小样本基线。做更强结论前，应优先参考扩展后的 20 题正式结果。

## 已知缺口

- 没有 transcript summary。
- 没有 diff summary。
- 没有 test stdout summary。
- `steps_after_handoff` 和 `repeated_known_info` 在这次 run 中缺失。
- 因此这份证据足够做基线盲检，不足以做严格流程质量审计。
