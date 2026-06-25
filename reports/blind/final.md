# Blind Benchmark Report

## Scope

- Tasks: `task-001` to `task-005`
- Candidates: anonymized as `cand-a` / `cand-b` per pair
- Reviewers: `efficiency_reviewer`, `quality_token_reviewer`, `debug_handoff_reviewer`
- Source metrics: existing 2026-06-24 real runner reports

The expanded `task-006` to `task-025` suite is ready, but not executed in this
blind report.

## Reviewer Results

Efficiency reviewer:

- `cand-a` won 3 pairs.
- `cand-b` won 2 pairs.
- The reviewer only used elapsed time and token counts because step and
  repeated-exploration fields were unavailable.

Quality/token reviewer:

- Token side: `cand-a` won 4 pairs.
- Token side: `cand-b` won 1 pair.
- All candidates passed, so correctness tied.
- Diff and test-output evidence were missing, so change-quality scoring stayed
  conservative.

Debug/handoff reviewer:

- Candidates with an anonymous context packet and snapshot won all 5 pairs.
- 4 of those 5 also used less time and fewer tokens.
- `pair-002` used slightly more tokens, but was faster and had a handoff
  artifact.

## Unblinded Summary

After unblinding:

- `rs_handoff`: 5/5 passed, 360.556s total, 1,498,660 tokens.
- `no_handoff`: 5/5 passed, 466.965s total, 1,920,236 tokens.

Delta:

- `rs_handoff` was 106.409s faster, about 22.8%.
- `rs_handoff` used 421,576 fewer tokens, about 22.0%.

## Conclusion

On the first 5 tasks, both groups passed. The RelayStack handoff group was
faster and used fewer tokens overall, and the blind debug/handoff reviewer
preferred the candidates with an anonymous context packet and snapshot in every
pair.

This is still a small baseline. The expanded 20-task suite should be run next
before making stronger claims.

## Known Gaps

- No transcript summary.
- No diff summary.
- No test stdout summary.
- `steps_after_handoff` and `repeated_known_info` were missing in this run.
- Reviewer evidence is therefore enough for a baseline blind check, not for a
  strict process-quality audit.
