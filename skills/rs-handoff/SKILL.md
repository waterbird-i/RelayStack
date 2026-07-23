---
name: rs-handoff
description: Generate a personal RelayStack handoff snapshot from current workspace evidence.
version: "0.1.3"
updated: 2026-07-23
---

# RS Handoff

## Personal Root Default

If neither `<personal-root>` nor an explicit external output directory is
provided, use the current project root: the Git repository top-level when
available, otherwise the current working directory. Do not ask the user for a
personal path. Write personal records under the ignored `/project/` tree; those
records are not team project documentation and must not be committed.

Use this skill to turn the current workspace state into a verifiable personal
handoff snapshot. It must contain real local evidence another owner can use.
Handoff snapshots are personal transfer artifacts, not team project docs or a
second process record.

`rs-handoff` also owns the lightweight live `current-work-state` protocol for a
single active work item. That state lives at
`<personal-root>/project/handoffs/current-work-state.md` and records:

- `id` / `work_id`
- `stage`
- `owner`
- `next_action`
- `evidence_fingerprint`
- `backlinks` / `linked_docs`
- `context_manifest` split into `docs` / `code` / `evidence`
- optional claim metadata such as `claimed_by` and `claimed_at`

The state must already be active and carry a non-empty context manifest before
`rs-continue` or `rs-finish-work` can consume it; a finished state is terminal
until a new live item is created.

A snapshot may still be generated without creating or updating live state. In
that case it remains a read-only transfer artifact; the Documentation Decision
still reports the snapshot path and does not claim a live-state update.

## Inputs

- repository root
- manual fields: task, goal, stage, owner, blockers, risks, next action, validation
- live current-work-state file, if present
- optional repeated `--context-doc` paths for related owner docs not yet listed
  in the live state
- optional agent records
- optional `--personal-root` or explicit external `--output-dir` override

## Workflow

1. Collect the manual handoff fields from the conversation.
2. Read `docs/context/` first. When a live `current-work-state` exists, use its
   `next_action`, `next_skill`, `backlinks`, and `context_manifest` to select
   only the related docs, code, and evidence for this handoff.
3. Ask only for missing facts that cannot be inferred safely.
4. Run the generator from the target repository root.
5. If the next owner is taking over, check freshness first, then use the lightweight state manager to `continue` or `finish` the live state.
6. Pass each available agent record with `--agent-record`.
7. Read the generated snapshot and verify concrete evidence, the context manifest, and next actions.
8. Report the snapshot path, remaining unknowns, and one Documentation Decision.

## Command

```bash
python3 skills/rs-handoff/scripts/generate_snapshot.py \
  --task "RelayStack MVP" \
  --goal "Generate one useful handoff snapshot" \
  --stage "MVP implementation" \
  --owner "current agent" \
  --next-step "Give the snapshot to the next owner" \
  --validation "Read the snapshot and answer the handoff questions"
```

```bash
python3 skills/rs-handoff/scripts/manage_work_state.py \
  --state project/handoffs/current-work-state.md \
  continue \
  <snapshot.md>

python3 skills/rs-handoff/scripts/manage_work_state.py \
  --state project/handoffs/current-work-state.md \
  finish \
  <snapshot.md> \
  --next-action sediment
```

`--personal-root` writes to `<personal-root>/project/handoffs`. It may equal the
repository root only when `/project/` is ignored by Git; other repository-local
personal roots are rejected. For compatibility, `--output-dir` may name an
explicit external directory. Relative `--output-dir` values are resolved from
the repository root and rejected because they remain inside it. When neither
output option is supplied, the command defaults to the current project root and
writes under its ignored `/project/handoffs/` directory.

## Output

```text
<personal-root>/project/handoffs/snapshot-<timestamp>.md
```

The snapshot reads `docs/context/` and only the owner-doc paths named by the
current work state's manifest, backlinks, or the current work item's slug. The
five categories (`docs/context/`, `docs/backlog/`, `docs/requirements/`,
`docs/design/`, and `docs/architecture/`) are an allowlist for those selected
paths, not a default scan. Its docs source does not include `handoff/**`.

The snapshot also carries the current work state's `context_manifest` so the
next owner can read only the docs, code, and evidence that this round needs.
When a live state exists, its `id` should reuse the canonical slug or file stem,
its `backlinks` should point at the stable related docs or records, and the live
state must stay active for consume to proceed.

```text
Documentation Decision
- Process record: project/handoffs/snapshot-<timestamp>.md
- Team docs: none
- Reason: timestamped personal transfer artifact; current-work-state is updated
  only when machine-consumable continuation is needed and remains the only live
  state source.
```

## Guardrails

- When the repository root is the personal root, write only under the ignored
  `project/handoffs/` directory and never commit it.
- Do not use `--output-dir` to write snapshots into the repository.
- Do not describe `project/handoffs/` as a team project directory.
- Do not move or delete legacy repo-local handoff files unless explicitly asked.
- Do not invent completed work, validation, blockers, risks, or agent conclusions.
- Do not turn `current-work-state` into a task platform or team journal.
- Do not create a second persistent workflow-state or navigation artifact.
- Do not include secrets, tokens, credentials, or private keys.
- Do not replace local Git evidence with chat memory.
