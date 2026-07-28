---
name: rs-decide
description: Record an already-made RelayStack technical decision, constraint, or convention.
version: "0.1.2"
updated: 2026-07-28
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

Choose exactly one canonical owner for each settled fact:

- `docs/context/`: project-wide constraints, conventions, workflow decisions;
- `docs/backlog/`: settled team priority, owner, status, or next-action decisions;
- `docs/architecture/`: current architecture and technical structure decisions;
- `docs/requirements/`: product or capability boundary decisions;
- `docs/design/`: approved user-facing behavior decisions.

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
5. Link to related owner docs instead of repeating their facts.

## Rules

- Do not record tentative ideas as decisions.
- Do not overwrite an old decision silently; mark it superseded or add a new
  decision note.
- Do not invent rationale when it is unknown.

Communicate the settled decision, owner path, rationale, and consequences in
the form most useful for future contributors. Do not use a fixed response
template.
