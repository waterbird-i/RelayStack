---
name: rs-feat-design
description: Draft a small feature design note as the single input for implementation, while keeping stable facts aligned with RelayStack attractor docs.
version: "0.1.0"
updated: 2026-06-24
---

# RS Feat Design

Use this skill after a feature is clear enough to design.

In RelayStack, a design note is a working input, not a permanent team archive.
Keep it in `project/features/` inside the user's personal project directory.
These records are personal modification history, not team-maintained docs.

## Workflow

1. Read:
   - `docs/context/`
   - related `docs/requirements/`
   - related `docs/design/`
   - related `docs/architecture/`
   - related `docs/backlog/`
2. Confirm one feature scope and explicit non-goals.
3. Draft `{slug}-design.md` in `project/features/`.
4. Cover:
   - current behavior
   - planned behavior
   - user-visible acceptance criteria
   - affected attractor docs
   - implementation order
5. Ask for user approval before implementation.
6. If the work no longer fits one feature, route to `rs-roadmap`.

## Output

```markdown
# {slug} Design

## Goal
## Non-Goals
## Current Attractor Facts
## Proposed Behavior
## Implementation Order
## Acceptance Criteria
## Attractor Docs To Update
```

## Rules

- Do not write code from this skill.
- Do not store long design archives in team docs.
- Do not invent requirements or architecture facts.
- Use `rs-feat-impl` only after the design is approved.
