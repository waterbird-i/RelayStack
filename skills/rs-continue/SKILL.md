---
name: rs-continue
description: Consume a fresh RelayStack handoff snapshot, claim the active current-work-state, and route to the next stage.
version: "0.1.1"
updated: 2026-07-28
---

# RS Continue

Use this skill when a person or agent takes over from a RelayStack handoff
snapshot.

This is a thin state-machine entry over
`project/handoffs/current-work-state.md`. It is not a queue, task tracker,
permission model, database, or team journal.

## Inputs

- a handoff snapshot path
- an existing active `project/handoffs/current-work-state.md`
- the new owner or claimant when known

## Workflow

1. Read the snapshot's machine-readable quality block.
2. Verify freshness before using any snapshot claims.
3. Confirm the snapshot and live state have the same `id` / `work_id`.
4. Confirm the live state is active and has a non-empty `context_manifest`.
5. Claim the next step with:

```bash
python3 <relaystack-plugin>/skills/rs-handoff/scripts/manage_work_state.py \
  --state project/handoffs/current-work-state.md \
  continue \
  <snapshot.md> \
  --claimed-by "<agent-or-person>"
```

6. Read the declared `context_manifest` buckets:
   - `docs`
   - `code`
   - `evidence`
7. Route to the single `next_skill` from the updated state. The expected
   continuation phases are `design`, `implement`, `accept`, `handoff`, or
   `sediment`.
8. Only after the active state is successfully claimed, communicate the updated
   state path, chosen next skill, and any missing fact in the form most useful
   for continuation. Do not use a fixed response template.

## Guardrails

- Do not continue from a stale snapshot.
- Do not continue from a finished current-work-state.
- Do not claim a snapshot whose `work_id` differs from the live state.
- Do not read the whole repository when the manifest is enough.
- Do not promote personal state into team docs unless a durable owner-doc fact
  changed.
