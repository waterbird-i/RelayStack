---
name: rs-learn
description: Capture a pitfall or good practice discovered during RelayStack work.
version: "0.1.0"
updated: 2026-06-24
---

# RS Learn

Use this skill when a feature, issue, or exploration produced reusable learning.

## Do Not Use When

- The learning is now a settled rule, constraint, or decision; use `rs-decide`.
- The detail is only useful for one incident; keep it in personal notes or
  `rs-handoff`.
- The lesson has not been verified; use `rs-explore` first.

## Destination

- Personal project notes: detailed story, failed attempts, incident context.
- Team docs: only the stable lesson future work should reuse.

Stable lessons usually update:

- `docs/context/` for project-wide gotchas or workflow facts
- `docs/architecture/` for module-boundary lessons
- `docs/design/` for behavior or UX lessons

## Workflow

1. Decide whether this is a pitfall or good practice.
2. Check whether the lesson is already captured.
3. Write the shortest reusable lesson.
4. Link to the feature, issue, or handoff snapshot when useful.

## Rules

- Do not archive one-off noise in team docs.
- Do not invent lessons to make a task look complete.
- If the lesson is actually a rule, use `rs-decide`.
