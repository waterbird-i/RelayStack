---
name: rs-issue-report
description: Turn a fuzzy problem report into a reproducible RelayStack issue report.
version: "0.1.0"
updated: 2026-07-10
---

# RS Issue Report

## Missing Personal Root

If `<personal-root>` is not provided, do not create an issue report or choose an
undeclared personal storage location. Return the report in the conversation
and request or wait for a personal path. Continue any applicable updates to the
five team owner doc categories normally.

Use this skill to record the problem before root-cause analysis.

The report is personal process memory. Keep it in
`<personal-root>/project/issues/`. It is not a team-maintained project directory
and must remain ignored by Git and uncommitted when the repository root is the
personal root.

## Workflow

Ask one question at a time:

1. What did you observe?
2. How can it be reproduced?
3. What was expected?
4. What actually happened?
5. Where did it happen?
6. How severe is it?

Then decide:

- simple, root cause obvious, low risk -> `rs-issue-fix`
- unclear, risky, or multi-candidate -> `rs-issue-analyze`

## Output

```markdown
# {slug} Issue Report

## Observed
## Reproduction
## Expected
## Actual
## Environment
## Severity
```

## Rules

- Report symptoms, not guessed causes.
- Do not fix from this skill.
- If it is a new capability request, route to `rs-feat`.
