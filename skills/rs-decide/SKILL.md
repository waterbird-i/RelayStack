---
name: rs-decide
description: Record an already-made RelayStack technical decision, constraint, or convention.
version: "0.1.0"
updated: 2026-06-24
---

# RS Decide

Use this skill when a decision is already made.

Decisions are durable attractor facts. They belong in team docs when they affect
future contributors.

## Do Not Use When

- The point is a reusable pitfall or practice, but not a settled decision; use
  `rs-learn`.
- The decision is still being debated; use `rs-brainstorm`.
- The evidence is missing; use `rs-explore` first.

## Destination

- `docs/context/`: project-wide constraints, conventions, workflow decisions
- `docs/architecture/`: architecture and technical structure decisions
- `docs/requirements/`: product or capability boundary decisions
- `docs/design/`: user-facing behavior decisions

## Workflow

1. Confirm the decision is settled, not still being debated.
2. Identify the decision category:
   - tech stack
   - architecture
   - constraint
   - convention
3. Check existing docs for overlap.
4. Record:
   - decision
   - context
   - alternatives considered
   - consequences
   - where future work should look

## Rules

- Do not record tentative ideas as decisions.
- Do not overwrite an old decision silently; mark it superseded or add a new
  decision note.
- Do not invent rationale when it is unknown.
