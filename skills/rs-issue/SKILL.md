---
name: rs-issue
description: Route a RelayStack issue to the smallest safe diagnostic or fix path without implementing or writing owner docs.
version: "0.1.4"
updated: 2026-07-23
---

# RS Issue

## Personal Root Default

If `<personal-root>` is not provided, use the current project root: the Git
repository top-level when available, otherwise the current working directory.
Do not ask the user for a personal path. Keep personal records under the ignored
`/project/` tree.

Use this skill when existing behavior is broken, incorrect, or risky.

Issue work may leave two kinds of memory when they are explicitly useful:

- personal process memory in `<personal-root>/project/issues/`
- durable team truth in the attractor docs

## Do Not Use When

- The problem is a new capability request; use `rs-feat`.
- The user explicitly asks for structured reproduction evidence; use the
  optional `rs-issue-report` helper.
- Root cause and fix direction are already confirmed; route to `rs-issue-fix`.

## Workflow

1. Read `docs/context/`, current-work-state when relevant, its backlinks and
   context manifest, and only directly related owner docs.
2. Define the expected behavior from requirements, design, or current code. If
   the reusable user-observable contract is missing, route explicitly to
   `rs-req` instead of guessing.
3. Reproduce or inspect the failure with the cheapest local evidence available.
4. Route by the user's need and the evidence available:
   - structured reproduction evidence is requested or needed for handoff ->
     `rs-issue-report`;
   - root cause is unclear, risky, or has multiple candidates ->
     `rs-issue-analyze`;
   - root cause and fix direction are confirmed -> `rs-issue-fix`;
   - another owner must continue -> `rs-handoff`.
5. Do not implement or update team docs from this routing skill.

## Routes

| Current state | Route |
|---|---|
| structured reproduction evidence is needed | `rs-issue-report` |
| root cause is unclear or risky | `rs-issue-analyze` |
| root cause and fix are confirmed | `rs-issue-fix` |
| fix is complete and needs handoff | `rs-handoff` |
| problem is actually a new capability | `rs-feat` |

## Shared Issue Record Contract

For an issue that explicitly needs a persistent process record, use at most one
file:

```text
<personal-root>/project/issues/{slug}.md
```

Append only the sections that are useful, in this order:

```markdown
# {slug}

## Report
### Observed
### Reproduction
### Expected
### Actual
### Environment
### Severity

## Analysis
### Key Locations
### Failure Path
### Root Cause
### Impact
### Fix Options
### Recommended Fix

## Fix
### Changed Files
### Implementation
### Docs Updated
### Skipped
### Next Skill

## Verification
### Reproduction Check
### Regression Checks
### Result
### Remaining Risks
```

The record is personal, ignored, and non-authoritative. Do not create separate
report, analysis, or fix files for the same issue.

New issue process records should start with the shared personal record header.
Use the file stem as `id`, and use `backlinks` for related reports, analyses,
fix notes, handoff snapshots, or owner docs. Do not mass-migrate old records.

## Rules

- Create at most one issue process record under
  `<personal-root>/project/issues/{slug}.md` only when the user requests a
  record, another owner must continue, or cross-round evidence is genuinely
  useful. A one-turn issue defaults to no record.
- Do not treat `project/issues/` records as team-maintained docs.
- Do not update team docs from this routing skill; the confirmed fix makes one
  Documentation Decision.
- Do not hide a behavior or architecture change only in the private notes.
- Do not broaden the fix into a new feature. Open a feature path instead.
- If the fix changes a reusable user-observable capability contract, route the
  requirements update through `rs-req`.
- If the fix changes an implemented stable boundary, route the architecture
  update through `rs-arch`.
- Do not update attractor docs with guesses. Only write stable facts.
- Keep validation scoped. Do not run full TypeScript checks unless the user asks.

## Output

```text
Route Recommendation
- Detected intent: existing behavior is broken
- Evidence: <context, state, code, and request paths>
- Next skill: <exactly one rs-* skill>
- Gate: <none | user confirmation | root-cause confirmation>
- Missing fact: <none | one fact>
```
