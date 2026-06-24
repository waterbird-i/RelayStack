---
name: rs-roadmap
description: Plan RelayStack work that is too large for one feature, using docs/backlog as the team-facing planning attractor.
version: "0.1.0"
updated: 2026-06-24
---

# RS Roadmap

Use this skill when a request is too large for one `rs-feat` pass.

RelayStack does not add a separate roadmap tree by default. Team-facing planning
lives in `docs/backlog/`, with links to requirements, design, and architecture.

## Workflow

1. Read:
   - `docs/context/`
   - `docs/backlog/`
   - related `docs/requirements/`
   - related `docs/design/`
   - related `docs/architecture/`
2. Lock one large goal.
3. Define scope and explicit non-goals.
4. Split the work into small `rs-feat` seeds.
5. Record dependencies and the smallest useful end-to-end slice.
6. Update `docs/backlog/` with the agreed roadmap entry.

## Suggested Shape

```markdown
# Roadmap: Goal Name

## Goal

## Scope

## Non-Goals

## Current Attractor Docs

## Work Slices

## Dependencies

## Smallest Useful Slice

## Verification
```

## Rules

- Do not write detailed implementation design for each slice.
- Do not update architecture current-state docs with future target state.
- Do not split work into tasks that cannot be completed independently.
- If a slice is ready to implement, route it to `rs-feat`.
