# Blind Benchmark Summary

## Runner Totals

| Runner | Runs | Pass Rate | Total Seconds | Total Tokens |
| --- | ---: | ---: | ---: | ---: |
| `no_handoff` | 5 | 100.0% | 466.965 | 1,920,236 |
| `rs_handoff` | 5 | 100.0% | 360.556 | 1,498,660 |

## Reviewer Wins

| Reviewer | Runner | Wins |
| --- | --- | ---: |
| `debug_handoff_reviewer` | `rs_handoff` | 5 |
| `efficiency_reviewer` | `rs_handoff` | 5 |
| `quality_token_reviewer` | `no_handoff` | 1 |
| `quality_token_reviewer` | `rs_handoff` | 4 |

## Notes

- `raw-runs.jsonl` is the only file that should expose real runner names.
- Reviewer packets should stay anonymized until `unblind-map.json` is used by the aggregator.
