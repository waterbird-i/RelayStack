---
name: rs-explore
description: Explore code or docs to answer a focused question and preserve reusable evidence.
---

# RS Explore

Use this skill when the user asks how something works or wants evidence before
designing or fixing.

## Workflow

1. State the focused question.
2. Read relevant attractor docs.
3. Read real code or files.
4. Put the short answer first.
5. List only evidence that supports the answer.
6. If the conclusion is durable, update the right attractor doc.
7. Put detailed evidence notes in personal project notes or `rs-handoff`.

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
