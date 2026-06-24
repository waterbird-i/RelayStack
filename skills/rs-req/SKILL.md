---
name: rs-req
description: Maintain RelayStack requirements attractor docs under docs/requirements/.
---

# RS Req

Use this skill to maintain `docs/requirements/`.

Requirements explain what capability should exist, why it matters, expected
behavior, and explicit non-goals. They do not describe implementation steps.

## Modes

- `draft`: capture a future capability before implementation.
- `backfill`: document an existing capability that is already real.
- `update`: refresh a requirement after behavior changes.

## Workflow

1. Read:
   - `docs/context/`
   - existing `docs/requirements/`
   - related `docs/design/`
   - related `docs/backlog/`
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
