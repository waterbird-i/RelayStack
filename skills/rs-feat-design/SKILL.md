---
name: rs-feat-design
description: Create one approved team-owned feature design under docs/design/ when the approval gate requires it.
version: "0.1.3"
updated: 2026-07-23
---

# RS Feat Design

## Personal Root Default

If `<personal-root>` is not provided, use the current project root: the Git
repository top-level when available, otherwise the current working directory.
Do not ask the user for a personal path. Keep personal records under the ignored
`/project/` tree.

Use this skill after a feature is clear enough to design.

A request passes the design gate when its goal, success condition, one-feature
boundary, and non-goals are clear enough to approve behavior and contracts. If
they remain unclear, route to `rs-brainstorm`. If multiple independently
deliverable slices or dependency ordering are visible, route to `rs-roadmap`.
Tiny, clear, low-risk work with no new terminology and no cross-module contract
change routes to `rs-feat-ff` instead.

Do not equate invoking this skill with a design requirement. If the approval
gate does not pass, stop before writing and route to `rs-feat-ff` (or back to
`rs-feat` for clarification).

The formal design that is reviewed, approved, and used to drive implementation
is exactly one team owner doc at `docs/design/{slug}.md`, or the existing project
naming convention within `docs/design/`. Personal feature records under
`<personal-root>/project/features/` are optional process notes only. They may
contain working evidence, but must not be the authoritative design or the sole
implementation input.

## Inputs

Read only directly related source material:

- `docs/context/`
- the matching `current-work-state` backlinks and `context_manifest`, when
  present
- related `docs/requirements/`, `docs/architecture/`, or `docs/backlog/`
- the directly relevant existing team design under `docs/design/`
- the single optional personal feature record
  `<personal-root>/project/features/{slug}.md`

Do not read unrelated owner directories merely because they exist.

## Workflow

1. Confirm one feature scope and explicit non-goals.
2. If a reusable, long-lived, user-observable capability contract is missing,
   stop and route explicitly to `rs-req`; do not create a requirements document
   as a side effect.
3. Link existing requirements for goals and acceptance criteria, and link
   existing architecture docs for technical constraints and impact. Do not copy
   either owner into the design.
4. Draft or update the one formal design in `docs/design/{slug}.md`, following
   the directory's existing naming convention when one exists.
5. Cover current behavior, target behavior, user flow, contracts, affected
   modules, rollout, acceptance criteria, risks, and verification.
6. Get the team design approved before routing to `rs-feat-impl`.
7. Do not update requirements or architecture from this skill. Record possible
   post-implementation facts as candidates for `rs-feat-accept`.
8. Keep any working evidence in the single personal feature record and label
   it non-authoritative.

## Output

When the approval gate passes, the single authoritative output is:

```text
docs/design/{slug}.md
```

Optional personal process records:

```text
<personal-root>/project/features/{slug}.md
```

```text
Documentation Decision
- Process record: none | project/features/{slug}.md
- Team docs: none | docs/design/{slug}.md
- Reason: <design gate passed and an approval-worthy behavior/contract needs one design | design not needed; route to rs-feat-ff>
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
- Do not update requirements or architecture from this skill.
- If the work requires multiple independently deliverable slices, route to
  `rs-roadmap` before writing feature-level design.
