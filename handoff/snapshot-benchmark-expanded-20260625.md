# Handoff Snapshot: expanded benchmark A/B run

Generated: 2026-06-25

## Goal

Expand the terminal-bench style evaluation by 20 tasks, run a prompt-only vs RelayStack rs-handoff A/B benchmark, and use 3 blind subagent reviewers to score efficiency, completion/token cost, and debugger/handoff quality.

## Completed

- Added `tasks/task-006` through `tasks/task-025`.
- Updated benchmark documentation in `docs/dev/benchmark-evaluation.md`.
- Updated runner support in `runners/_runner.py` for:
  - metrics JSON collection,
  - `--blind-dir`,
  - `--seed`,
  - anonymous candidate IDs,
  - raw/packet/debug packet emission,
  - run artifact folders.
- Added helper scripts:
  - `scripts/add_benchmark_tasks.py`
  - `scripts/summarize_blind_benchmark.py`
- Ran external Codex/model A/B benchmark for all 20 expanded tasks after user approval.
- Ran 3 blind subagent reviewers:
  - `efficiency_reviewer`
  - `quality_token_reviewer`
  - `debug_handoff_reviewer`

## Final Result

| Runner | Runs | Passed | Total Seconds | Total Tokens |
| --- | ---: | ---: | ---: | ---: |
| `no_handoff` | 20 | 18 | 2367.293 | 9,391,563 |
| `rs_handoff` | 20 | 19 | 1791.844 | 7,209,958 |

Blind reviewer wins after unblinding:

- `efficiency_reviewer`: `rs_handoff` 17, `no_handoff` 3.
- `quality_token_reviewer`: `rs_handoff` 16, `no_handoff` 4.
- `debug_handoff_reviewer`: `rs_handoff` 20, `no_handoff` 0.

Conclusion: RelayStack rs-handoff won on pass rate, elapsed time, reported token usage, repeated-exploration reduction, and handoff/debugger completeness.

## Key Artifacts

- Human report: `reports/blind-expanded-20260625/final.md`
- Machine report: `reports/blind-expanded-20260625/final.generated.md`
- Prompt-only raw run: `reports/no_handoff-expanded-20260625.jsonl`
- RelayStack raw run: `reports/rs_handoff-expanded-20260625.jsonl`
- Blind raw records: `reports/blind-expanded-20260625/raw-runs.jsonl`
- Reviewer input: `reports/blind-expanded-20260625/packets.jsonl`
- Debug reviewer input: `reports/blind-expanded-20260625/debug-packets.jsonl`
- Reviewer scores: `reports/blind-expanded-20260625/reviews.jsonl`
- Unblind map: `reports/blind-expanded-20260625/unblind-map.json`

## Validation Run

- `python3 -m py_compile runners/_runner.py runners/no_handoff.py runners/rs_handoff.py scripts/add_benchmark_tasks.py scripts/summarize_blind_benchmark.py`
- `for task in tasks/task-{006..025}; do bash -n "$task/test.sh"; done`
- `git diff --check`
- No-op fail-before-fix check confirmed new tasks fail before implementation.
- Blind packet leak check confirmed `packets.jsonl` does not expose runner names or handoff context fields.
- `reviews.jsonl` parse check confirmed 120 review rows, 40 rows per reviewer.

## Caveats

- `task-015` has anomalous token telemetry in both variants (`0` and `3` tokens). Treat task-level token comparison for that pair as invalid.
- Many Python-task agent diffs included `__pycache__` artifacts inside temporary run diffs. This affected reviewer risk scores but not benchmark pass/fail.
- `task-016` failed in both variants and should be reviewed if the benchmark set is used as a long-term public suite.

## Next Recommended Step

If this benchmark is used for product messaging, quote the expanded 20-task result and the blind-reviewer win table, not the older 5-task baseline.
