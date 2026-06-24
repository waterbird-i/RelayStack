---
name: rs-feat
description: Start and guide a RelayStack feature change. Use when adding a new capability and the team repository should converge on docs/context, docs/backlog, docs/requirements, docs/design, and docs/architecture instead of storing full process archives.
---

# RS Feat

Use this skill when the request adds a new capability.

RelayStack feature work keeps the heavy process outside the team repository and
updates only the durable attractor docs that future sessions must read.

## Workflow

1. Read the attractor docs before implementation:
   - `docs/context/`
   - `docs/backlog/`
   - `docs/requirements/`
   - `docs/design/`
   - `docs/architecture/`
2. State what is known, missing, and affected:
   - what should be built
   - why it matters now
   - which existing design or architecture it touches
3. If the request is still unclear, keep brainstorming in the user's personal
   project notes, not in the team repository.
4. Implement the smallest complete slice.
5. After implementation, update only the affected attractor docs:
   - `docs/backlog/`: status, owner, next action, verification
   - `docs/requirements/`: settled behavior or acceptance criteria
   - `docs/design/`: final app behavior and user flow
   - `docs/architecture/`: real structure, boundaries, or contracts
6. Use `rs-handoff` when another person or agent needs to continue.

## Personal Project Notes

Detailed process records belong in the user's personal project directory when
one is provided, such as:

- brainstorm trails
- draft plans
- sub-agent records
- temporary checklists
- validation scratch notes

If no personal project directory is provided, summarize the process in the final
reply or handoff snapshot. Do not invent a process directory inside the team
repository.

## Rules

- Do not create `.codestable/features/` records in the team repository.
- Do not store full design/checklist/acceptance archives in `docs/`.
- Do not update attractor docs with guesses. Write `未发现` or ask for the
  missing fact when it blocks safe work.
- If the work is actually a bug or regression, use `rs-issue`.
- Keep validation scoped. Do not run full TypeScript checks unless the user asks.
