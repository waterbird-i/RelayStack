---
name: rs-onboard
description: Onboard a repository into RelayStack by establishing project context and auditing optional owner docs.
version: "0.1.2"
updated: 2026-07-28
---

# RS Onboard

Use this skill to connect a repository to RelayStack.

The goal is not to install a platform. The goal is to establish one mandatory
project context entry point and let the other owner docs appear only when
durable facts need them.

## Target Shape

```text
docs/context/
docs/backlog/       # on demand
docs/requirements/  # on demand
docs/design/        # on demand
docs/architecture/  # on demand
```

These are the only team-maintained project doc categories RelayStack creates
or recommends committing. `docs/context/` is the mandatory adoption marker;
the other categories are lazy. The personal root is the current project root: use
the Git repository top-level when available, otherwise use the current working
directory. Do not ask the user to choose it. Personal records belong under:

```text
<personal-root>/project/
├── roadmaps/
├── features/
├── issues/
├── knowledge/
└── handoffs/
```

Keep these directories under the ignored `/project/` tree and never commit
them. Do not move or delete pre-existing legacy process files during onboarding
without an explicit migration request.

## Workflow

1. Scan existing repository docs, excluding `.git/`, `node_modules/`, and build
   output.
2. Check whether `project` exists, including symlinks, and whether Git ignores
   it. Treat an ignored `project/` as configured personal memory. Treat a
   tracked or unignored `project/` as legacy or misconfigured process memory;
   do not copy it into team docs.
3. If the user asks for audit only, stop at a migration map and create nothing.
4. Ensure `docs/context/relaystack-adoption.md` exists and records the owner
   contract. Do not create empty optional owner directories or README skeletons.
5. Use the current project root as the personal root. Add `/project/` to the
   project-root `.gitignore`; create personal subdirectories only when a later
   workflow needs them. Do not ask the user to choose a personal root.
6. If older docs already exist, propose a migration map before moving anything.
7. Keep heavy process records in the user's personal project directory, not the
   team documentation:
   - feature records in `project/features/`
   - issue records in `project/issues/`
   - sub-agent records
   - validation scratch notes
8. Record only the stable `/project/` storage contract in `docs/context/` so
   later skills do not have to infer it. Do not add a `RelayStack 个人存储根目录`
   field or a `TODO: 待确认` placeholder to a context `README.md`.
9. Report what was created, what was left in place, and which `rs-*` skill to
   use next.

## Rules

- Do not move or delete existing docs without user confirmation.
- Never commit `project/` as team documentation.
- Do not fill project facts with guesses. Use `TODO: 待确认` when needed, except
  for the personal root, which always defaults to the current project root.
- Keep the adoption skeleton limited to context and the ignore rule; create
  optional owner docs only for an actual durable fact.

Communicate what was created, what was preserved, and the useful next step in
the form that best fits the onboarding result. Mention documentation impact
only when relevant, without a fixed response template.
