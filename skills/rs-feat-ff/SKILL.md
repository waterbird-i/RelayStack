---
name: rs-feat-ff
description: Fast RelayStack feature path for tiny changes that do not need a design phase.
version: "0.1.0"
updated: 2026-06-24
---

# RS Feat FF

Use this skill when the request is small, clear, and low risk.

## Do Not Use When

- The scope needs design, new terminology, or contract changes; use
  `rs-feat-design`.
- Existing behavior is broken; use `rs-issue`.
- The task is multi-step or ambiguous; use `rs-feat`.

## Use When

- scope is one small slice
- no new terminology is needed
- no cross-module contract changes are expected
- the user wants direct implementation

## Workflow

1. Read `docs/context/` and any obviously related attractor docs.
2. Implement the smallest working change.
3. Run the smallest useful check.
4. Update durable attractor docs only if stable behavior changed.
5. If the task grows, stop and route to `rs-feat-design`.

## Rules

- No design note.
- No checklist.
- No permanent process archive.
- Do not use this for multi-step or ambiguous work.
