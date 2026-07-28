---
name: rs-feat
description: Route a RelayStack feature change through the smallest safe path without implementing or writing owner docs.
version: "0.1.4"
updated: 2026-07-28
---

# RS Feat

## Personal Root Default

If `<personal-root>` is not provided, use the current project root: the Git
repository top-level when available, otherwise the current working directory.
Do not ask the user for a personal path. Keep personal records under the ignored
`/project/` tree.

Use this skill when the request adds a new capability.

RelayStack feature work uses an approved team-owned design under `docs/design/`
only when the feature has an approval-worthy behavior or contract decision.
Clear, bounded, low-risk work may use `rs-feat-ff`. Optional process evidence
stays in one Git-ignored personal feature record; one-turn work normally has no
record.

## Do Not Use When

- The request is tiny, clear, and low risk; use `rs-feat-ff`.
- Existing behavior is broken; use `rs-issue`.
- The work is too large for one feature slice; use `rs-roadmap`.

Cross-module impact alone does not make work a roadmap. If one coherent
user-facing behavior needs API, type, permission, and doc changes, route to
`rs-feat-design` first.

## Workflow

1. Read `docs/context/`; when the matching current-work-state exists, read its
   `backlinks` and `context_manifest`; then read only slug-matched or directly
   related requirements, backlog, design, or architecture docs.
2. State what is known, missing, and affected:
   - goal and success condition
   - existing terminology or contract touched
   - whether the fast-path gate passes
   - whether design, an explicit requirements pass, or roadmap is required
3. Route according to the scope gate:
   - one small, clear, low-risk slice with no new terminology and no
     cross-module contract change -> `rs-feat-ff`;
   - a reusable user-observable capability contract is missing -> `rs-req`;
   - one coherent feature that needs an approval-worthy decision ->
     `rs-feat-design`;
   - multiple independently deliverable slices or dependency ordering ->
     `rs-roadmap`.
4. Do not implement or update team docs from this routing skill.
5. Route completed implementation to `rs-feat-accept`, where documentation
   impact is assessed after evidence is available.
6. Use `rs-handoff` only when another person or agent needs to continue.

## Routes

| Current state | Route |
|---|---|
| idea is fuzzy | `rs-brainstorm` |
| clear feature, fails the fast-path gate and needs formal design | `rs-feat-design` |
| reusable capability contract is missing | `rs-req` |
| approved design exists under `docs/design/` | `rs-feat-impl` |
| implementation is done | `rs-feat-accept` |
| tiny, clear, low-risk change | `rs-feat-ff` |
| multiple independently deliverable slices or dependency ordering | `rs-roadmap` |

## Personal Project Notes

The optional feature process record is one personal file:

```text
<personal-root>/project/features/{slug}.md
```

It is non-authoritative and must remain ignored by Git. It may contain
brainstorm context, checklists, implementation notes, acceptance evidence, and
backlinks, but it must never replace the approved team design. Do not create a
separate acceptance archive for the same feature.

## Rules

- Create at most one feature process record:
  `<personal-root>/project/features/{slug}.md`.
- Do not create that record for a one-turn task unless the user asks for a
  durable process note or another owner must continue.
- Do not treat the personal feature record as a team-maintained doc or as the
  authoritative design.
- Do not store full design/checklist/acceptance archives in `docs/`.
- Do not update team docs from this routing skill; acceptance assesses any
  documentation impact.
- Do not update attractor docs with guesses. Write `未发现` or ask for the
  missing fact when it blocks safe work.
- If the work is actually a bug or regression, use `rs-issue`.
- Keep validation scoped. Do not run full TypeScript checks unless the user asks.

Present the route in whatever form best fits the request. Make the evidence,
gate, missing facts, and next step clear when they matter; do not use a fixed
heading, field list, or order.
