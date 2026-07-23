---
name: rs-trick
description: Capture a reusable programming pattern, library usage, or technical recipe for RelayStack work.
version: "0.1.2"
updated: 2026-07-23
---

# RS Trick

## Personal Root Default

If `<personal-root>` is not provided, use the current project root: the Git
repository top-level when available, otherwise the current working directory.
Do not ask the user for a personal path. Keep personal records under the ignored
`/project/` tree.

Use this skill for prescriptive knowledge: "when doing X, use Y".

## Destination

- `<personal-root>/project/knowledge/` for raw investigation and examples.
- Team docs only when the trick is stable enough that future contributors should
  follow it.

Map a stable trick into exactly one canonical owner:

- `docs/context/` for workflow or command recipes
- `docs/architecture/` for implementation patterns
- `docs/design/` for interaction or behavior patterns

## Workflow

1. Classify the trick:
   - pattern
   - library usage
   - technique
2. Verify it against real code or a real command.
3. Record when to use it and when not to use it.
4. Add a small example only if it is real.
5. Make one Documentation Decision and link to existing owner facts instead of
   copying them.

## Rules

- Do not write unverified tricks.
- Do not duplicate existing docs.
- Do not turn a trick into a permanent rule; use `rs-decide` for that.

## Output

```text
Documentation Decision
- Process record: none | project/knowledge/{slug}.md
- Team docs: none | <one canonical owner path>
- Reason: <verified reusable recipe, or why it remains personal>
```
