---
name: rs-feat-accept
description: Validate feature implementation against the approved team design and update applicable team owner docs when durable facts changed.
version: "0.1.1"
updated: 2026-07-13
---

# RS Feat Accept

## Personal Root Default

If `<personal-root>` is not provided, use the current project root: the Git
repository top-level when available, otherwise the current working directory.
Do not ask the user for a personal path. Keep personal records under the ignored
`/project/` tree.

Use this skill after feature implementation.

The acceptance baseline is the approved team-owned design under `docs/design/`.
Acceptance must be reported to the user. Update team owner docs only when the
result changes a durable team fact; the correct docs update count may be zero,
one, or multiple. A personal acceptance note under
`<personal-root>/project/features/` is optional process memory and is never the
official result.

## Inputs

- approved `docs/design/{slug}.md`, or the project's existing design filename
- current implementation diff
- verification evidence
- related team owner docs

## Workflow

1. Read the approved team design and current diff.
2. Verify behavior against its acceptance criteria.
3. Check that non-goals stayed out.
4. Decide whether the result changes durable team facts. If so, record only
   those facts in the applicable owner docs:
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
- docs/... | none
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
- Do not update docs solely because this skill ran.
- Do not update docs with intended behavior that the code does not implement.
- Always report the acceptance result to the user, even when no owner doc needs
  to change.
- Keep optional acceptance archives only under ignored `project/features/`,
  never in `docs/` or another tracked path.
