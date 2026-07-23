---
name: rs-learn
description: Capture a pitfall or good practice discovered during RelayStack work.
version: "0.1.2"
updated: 2026-07-23
---

# RS Learn

## Personal Root Default

If `<personal-root>` is not provided, use the current project root: the Git
repository top-level when available, otherwise the current working directory.
Do not ask the user for a personal path. Keep personal records under the ignored
`/project/` tree.

Use this skill when a feature, issue, or exploration produced reusable learning.

## Do Not Use When

- The learning is now a settled rule, constraint, or decision; use `rs-decide`.
- The detail is only useful for one incident; keep it in
  `<personal-root>/project/knowledge/`.
- The lesson has not been verified; use `rs-explore` first.

## Destination

- `<personal-root>/project/knowledge/`: raw story, failed attempts, and incident context.
- Team docs: only the stable lesson future work should reuse.

Stable lessons may update exactly one canonical owner:

- `docs/context/` for project-wide gotchas or workflow facts
- `docs/architecture/` for module-boundary lessons
- `docs/design/` for behavior or UX lessons

## Workflow

1. Decide whether this is a pitfall or good practice.
2. Check whether the lesson is already captured.
3. Write the shortest reusable lesson.
4. Link to the feature, issue, or handoff snapshot when useful.
5. Make one Documentation Decision. Keep incident context personal; promote
   only the shortest reusable fact to its one owner.

## Rules

- Do not archive one-off noise in team docs.
- Do not invent lessons to make a task look complete.
- If the lesson is actually a rule, use `rs-decide`.

## Output

```text
Documentation Decision
- Process record: none | project/knowledge/{slug}.md
- Team docs: none | <one canonical owner path>
- Reason: <reusable lesson, or why it remains personal>
```
