---
name: rs-onboard
description: Onboard a repository into RelayStack by creating or auditing the five attractor doc directories under docs/.
version: "0.1.0"
updated: 2026-07-10
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

These are the only team-maintained project doc directories RelayStack creates
or recommends committing. Configure or ask for a personal root for:

```text
<personal-root>/project/
├── roadmaps/
├── features/
├── issues/
├── knowledge/
└── handoffs/
```

The repository root may be selected explicitly as the personal root only when
`/project/` is ignored by Git. In that configuration, keep these directories
under the ignored `/project/` tree and never commit them. Otherwise keep the
personal root outside the repository. Do not choose an undeclared personal
storage location. Do not move or delete pre-existing legacy process files
during onboarding without an explicit migration request.

## Workflow

1. Scan existing repository docs, excluding `.git/`, `node_modules/`, and build
   output.
2. Check whether `project` exists, including symlinks, and whether Git ignores
   it. Treat an ignored `project/` as configured personal memory. Treat a
   tracked or unignored `project/` as legacy or misconfigured process memory;
   do not copy it into team docs.
3. If the user asks for audit only, stop at a migration map and create nothing.
4. If the five directories are missing, create them with short `README.md`
   ownership notes.
5. Ask for or discover the personal-root choice. When the user explicitly
   chooses the repository root, add `/project/` to `.gitignore` before creating
   `project/{roadmaps,features,issues,knowledge,handoffs}/`.
6. If older docs already exist, propose a migration map before moving anything.
7. Keep heavy process records in the user's personal project directory, not the
   team documentation:
   - feature records in `project/features/`
   - issue records in `project/issues/`
   - sub-agent records
   - validation scratch notes
8. Record the selected storage contract in `docs/context/` so later skills do
   not have to infer it.
9. Report what was created, what was left in place, and which `rs-*` skill to
   use next.

## Rules

- Do not move or delete existing docs without user confirmation.
- Never commit `project/` as team documentation.
- Do not fill project facts with guesses. Use `TODO: 待确认` when needed.
- Keep the skeleton small enough that a team will actually maintain it.
