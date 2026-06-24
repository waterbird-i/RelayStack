---
name: rs-guide
description: Write external-facing how-to documentation from RelayStack attractor docs and real code.
version: "0.1.0"
updated: 2026-06-24
---

# RS Guide

Use this skill for task-oriented docs: "how do I use this to do X?"

RelayStack does not create `docs/dev/` or `docs/user/` by default. Fit guides
into the existing attractor docs unless the repository already has a public docs
convention.

## Do Not Use When

- The doc is exhaustive API, command, or component reference; use `rs-libdoc`.
- The content is a settled convention or constraint; use `rs-decide`.
- The behavior is not verified from source or docs; use `rs-explore` first.

## Destination

- developer setup or contribution guides -> `docs/context/`
- integration and system usage guides -> `docs/architecture/`
- user-facing flows and feature guides -> `docs/design/`

## Workflow

1. Identify the reader: developer, integrator, or user.
2. Read relevant attractor docs and source files.
3. Check for existing guide content.
4. Write steps the reader can actually follow.
5. Keep implementation rationale out unless the reader needs it.

## Rules

- Do not copy internal design notes into guides.
- Do not invent API behavior.
- If the doc is reference-oriented, use `rs-libdoc`.
