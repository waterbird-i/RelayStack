---
name: rs-issue-fix
description: Apply a confirmed issue fix, verify it, and update durable RelayStack attractor docs.
version: "0.1.0"
updated: 2026-06-24
---

# RS Issue Fix

Use this skill when the root cause and fix direction are confirmed.

## Workflow

1. Read the issue report and analysis when available.
2. Re-read affected code and attractor docs.
3. Make the narrowest root-cause fix.
4. Verify the original reproduction no longer fails.
5. Run scoped regression checks for the impact area.
6. Write detailed fix notes to `project/issues/` when available.
7. Update durable attractor docs:
   - `docs/backlog/`: issue status and verification
   - `docs/requirements/`: clarified expected behavior
   - `docs/design/`: changed supported behavior
   - `docs/architecture/`: stable boundary or contract exposed by the fix

## Do Not Use When

- Root cause is unclear; use `rs-issue-analyze`.
- Expected behavior is missing; use `rs-req`.
- The problem is actually a new capability gap; use `rs-feat`.

## Final Output

```markdown
Changed Files:
- ...

Checks:
- ...

Docs Updated:
- ...

Skipped:
- ...

Next Skill:
- ...
```

## Rules

- Do not include unrelated cleanup.
- Do not introduce a new abstraction unless it is required to fix the root cause.
- If the fix reveals a new capability gap, route that gap to `rs-feat`.
