---
name: rs-issue-analyze
description: Find root cause, assess risk, and propose fixes for a RelayStack issue.
version: "0.1.0"
updated: 2026-07-10
---

# RS Issue Analyze

## Missing Personal Root

If `<personal-root>` is not provided, do not create issue analysis files or
choose an undeclared personal storage location. Return the analysis in the
conversation and request or wait for a personal path. Continue any applicable
updates to the five team owner doc categories normally.

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
7. Write the analysis to `<personal-root>/project/issues/` when a personal root
   is available.
8. Wait for user confirmation before editing.

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
