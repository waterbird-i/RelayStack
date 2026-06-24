---
name: rs-issue-analyze
description: Find root cause, assess risk, and propose fixes for a RelayStack issue.
version: "0.1.0"
updated: 2026-06-24
---

# RS Issue Analyze

Use this skill after an issue report exists.

## Workflow

1. Read the issue report.
2. Read related attractor docs:
   - `docs/context/`
   - `docs/requirements/`
   - `docs/design/`
   - `docs/architecture/`
3. Trace the real code path.
4. Identify the root cause with file references.
5. Assess blast radius and regression risk.
6. Offer 2-3 fix options and recommend one.
7. Wait for user confirmation before editing.

## Output

```markdown
# {slug} Root Cause Analysis

## Key Locations
## Failure Path
## Root Cause
## Impact
## Fix Options
## Recommended Fix
```

## Rules

- Do not guess root cause without reading code.
- Do not change code from this skill.
- If expected behavior is missing, route to `rs-req`.
