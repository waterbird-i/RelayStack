---
name: rs-arch
description: Maintain RelayStack architecture attractor docs under docs/architecture/.
version: "0.1.2"
updated: 2026-07-23
---

# RS Arch

Use this skill to maintain `docs/architecture/`.

Architecture docs describe the current technical structure, module boundaries,
data flow, and stable integration contracts after they are real in the
implementation. They do not describe future plans or merely suspected impact.

## Modes

- `backfill`: document an existing module or system area.
- `update`: refresh architecture after code changed.
- `check`: compare docs, design, and code for consistency.

## Workflow

1. Read `docs/context/`, the directly related architecture doc when it exists,
   linked design sections, and the real source files for the target area.
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
- Do not copy capability goals or feature behavior; link to their canonical
  requirements or design owner.
- Use this explicit route after implementation when a real boundary, data flow,
  or integration contract changed; touching code alone is not an architecture
  trigger.

## Output

```text
Documentation Decision
- Process record: none
- Team docs: none | docs/architecture/{slug}.md
- Reason: <explicit current-architecture maintenance request | check mode produced no doc>
```
