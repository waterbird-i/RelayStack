---
name: rs-feat-impl
description: Implement and verify a feature from an approved team-owned design under docs/design/.
version: "0.1.4"
updated: 2026-07-28
---

# RS Feat Impl

## Personal Root Default

If `<personal-root>` is not provided, use the current project root: the Git
repository top-level when available, otherwise the current working directory.
Do not ask the user for a personal path. Keep personal records under the ignored
`/project/` tree.

Use this skill when the formal feature design under `docs/design/` is approved.
That team owner doc is the authoritative implementation input. Personal records
under `<personal-root>/project/features/` may assist execution but cannot replace
or override the approved design.

## Inputs

- approved `docs/design/{slug}.md`, or the project's existing design filename
- only related owner-doc sections needed to resolve implementation contracts
- the single optional personal feature record
  `<personal-root>/project/features/{slug}.md`

## Workflow

1. Read the approved team design under `docs/design/`.
2. Read the matching current-work-state backlinks and `context_manifest` when
   present, then only the related requirements, architecture, backlog, and
   context sections needed for implementation.
3. Implement in the approved design order.
4. Stop if reality contradicts the design; update the team design through
   `rs-feat-design` before continuing.
5. Keep the diff as small as possible.
6. Run the smallest checks that prove the slice works.
7. Summarize changed files, checks, and candidate durable facts discovered by
   the implementation.
8. Append implementation evidence, if needed, only to the existing or explicitly
   requested `<personal-root>/project/features/{slug}.md` record. Do not create a
   record for a one-turn implementation merely because this skill ran.
9. Route the completed implementation to `rs-feat-accept`.

`rs-feat-impl` never creates or updates team docs.

## Communication

Summarize the implementation in the form that best fits the change. Include
changed files, verification, candidate durable facts, or personal-record
impact when useful, but do not follow a fixed heading, field list, or order.

## Guardrails

- Do not implement from a personal brainstorm, checklist, or feature note alone.
- Do not expand scope during implementation.
- Do not fix unrelated bugs; route them to `rs-issue`.
- Do not create or update team docs.
- Do not skip verification because the diff is small.
