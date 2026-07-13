---
name: rs-feat
description: Start and guide a RelayStack feature change. Use when adding a new capability and the team repository should converge on docs/context, docs/backlog, docs/requirements, docs/design, and docs/architecture instead of storing full process archives.
version: "0.1.1"
updated: 2026-07-13
---

# RS Feat

## Personal Root Default

If `<personal-root>` is not provided, use the current project root: the Git
repository top-level when available, otherwise the current working directory.
Do not ask the user for a personal path. Keep personal records under the ignored
`/project/` tree.

Use this skill when the request adds a new capability.

RelayStack feature work uses an approved team-owned design under `docs/design/`
to drive implementation. Optional brainstorms, checklists, implementation notes,
and acceptance notes stay under `<personal-root>/project/features/` as personal,
Git-ignored process records.

## Do Not Use When

- The request is tiny, clear, and low risk; use `rs-feat-ff`.
- Existing behavior is broken; use `rs-issue`.
- The work is too large for one feature slice; use `rs-roadmap`.

Cross-module impact alone does not make work a roadmap. If one coherent
user-facing behavior needs API, type, permission, and doc changes, route to
`rs-feat-design` first.

## Workflow

1. Read the attractor docs before implementation:
   - `docs/context/`
   - `docs/backlog/`
   - `docs/requirements/`
   - `docs/design/`
   - `docs/architecture/`
2. State what is known, missing, and affected:
   - what should be built
   - why it matters now
   - which existing design or architecture it touches
   - whether `rs-req`, `rs-arch`, or `rs-roadmap` should run first
3. If the request is still unclear, keep brainstorming in the user's personal
   project notes, not in the team repository.
4. If the request is too large for one complete slice, route to `rs-roadmap`.
5. Implement the smallest complete slice.
6. After implementation, decide whether any durable team fact changed. Update
   zero, one, or multiple affected attractor docs as warranted:
   - `docs/backlog/`: status, owner, next action, verification
   - `docs/requirements/`: settled behavior or acceptance criteria
   - `docs/design/`: final app behavior and user flow
   - `docs/architecture/`: real structure, boundaries, or contracts
7. Use `rs-handoff` when another person or agent needs to continue.

## Routes

| Current state | Route |
|---|---|
| idea is fuzzy | `rs-brainstorm` |
| clear feature, needs formal team design | `rs-feat-design` |
| approved design exists under `docs/design/` | `rs-feat-impl` |
| implementation is done | `rs-feat-accept` |
| tiny, clear, low-risk change | `rs-feat-ff` |
| multiple independently deliverable slices or dependency ordering | `rs-roadmap` |

## Personal Project Notes

Optional feature process records belong in
`<personal-root>/project/features/`, never in team-maintained project docs. When
the repository root is the personal root, these records must remain ignored by
Git. The formal, approved implementation design belongs in `docs/design/`; no
personal feature record may replace or override it. Personal records include:

- brainstorm trails
- sub-agent records
- temporary checklists
- implementation notes
- acceptance notes
- validation scratch notes

## Rules

- Create feature process records under `project/features/` in the user's
  personal project directory when available.
- Do not treat `project/features/` records as team-maintained docs.
- Do not store full design/checklist/acceptance archives in `docs/`.
- Do not update docs solely because this skill ran.
- Do not update attractor docs with guesses. Write `未发现` or ask for the
  missing fact when it blocks safe work.
- If the work is actually a bug or regression, use `rs-issue`.
- Keep validation scoped. Do not run full TypeScript checks unless the user asks.
