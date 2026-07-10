---
name: rs-feat-accept
description: Validate feature implementation against the approved team design and write formal acceptance results back to team owner docs.
version: "0.1.0"
updated: 2026-07-10
---

# RS Feat Accept

## Missing Personal Root

If `<personal-root>` is not provided, do not create an acceptance note or
choose an undeclared personal storage location. Return the optional personal
note in the conversation and request or wait for a personal path. Still write the
formal acceptance result to the applicable team owner docs.

Use this skill after feature implementation.

The acceptance baseline is the approved team-owned design under `docs/design/`.
Formal acceptance results must be written back to the applicable team owner docs.
A personal acceptance note under `<personal-root>/project/features/` is optional
process memory and is never the official result.

## Inputs

- approved `docs/design/{slug}.md`, or the project's existing design filename
- current implementation diff
- verification evidence
- related team owner docs

## Workflow

1. Read the approved team design and current diff.
2. Verify behavior against its acceptance criteria.
3. Check that non-goals stayed out.
4. Record the formal result in the applicable team owner docs:
   - `docs/backlog/`: status, verification, and next step
   - `docs/requirements/`: settled capability behavior
   - `docs/design/`: accepted behavior, deviations, or follow-up decisions
   - `docs/architecture/`: real structural changes
   - `docs/context/`: durable workflow or operating facts
5. Report remaining gaps and route unresolved defects to `rs-issue`.
6. Optionally save a personal acceptance note under
   `<personal-root>/project/features/`.

## Output

Required:

```text
Acceptance: pass | partial | fail
Team Docs Updated:
- docs/...
Verification:
- command: result
Remaining Gaps:
- item
```

Optional:

```text
<personal-root>/project/features/{slug}-acceptance-note.md
```

## Guardrails

- Do not treat a personal acceptance note as the official acceptance result.
- Do not mark work accepted without verification evidence.
- Do not update docs with intended behavior that the code does not implement.
- Do not leave formal acceptance results only in chat or personal notes.
- Keep optional acceptance archives only under ignored `project/features/`,
  never in `docs/` or another tracked path.
