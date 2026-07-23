---
name: rs-libdoc
description: Write source-of-truth reference documentation for public APIs, commands, or reusable components.
version: "0.1.2"
updated: 2026-07-23
---

# RS Libdoc

Use this skill for reference docs: "what does this public surface expose?"

## Do Not Use When

- The reader wants step-by-step task guidance; use `rs-guide`.
- The surface is private or unstable; use `rs-explore` first.
- The content is a project convention rather than a public surface; use
  `rs-decide`.

## Destination

Fit each reference entry into one canonical owner:

- public contracts and APIs -> `docs/architecture/`
- public command behavior -> `docs/context/`
- user-visible options or states -> `docs/design/`

Only create a separate API docs tree if the repository already uses one or the
user explicitly asks for it.

## Workflow

1. Identify the public surface and entry granularity.
2. Read source code for each entry.
3. Extract signatures, options, defaults, examples, and limitations from source.
4. Write one reference entry at a time.
5. Link guide docs when they explain task workflows.
6. Link to other owner docs rather than copying their facts.

## Rules

- Source code is the authority.
- Do not copy an old entry and rename it.
- Do not document private internals as public API.

## Output

```text
Documentation Decision
- Process record: none
- Team docs: none | <one canonical reference path>
- Reason: <explicit source-backed public reference request | no reference fact changed>
```
