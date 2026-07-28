---
name: rs-feat-accept
description: Validate feature implementation against the approved team design and update applicable team owner docs when durable facts changed.
version: "0.1.4"
updated: 2026-07-28
---

# RS Feat Accept

## Personal Root Default

If `<personal-root>` is not provided, use the current project root: the Git
repository top-level when available, otherwise the current working directory.
Do not ask the user for a personal path. Keep personal records under the ignored
`/project/` tree.

Use this skill after feature implementation.

The acceptance baseline is the approved team-owned design under `docs/design/`
when the feature required design. For `rs-feat-ff`, use the explicit user
request, stated success condition, implementation diff, and verification
evidence. Acceptance must always be reported. This is the single point at which
feature work decides whether durable team documentation changes are required.

## Inputs

- approved `docs/design/{slug}.md` when one exists, otherwise the fast-path
  request and success condition
- current implementation diff
- verification evidence
- the matching current-work-state backlinks and `context_manifest`, when
  present
- only related owner-doc sections needed to assess durable facts
- the optional single personal feature record
  `<personal-root>/project/features/{slug}.md`

## Workflow

1. Read the acceptance baseline and current diff.
2. Verify behavior against the design acceptance criteria or fast-path success
   condition.
3. Check that non-goals stayed out.
4. Classify every discovered change:
   - task-local or contained change -> no team doc;
   - project-wide rule or mandatory verification contract -> `docs/context/`;
   - team-visible priority, owner, or next action -> `docs/backlog/`;
   - durable capability or user-visible acceptance constraint ->
     `docs/requirements/`;
   - approved feature behavior or user flow -> `docs/design/`;
   - implemented structure, data flow, or integration boundary ->
     `docs/architecture/`.
5. Assess documentation impact. Give each durable fact one canonical owner and
   update only the minimal owner doc paths. Link across owners instead of
   duplicating facts.
6. Report remaining gaps and route unresolved defects to `rs-issue`.
7. Append acceptance evidence, if useful, to the existing or explicitly needed
   single personal feature record instead of creating a separate acceptance
   record. A one-turn feature normally has no process record.

## Communication

Report the acceptance result and the evidence that supports it in the form that
best fits the feature. Mention verification, remaining gaps, and documentation
impact when relevant; do not use a fixed heading, field list, or order.

## Guardrails

- Do not treat a personal feature record as the official acceptance result.
- Do not mark work accepted without verification evidence.
- Assign each durable fact to one canonical owner when documentation changes.
- Do not update docs with intended behavior that the code does not implement.
- Always report the acceptance result to the user, even when no owner doc needs
  to change.
- Never create a separate design, checklist, or acceptance archive for the same
  feature under `project/features/`.
