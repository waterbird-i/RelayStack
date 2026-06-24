---
name: rs-feat-impl
description: Implement a feature according to an approved RelayStack design note.
---

# RS Feat Impl

Use this skill when `{slug}-design.md` is approved.

## Workflow

1. Read the approved design note.
2. Re-read the related attractor docs before editing.
3. Implement in the design order.
4. Stop if reality contradicts the design; update the design or route back to
   `rs-feat-design`.
5. Keep the diff as small as possible.
6. Run the smallest checks that prove the slice works.
7. Summarize changed files and checks.

## Rules

- Do not expand scope during implementation.
- Do not fix unrelated bugs; route them to `rs-issue`.
- Do not update stable attractor docs until implementation facts are real.
- Use `rs-feat-accept` when implementation is done.
