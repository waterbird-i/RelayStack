---
name: rs-roadmap
description: Plan RelayStack work that is too large for one feature, keeping roadmap prose personal and docs/backlog team-facing.
version: "0.1.0"
updated: 2026-07-10
---

# RS Roadmap

## Missing Personal Root

If `<personal-root>` is not provided, do not create a roadmap or substitute
process directory inside the repository. Return the proposed personal record in
the conversation and request or wait for a personal path. Continue any applicable
updates to the five team owner doc categories normally.

Use this skill when a request is too large for one `rs-feat` pass.

Do not use it just because a feature touches several modules. A single coherent
behavior with API, type, permission, and documentation impact should start with
`rs-feat-design`.

The roadmap body is a personal process record at
`<personal-root>/project/roadmaps/{slug}.md`, never a team project directory.
`docs/backlog/` may carry a concise team-visible priority, status, and next step
that links to stable requirements, design, or architecture facts.

## Inputs

- a personal root
- `docs/context/`, related `docs/requirements/` and `docs/architecture/`
- current `docs/backlog/`

## Workflow

1. Clarify the goal, users, boundaries, and success signal.
2. Define stable cross-feature contracts only where necessary.
3. Split the goal into independently deliverable feature slices.
4. Order by dependency and earliest useful value.
5. Write the roadmap body to `<personal-root>/project/roadmaps/{slug}.md`.
6. Update `docs/backlog/` only with team-visible priority, status, and next step.
7. Promote stable capability or structure facts to requirements or architecture.
8. Hand the first slice to `rs-feat-design`.

## Outputs

- personal roadmap: `<personal-root>/project/roadmaps/{slug}.md`
- optional team planning summary: `docs/backlog/`

## Guardrails

- Do not write the roadmap body into `docs/backlog/` or any repository directory.
- Do not describe `project/roadmaps/` as a team project directory.
- Do not create speculative implementation details for every slice.
- Do not treat the roadmap as architecture truth.
- Do not split by technical layer when a user-visible vertical slice is possible.
