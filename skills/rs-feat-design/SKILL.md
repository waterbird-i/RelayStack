---
name: rs-feat-design
description: Create or update the approved team-owned feature design under docs/design/ as the authoritative implementation input.
version: "0.1.0"
updated: 2026-07-10
---

# RS Feat Design

## Personal Root Default

If `<personal-root>` is not provided, use the current project root: the Git
repository top-level when available, otherwise the current working directory.
Do not ask the user for a personal path. Keep personal records under the ignored
`/project/` tree.

Use this skill after a feature is clear enough to design.

The formal design that is reviewed, approved, and used to drive implementation
is a team owner doc at `docs/design/{slug}.md`, or the existing project naming
convention within `docs/design/`. Personal feature records under
`<personal-root>/project/features/` are optional process notes only. They may
contain brainstorms, checklists, implementation notes, or acceptance notes, but
must not be the authoritative design or the sole implementation input.

## Inputs

- `docs/context/`
- related `docs/requirements/`, `docs/architecture/`, and `docs/backlog/`
- existing team design docs under `docs/design/`
- optional personal brainstorm notes

## Workflow

1. Confirm one feature scope and explicit non-goals.
2. Draft or update the formal design in `docs/design/{slug}.md`, following the
   directory's existing naming convention when one exists.
3. Cover current behavior, target behavior, user flow, contracts, affected
   modules, rollout, acceptance criteria, risks, and verification.
4. Update requirements or architecture only when the design settles durable
   capability or structural facts.
5. Get the team design approved before routing to `rs-feat-impl`.
6. Optionally keep checklists or working notes in
   `<personal-root>/project/features/`; label them non-authoritative.

## Output

Required authoritative output:

```text
docs/design/{slug}.md
```

Optional personal process records:

```text
<personal-root>/project/features/
```

## Design Shape

```markdown
# Feature: {name}

## Context
## Goal
## Non-Goals
## Current Behavior
## Proposed Behavior
## User Flow
## Contracts
## Affected Areas
## Acceptance Criteria
## Rollout
## Risks
## Verification
```

## Guardrails

- Do not place the formal or approved design in personal `project/features/`.
- Do not use a personal checklist or note as the sole implementation input.
- Do not implement from this skill.
- Do not hide contract changes inside implementation notes.
- If the work requires multiple independently deliverable slices, route to
  `rs-roadmap` before writing feature-level design.
