---
name: rs-arch
description: Maintain RelayStack architecture attractor docs under docs/architecture/.
version: "0.1.0"
updated: 2026-06-24
---

# RS Arch

Use this skill to maintain `docs/architecture/`.

Architecture docs describe the current technical structure, module boundaries,
data flow, and stable contracts. They do not describe future plans.

## Modes

- `backfill`: document an existing module or system area.
- `update`: refresh architecture after code changed.
- `check`: compare docs, design, and code for consistency.

## Workflow

1. Read:
   - `docs/context/`
   - `docs/architecture/`
   - related `docs/design/`
   - related source files
2. Lock one target and one mode.
3. For backfill/update, write current facts only.
4. For check, report inconsistencies with file references and suggested fixes.
5. Route planned architecture changes to `rs-roadmap`.

## Suggested Shape

```markdown
# Architecture Area

## Current Responsibility

## Key Modules

## Data Flow

## Contracts

## Boundaries

## Verification
```

## Rules

- Current state only. Future target state belongs in `rs-roadmap`.
- Anchor important claims to code or existing docs.
- Do not change code from this skill.
- Do not create broad architecture rewrites in one pass.
