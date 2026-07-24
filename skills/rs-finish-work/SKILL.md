---
name: rs-finish-work
description: Close a RelayStack current work state after a fresh handoff snapshot and leave the next step as handoff or sediment.
version: "0.1.1"
updated: 2026-07-23
---

# RS Finish Work

Use this skill when the active work item is complete and the live state should
be closed.

This is a thin terminal step over
`project/handoffs/current-work-state.md`. It does not archive the repository,
create a task platform, or rewrite personal notes into team truth.

## Inputs

- a fresh handoff snapshot path
- an active `project/handoffs/current-work-state.md`
- the closing owner or claimant when known
- an optional next action, usually `sediment`

## Workflow

1. Verify the snapshot is fresh and still matches the live state `id` /
   `work_id`.
2. Confirm the live state is active and carries a non-empty `context_manifest`.
3. Close the state with:

```bash
python3 <relaystack-plugin>/skills/rs-handoff/scripts/manage_work_state.py \
  --state project/handoffs/current-work-state.md \
  finish \
  <snapshot.md> \
  --next-action sediment
```

4. Record `finished_by` and `finished_at` in the live state.
5. Leave the next step for handoff or knowledge sediment only if stable facts
   changed.
6. Report the closed state path, the final next action, unresolved durable
   facts, and:

```text
Documentation Decision
- Process record: project/handoffs/current-work-state.md
- Team docs: none
- Reason: close the single personal live state; route any remaining durable fact
  to its explicit owner skill instead of promoting it from handoff.
```

## Guardrails

- Do not finish from a stale snapshot.
- Do not finish a finished current-work-state again.
- Do not close a state whose `work_id` does not match the live state.
- Do not turn the live state into a history log or team journal.
