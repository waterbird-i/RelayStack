---
name: rs-issue-report
description: Turn a fuzzy problem report into a reproducible RelayStack issue report.
version: "0.1.0"
updated: 2026-06-24
---

# RS Issue Report

Use this skill to record the problem before root-cause analysis.

The report is process memory. Keep it in `project/issues/` inside the user's
personal project directory. These records are personal modification history, not
team-maintained docs.

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
