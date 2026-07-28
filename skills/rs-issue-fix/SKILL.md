---
name: rs-issue-fix
description: Apply a confirmed issue fix, verify it, and assess documentation impact.
version: "0.1.4"
updated: 2026-07-28
---

# RS Issue Fix

## Personal Root Default

If `<personal-root>` is not provided, use the current project root: the Git
repository top-level when available, otherwise the current working directory.
Do not ask the user for a personal path. Keep personal records under the ignored
`/project/` tree.

Use this skill when the root cause and fix direction are confirmed.

## Workflow

1. Read the issue report and analysis when available.
2. Read `docs/context/`, current-work-state when relevant, its backlinks and
   context manifest, then only the owner docs directly affected by the fix.
3. Make the narrowest root-cause fix.
4. Verify the original reproduction no longer fails.
5. Run scoped regression checks for the impact area.
6. Append Fix and Verification sections only to an existing or explicitly
   requested single `<personal-root>/project/issues/{slug}.md` record. A
   one-turn fix normally creates no process record.
7. After verification, assess documentation impact:
   - task-local fix -> no team doc;
   - changed a reusable user-observable capability contract ->
     `docs/requirements/`;
   - corrected an existing approved feature behavior or state -> `docs/design/`;
   - exposed a stable implemented technical boundary or contract ->
     `docs/architecture/`;
   - created an ongoing team coordination need -> `docs/backlog/`;
   - changed a project-wide rule or verification contract -> `docs/context/`.
   Update only the minimal owner paths and link across owners instead of copying
   the same fact.

## Do Not Use When

- Root cause is unclear; use `rs-issue-analyze`.
- Expected behavior is missing; use `rs-req`.
- The problem is actually a new capability gap; use `rs-feat`.

## Communication

Describe the fix and verification in the form most useful for the issue.
Mention changed files, documentation impact, remaining risks, or a next skill
when relevant, without a fixed heading, field list, or order.

## Rules

- Do not include unrelated cleanup.
- Do not update docs solely because this skill ran.
- Do not create separate report, analysis, or fix files for one issue.
- Do not introduce a new abstraction unless it is required to fix the root cause.
- If the fix reveals a new capability gap, route that gap to `rs-feat`.
