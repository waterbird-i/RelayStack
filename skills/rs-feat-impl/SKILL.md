---
name: rs-feat-impl
description: Implement a feature from an approved team-owned design under docs/design/.
version: "0.1.0"
updated: 2026-07-10
---

# RS Feat Impl

## Missing Personal Root

If `<personal-root>` is not provided, do not create implementation notes or
choose an undeclared personal storage location. Return optional personal
notes in the conversation and request or wait for a personal path. Continue code
and applicable team owner doc updates normally.

Use this skill when the formal feature design under `docs/design/` is approved.
That team owner doc is the authoritative implementation input. Personal records
under `<personal-root>/project/features/` may assist execution but cannot replace
or override the approved design.

## Inputs

- approved `docs/design/{slug}.md`, or the project's existing design filename
- related `docs/context/`, `docs/requirements/`, and `docs/architecture/`
- optional personal checklist or implementation notes

## Workflow

1. Read the approved team design under `docs/design/`.
2. Re-read the related team owner docs before editing.
3. Implement in the approved design order.
4. Stop if reality contradicts the design; update the team design through
   `rs-feat-design` before continuing.
5. Keep the diff as small as possible.
6. Run the smallest checks that prove the slice works.
7. Summarize changed files and checks.
8. Optionally save non-authoritative implementation notes under
   `<personal-root>/project/features/`.

## Output

```text
Changed Files:
- path: purpose

Checks:
- command: result

Docs Updated:
- docs/design/... or none yet
```

## Guardrails

- Do not implement from a personal brainstorm, checklist, or feature note alone.
- Do not expand scope during implementation.
- Do not fix unrelated bugs; route them to `rs-issue`.
- Do not update stable owner docs until implementation facts are real.
- Do not skip verification because the diff is small.
