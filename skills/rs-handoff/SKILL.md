---
name: rs-handoff
description: Generate a personal RelayStack handoff snapshot from current workspace evidence.
version: "0.1.0"
updated: 2026-07-10
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
Handoff snapshots are personal process records, not team project docs.

## Inputs

- repository root
- manual fields: task, goal, stage, owner, blockers, risks, next action, validation
- optional agent records
- optional `--personal-root` or explicit external `--output-dir` override

## Workflow

1. Collect the manual handoff fields from the conversation.
2. Ask only for missing facts that cannot be inferred safely.
3. Run the generator from the target repository root.
4. Pass each available agent record with `--agent-record`.
5. Read the generated snapshot and verify concrete evidence and next actions.
6. Report the snapshot path and remaining unknowns.

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

The snapshot may read team docs only from `docs/context/`, `docs/backlog/`,
`docs/requirements/`, `docs/design/`, and `docs/architecture/`. Its docs source
does not include `handoff/**`.

## Guardrails

- When the repository root is the personal root, write only under the ignored
  `project/handoffs/` directory and never commit it.
- Do not use `--output-dir` to write snapshots into the repository.
- Do not describe `project/handoffs/` as a team project directory.
- Do not move or delete legacy repo-local handoff files unless explicitly asked.
- Do not invent completed work, validation, blockers, risks, or agent conclusions.
- Do not include secrets, tokens, credentials, or private keys.
- Do not replace local Git evidence with chat memory.
