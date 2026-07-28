---
name: rs-req
description: Maintain RelayStack requirements attractor docs under docs/requirements/.
version: "0.1.2"
updated: 2026-07-28
---

# RS Req

Use this skill to maintain `docs/requirements/`.

Requirements explain a reusable, long-lived capability contract: what users
should be able to observe, why it matters, expected behavior, and explicit
non-goals. They do not describe implementation steps and are not required for a
task-local change.

## Modes

- `draft`: capture a future capability before implementation.
- `backfill`: document an existing capability that is already real.
- `update`: refresh a requirement after behavior changes.

## Workflow

1. Read `docs/context/`, the directly related requirement when it exists, and
   only linked design or backlog entries needed to resolve the capability
   contract.
2. Lock one capability and one mode.
3. Draft or update one requirement document.
4. Keep implementation details out. Move technical structure to `rs-arch`.
5. If the work is too large to implement directly, route to `rs-roadmap`.

## Suggested Shape

```markdown
# Capability Name

## User Stories

## Why It Matters

## Expected Behavior

## Non-Goals

## Verification
```

## Rules

- One capability per file.
- Do not invent user stories.
- Do not write implementation details.
- Do not update code from this skill.
- Do not create design or architecture docs from this skill; link to their
  canonical owners when the requirement depends on them.
- A design may link this requirement's goals and acceptance criteria; do not
  duplicate them in `docs/design/`.

Communicate the requirement path, capability contract, and relevant evidence in
the form most useful for the request. Do not use a fixed response template.
