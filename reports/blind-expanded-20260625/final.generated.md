# Blind Benchmark Summary

## Runner Totals

| Runner | Runs | Pass Rate | Total Seconds | Total Tokens |
| --- | ---: | ---: | ---: | ---: |
| `no_handoff` | 20 | 90.0% | 2367.293 | 9,391,563 |
| `rs_handoff` | 20 | 95.0% | 1791.844 | 7,209,958 |

## Reviewer Wins

| Reviewer | Runner | Wins |
| --- | --- | ---: |
| `debug_handoff_reviewer` | `rs_handoff` | 20 |
| `efficiency_reviewer` | `no_handoff` | 3 |
| `efficiency_reviewer` | `rs_handoff` | 17 |
| `quality_token_reviewer` | `no_handoff` | 4 |
| `quality_token_reviewer` | `rs_handoff` | 16 |

## Notes

- `raw-runs.jsonl` is the only file that should expose real runner names.
- Reviewer packets should stay anonymized until `unblind-map.json` is used by the aggregator.
