---
name: rs-issue-analyze
description: Optionally diagnose an unclear or risky RelayStack issue and propose a fix without requiring a report record.
version: "0.1.3"
updated: 2026-07-23
---

# RS Issue Analyze

## Personal Root Default

If `<personal-root>` is not provided, use the current project root: the Git
repository top-level when available, otherwise the current working directory.
Do not ask the user for a personal path. Keep personal records under the ignored
`/project/` tree.

Use this optional helper when the root cause is unclear, risky, or has multiple
candidates. It can start from the user's description, current code evidence, or
an existing issue record; a report section is not required.

## Workflow

1. Read `docs/context/`, current-work-state when relevant, its backlinks and
   context manifest, and only related requirements, design, or architecture
   sections needed to establish expected behavior and blast radius.
2. Read an existing issue record when one is available; do not require one.
3. Trace the real code path.
4. Identify the root cause with file references.
5. Assess blast radius and regression risk.
6. Offer 2-3 fix options and recommend one.
7. Append the analysis only to an existing or explicitly requested
   `<personal-root>/project/issues/{slug}.md` record.
8. Wait for user confirmation before editing.

## Output

```markdown
---
id: {slug}
backlinks:
  - <related issue report, owner docs, or handoff snapshots>
---

## Analysis

### Key Locations
### Failure Path
### Root Cause
### Impact
### Fix Options
### Recommended Fix
```

```text
Documentation Decision
- Process record: none | project/issues/{slug}.md
- Team docs: none
- Reason: analysis is personal evidence until a confirmed fix changes a durable fact
```

## Rules

- Do not guess root cause without reading code.
- Do not change code from this skill.
- Do not create a separate analysis file for an existing issue record.
- Do not create a personal record merely because diagnosis was performed.
- If expected behavior is missing, route to `rs-req`.
