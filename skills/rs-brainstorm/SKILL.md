---
name: rs-brainstorm
description: RelayStack discussion entry for unclear ideas. Triage to rs-feat-design, a personal feature brainstorm note, or rs-roadmap.
version: "0.1.0"
updated: 2026-07-10
---

# RS Brainstorm

## Personal Root Default

If `<personal-root>` is not provided, use the current project root: the Git
repository top-level when available, otherwise the current working directory.
Do not ask the user for a personal path. Keep personal records under the ignored
`/project/` tree.

Use this skill when the idea is not clear enough to design or build.

The goal is to clarify intent without polluting the team repository with raw
discussion. RelayStack follows AGE: team docs keep durable attractors; messy
thinking stays in `<personal-root>/project/features/` or
`<personal-root>/project/roadmaps/`. Personal brainstorm notes are optional and
non-authoritative; once the feature is clear, `rs-feat-design` writes the formal
team design under `docs/design/`.

## Triage

| Case | Signal | Route |
|---|---|---|
| Clear enough | goal, behavior, success, and non-goals are known | `rs-feat-design` |
| Small feature, still fuzzy | one feature can hold it, but solution or boundary is unclear | optionally write a personal brainstorm note, then create the formal team design with `rs-feat-design` |
| Large work, decomposition ready | multiple slices or modules are already visible | `rs-roadmap` |
| Large work, still fuzzy | broad idea needs grilling before decomposition | personal brainstorm note, then `rs-roadmap` |

## Workflow

1. Read existing attractor docs:
   - `docs/context/`
   - `docs/backlog/`
   - `docs/requirements/`
   - `docs/design/`
   - `docs/architecture/`
2. Reframe the user's proposal as the underlying problem.
3. Offer 2-3 concrete directions when helpful.
4. Decide the triage case.
5. If a note is needed, write it only to the user's personal project notes when
   a path is provided.
6. Update team docs only after a stable fact emerges.

## Rules

- Keep brainstorm archives only under ignored personal `project/` paths, never
  in tracked team docs.
- Do not start implementation from this skill.
- Do not force a clear request through brainstorming.
- If the idea is a broken existing behavior, route to `rs-issue`.
