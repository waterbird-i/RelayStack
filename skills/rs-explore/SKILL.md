---
name: rs-explore
description: Explore code or docs to answer a focused question and preserve reusable evidence.
version: "0.1.2"
updated: 2026-07-23
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
2. Read `docs/context/` and only directly related owner docs.
3. Read real code or files.
4. Put the short answer first.
5. List only evidence that supports the answer.
6. Identify candidate durable facts, but do not update team docs from this
   exploration skill. Route a confirmed fact to its explicit owner skill.
7. Put raw evidence notes in `<personal-root>/project/knowledge/`; use
   `rs-handoff` only for a personal continuation snapshot.

## Output

Answer first, then use this optional note shape:

```markdown
# Explore: {question}

## Short Answer
## Evidence
## Confidence
## Follow-Up
```

```text
Documentation Decision
- Process record: none | project/knowledge/{slug}.md
- Team docs: none
- Reason: exploration produces evidence, not an approved durable fact
```

## Rules

- Do not guess without reading.
- Do not turn exploration into a decision; use `rs-decide`.
- Do not update team docs from this skill.
- Do not dump long evidence into team docs unless it is stable owner context.
