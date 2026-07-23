---
name: rs-brainstorm
description: RelayStack discussion entry for unclear ideas. Triage to rs-feat-ff, rs-feat-design, or rs-roadmap with one optional personal record.
version: "0.1.2"
updated: 2026-07-23
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

1. Read `docs/context/` and only directly related owner docs needed to
   understand the proposal.
2. Reframe the user's proposal as the underlying problem.
3. Identify goal, success condition, non-goals, scope, and unresolved
   terminology or contract questions.
4. Decide the triage case:
   - one coherent feature with a clear boundary -> `rs-feat-design`;
   - multiple independently deliverable slices or dependency ordering ->
     `rs-roadmap`;
   - still too ambiguous to classify -> keep the discussion in the single
     personal feature record.
5. Keep discussion evidence in at most one
   `<personal-root>/project/features/{slug}.md` record only when cross-round
   memory is useful. Do not create one for a one-turn clarification.
6. Do not update team docs from brainstorming. Stable documentation is decided
   once at the appropriate terminal stage.

## Rules

- Keep brainstorm material only in the single ignored personal record
  `<personal-root>/project/features/{slug}.md`, never in tracked team docs.
- The personal record is non-authoritative and cannot replace
  `docs/design/{slug}.md`.
- Do not start implementation from this skill.
- Do not force a clear request through brainstorming.
- If the idea is a broken existing behavior, route to `rs-issue`.

## Output

```text
Route Recommendation
- Detected intent: unclear proposal
- Evidence: <request and targeted context paths>
- Next skill: <exactly one rs-* skill>
- Gate: <none | user confirmation | design approval>
- Missing fact: <none | one fact>

Documentation Decision
- Process record: none | project/features/{slug}.md
- Team docs: none
- Reason: discussion remains personal until a later route creates an approved
  durable fact
```
