# Handoff Snapshot：扩展 Benchmark A/B 运行

生成时间：2026-06-25

## 目标

把 terminal-bench 风格评测新增 20 道题，运行 prompt-only 与 RelayStack rs-handoff 的 A/B benchmark，并派 3 个盲评 subagent 分别评分：效率、完成度/token、debugger/handoff 质量。

## 已完成

- 新增 `tasks/task-006` 到 `tasks/task-025`。
- 更新 benchmark 文档：`docs/dev/benchmark-evaluation.md`。
- 更新 runner 公共能力：`runners/_runner.py`，包括：
  - metrics JSON 收集；
  - `--blind-dir`；
  - `--seed`；
  - 匿名 candidate ID；
  - raw / packet / debug packet 输出；
  - 每次运行的 artifact 目录。
- 新增辅助脚本：
  - `scripts/add_benchmark_tasks.py`
  - `scripts/summarize_blind_benchmark.py`
- 在用户授权后，已调用外部 Codex/model 服务对 20 道扩展题完整跑 A/B。
- 已运行 3 个盲评 subagent：
  - `efficiency_reviewer`
  - `quality_token_reviewer`
  - `debug_handoff_reviewer`

## 最终结果

| Runner | 运行数 | 通过数 | 总耗时 | 总 Token |
| --- | ---: | ---: | ---: | ---: |
| `no_handoff` | 20 | 18 | 2367.293 | 9,391,563 |
| `rs_handoff` | 20 | 19 | 1791.844 | 7,209,958 |

解盲后的 reviewer 胜场：

- `efficiency_reviewer`：`rs_handoff` 17，`no_handoff` 3。
- `quality_token_reviewer`：`rs_handoff` 16，`no_handoff` 4。
- `debug_handoff_reviewer`：`rs_handoff` 20，`no_handoff` 0。

结论：RelayStack rs-handoff 在通过率、耗时、报告 token、重复探索减少、handoff/debugger 完整度上都胜出。

## 关键产物

- 人读报告：`reports/blind-expanded-20260625/final.md`
- 中文报告：`reports/blind-expanded-20260625/final.zh-CN.md`
- 机器报告：`reports/blind-expanded-20260625/final.generated.md`
- Prompt-only 原始运行：`reports/no_handoff-expanded-20260625.jsonl`
- RelayStack 原始运行：`reports/rs_handoff-expanded-20260625.jsonl`
- 盲测 raw 记录：`reports/blind-expanded-20260625/raw-runs.jsonl`
- Reviewer 输入：`reports/blind-expanded-20260625/packets.jsonl`
- Debug reviewer 输入：`reports/blind-expanded-20260625/debug-packets.jsonl`
- Reviewer 分数：`reports/blind-expanded-20260625/reviews.jsonl`
- 解盲映射：`reports/blind-expanded-20260625/unblind-map.json`

## 验证

- `python3 -m py_compile runners/_runner.py runners/no_handoff.py runners/rs_handoff.py scripts/add_benchmark_tasks.py scripts/summarize_blind_benchmark.py`
- `for task in tasks/task-{006..025}; do bash -n "$task/test.sh"; done`
- `git diff --check`
- no-op fail-before-fix 检查确认新增题在未修复前会失败。
- 盲测泄露检查确认 `packets.jsonl` 不暴露 runner 名称或 handoff context 字段。
- `reviews.jsonl` 解析检查确认共有 120 行评审记录，每个 reviewer 40 行。

## 注意事项

- `task-015` 两组 token 遥测异常（`0` 和 `3`）。不要使用这个 pair 做 task-level token 结论。
- 许多 Python 题的临时 agent diff 中带有 `__pycache__` artifact。这影响 reviewer 的风险评分，但不影响 benchmark pass/fail。
- `task-016` 两组都失败。如果这套题后续要长期公开使用，应优先复查这个任务的预期输出和边界。

## 下一步建议

如果要用于产品对外表达，引用扩展 20 题结果和盲评胜场表，不要再引用旧的 5 题 baseline 作为主要证据。
