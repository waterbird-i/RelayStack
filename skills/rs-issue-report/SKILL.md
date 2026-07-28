---
name: rs-issue-report
description: Optionally structure reproduction evidence for a RelayStack issue without forcing a multi-stage record.
version: "0.1.3"
updated: 2026-07-28
---

# RS Issue Report

## Personal Root Default

If `<personal-root>` is not provided, use the current project root: the Git
repository top-level when available, otherwise the current working directory.
Do not ask the user for a personal path. Keep personal records under the ignored
`/project/` tree.

Use this optional helper when reproduction evidence needs a structured record or
the user explicitly asks for an issue report. It is not a required step before
diagnosis or a fix.

If persistence is useful, the report is a section of the single personal issue
record `<personal-root>/project/issues/{slug}.md`. It is not a team-maintained
project directory and must remain ignored by Git. Otherwise return the evidence
without creating a file.

## Workflow

Ask one question at a time:

1. What did you observe?
2. How can it be reproduced?
3. What was expected?
4. What actually happened?
5. Where did it happen?
6. How severe is it?

Then recommend one next step when needed:

- simple, root cause obvious, low risk -> `rs-issue-fix`
- unclear, risky, or multi-candidate -> `rs-issue-analyze`

Communicate the reproduction evidence in the form most useful for the issue.
If a personal record is requested or genuinely useful, preserve the relevant
facts in the existing issue record, but do not require a fixed frontmatter or
response template.

## Rules

- Report symptoms, not guessed causes.
- Do not fix from this skill.
- Do not create a separate report file when the issue record already exists.
- Do not create a personal record merely because this helper ran.
- If it is a new capability request, route to `rs-feat`.
