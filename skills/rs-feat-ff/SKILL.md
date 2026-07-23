---
name: rs-feat-ff
description: Fast RelayStack feature path for tiny changes that do not need a design phase.
version: "0.1.2"
updated: 2026-07-23
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

1. Read `docs/context/`; if a matching current-work-state exists, follow its
   backlinks and context manifest; then read only the directly related owner
   doc needed to confirm scope, terminology, and existing contracts.
2. Confirm all fast-path gates:
   - one small complete slice;
   - clear goal and success condition;
   - no new terminology;
   - no cross-module contract, permission, API, or architecture change;
   - no unresolved ambiguity.
3. If any gate fails, stop and route to `rs-feat-design`.
4. Implement the smallest working change.
5. Run the smallest useful check.
6. Route the completed change to `rs-feat-accept`; do not update team docs here.
7. Keep optional process evidence in at most one
   `<personal-root>/project/features/{slug}.md` record. A one-turn change
   defaults to no record.

## Rules

- No formal design phase on the fast path.
- No checklist or permanent process archive.
- Do not update team docs from this skill.
- Do not create more than one personal feature record, and do not create one
  merely because this skill ran.
- Do not use this for multi-step or ambiguous work.

## Output

```text
Checks:
- command: result

Documentation Decision
- Process record: none | project/features/{slug}.md
- Team docs: none
- Reason: fast-path implementation produces no durable team fact; final owner
  promotion is decided once by rs-feat-accept
```
