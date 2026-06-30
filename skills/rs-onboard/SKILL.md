---
name: rs-onboard
description: Onboard a repository into RelayStack by creating or auditing the five attractor doc directories under docs/.
version: "0.1.0"
updated: 2026-06-24
---

# RS Onboard

Use this skill to connect a repository to RelayStack.

The goal is not to install a platform. The goal is to make the team repository
converge on five durable attractor docs.

## Target Shape

```text
docs/context/
docs/backlog/
docs/requirements/
docs/design/
docs/architecture/
```

## Workflow

1. Scan existing repository docs, excluding `.git/`, `node_modules/`, and build
   output.
2. Check whether `project` exists, including symlinks. If it exists, report
   it as legacy or personal process memory; do not copy it into team docs.
3. If the user asks for audit only, stop at a migration map and create nothing.
4. If the five directories are missing, create them with short `README.md`
   ownership notes.
5. If older docs already exist, propose a migration map before moving anything.
6. Keep heavy process records in the user's personal project directory, not the
   team repository:
   - feature records in `project/features/`
   - issue records in `project/issues/`
   - sub-agent records
   - validation scratch notes
7. Report what was created, what was left in place, and which `rs-*` skill to
   use next.

## Rules

- Do not move or delete existing docs without user confirmation.
- Do not fill project facts with guesses. Use `TODO: 待确认` when needed.
- Keep the skeleton small enough that a team will actually maintain it.
