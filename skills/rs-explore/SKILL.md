---
name: rs-explore
description: Explore code or docs to answer a focused question and preserve reusable evidence.
version: "0.1.0"
updated: 2026-07-10
---

# RS Explore

## Personal Root Default

If `<personal-root>` is not provided, use the current project root: the Git
repository top-level when available, otherwise the current working directory.
Do not ask the user for a personal path. Keep personal records under the ignored
`/project/` tree.

Use this skill when the user asks how something works or wants evidence before
designing or fixing.

## Workflow

1. State the focused question.
2. Read relevant attractor docs.
3. Read real code or files.
4. Put the short answer first.
5. List only evidence that supports the answer.
6. If the conclusion is durable, update the right attractor doc.
7. Put raw evidence notes in `<personal-root>/project/knowledge/`; use
   `rs-handoff` only for a personal continuation snapshot.

## Output

```markdown
# Explore: {question}

## Short Answer
## Evidence
## Confidence
## Follow-Up
```

## Rules

- Do not guess without reading.
- Do not turn exploration into a decision; use `rs-decide`.
- Do not dump long evidence into team docs unless it is stable owner context.
