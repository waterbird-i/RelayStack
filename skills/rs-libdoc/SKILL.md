---
name: rs-libdoc
description: Write source-of-truth reference documentation for public APIs, commands, or reusable components.
---

# RS Libdoc

Use this skill for reference docs: "what does this public surface expose?"

## Destination

Fit reference docs into the existing attractor docs:

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

## Rules

- Source code is the authority.
- Do not copy an old entry and rename it.
- Do not document private internals as public API.
