---
name: rs-roadmap
description: Plan RelayStack work that is too large for one feature, keeping roadmap prose personal and docs/backlog team-facing.
version: "0.1.3"
updated: 2026-07-28
---

# RS Roadmap

## Personal Root Default

If `<personal-root>` is not provided, use the current project root: the Git
repository top-level when available, otherwise the current working directory.
Do not ask the user for a personal path. Keep personal records under the ignored
`/project/` tree.

Use this skill when a request is too large for one `rs-feat` pass.

Do not use it just because a feature touches several modules. A single coherent
behavior with API, type, permission, and documentation impact should start with
`rs-feat-design`.

Use this skill only for a genuine multi-slice goal. In that case the roadmap
body is the one personal process record at
`<personal-root>/project/roadmaps/{slug}.md`, never a team project directory.
Do not create a roadmap record for work that fits one feature; route to
`rs-feat` instead.
`docs/backlog/` may carry a concise team-visible priority, status, and next step
that links to stable requirements, design, or architecture facts.

New roadmap records should start with the shared personal record header. Use the
file stem as `id`, and use `backlinks` for related backlog, requirements,
design, architecture, feature, issue, or handoff records. Do not rename
historical records merely to backfill the header.

## Inputs

- the resolved personal root
- `docs/context/`
- only related requirements, architecture, or backlog entries needed to
  understand durable constraints and team-visible priority

## Workflow

1. Clarify the goal, users, boundaries, and success signal.
2. Define stable cross-feature contracts only where necessary.
3. Split the goal into independently deliverable feature slices.
4. Order by dependency and earliest useful value.
5. Write the one roadmap body to
   `<personal-root>/project/roadmaps/{slug}.md`; do not create a second roadmap,
   checklist, or feature record for the same decomposition.
6. Update `docs/backlog/` only when the roadmap creates or changes a
   team-visible priority, owner, status, or next step. Communicate that impact
   when useful. Do not update requirements or architecture from roadmap
   planning.
7. Hand the first slice to `rs-feat-design`; use `rs-feat-ff` only when that
   slice independently passes the fast-path gate.

Communicate the roadmap path, first useful slice, dependencies, and any backlog
impact in the form most useful for the work. Do not use a fixed response
template.

## Guardrails

- Do not write the roadmap body into `docs/backlog/` or any team-maintained
  project directory. A repo-root personal archive must stay under ignored
  `project/roadmaps/`.
- Do not describe `project/roadmaps/` as a team project directory.
- Do not create speculative implementation details for every slice.
- Do not treat the roadmap as architecture truth.
- Do not write roadmap-derived requirements or architecture; route a stable
  fact to its explicit owner skill when it becomes real.
- Do not split by technical layer when a user-visible vertical slice is possible.
