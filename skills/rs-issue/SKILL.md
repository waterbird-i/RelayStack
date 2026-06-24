---
name: rs-issue
description: Fix a RelayStack issue while preserving root cause notes privately and updating only durable team attractor docs after the fix.
---

# RS Issue

Use this skill when existing behavior is broken, incorrect, or risky.

The fix should leave two kinds of memory:

- private process memory in the user's personal project notes
- durable team truth in the attractor docs

## Workflow

1. Read the attractor docs before issue work:
   - `docs/context/`
   - `docs/architecture/`
   - `docs/design/`
   - `docs/backlog/`
   - `docs/requirements/`
2. Define the expected behavior from requirements or design. If it is missing,
   call that out before editing.
3. Reproduce or inspect the failure with the cheapest local evidence available.
4. Trace the real call path and every relevant caller before editing shared code.
5. Fix the root cause at the narrowest shared point.
6. Run the smallest check that would fail if the bug returned.
7. Record detailed report / analysis / fix-note in the user's personal project
   directory when one is provided.
8. Update only durable team attractor docs:
   - `docs/backlog/`: issue status and verification
   - `docs/requirements/`: changed or clarified expected behavior
   - `docs/design/`: changed supported behavior or state
   - `docs/architecture/`: root cause that exposes a stable boundary or contract
9. Use `rs-handoff` when the fix needs to be handed to another owner.

## Personal Project Notes

Keep these outside the team repository by default:

- reproduction transcript
- failed hypotheses
- stack traces
- logs
- sub-agent analysis
- fix-note details that are only useful for this incident

## Rules

- Do not create `.codestable/issues/` records in the team repository.
- Do not hide a behavior or architecture change only in the private notes.
- Do not broaden the fix into a new feature. Open a feature path instead.
- If the fix changes expected behavior, update requirements through `rs-req`.
- If the fix changes a stable boundary, update architecture through `rs-arch`.
- Do not update attractor docs with guesses. Only write stable facts.
- Keep validation scoped. Do not run full TypeScript checks unless the user asks.
