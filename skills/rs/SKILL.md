---
name: rs
description: RelayStack root entry. Use when the user says rs, asks which RelayStack skill to use, wants the system overview, or gives an open-ended request that should be routed to an rs-* skill.
version: "0.1.0"
updated: 2026-06-24
---

# RS

`rs` is the RelayStack root entry. It explains the system and routes open-ended
requests to the right `rs-*` skill.

It does not implement work. It only routes.

## Quick Scan

Before answering:

1. Verify paths before routing. Use real filesystem evidence, not memory or
   names in older notes.
2. Check whether these attractor docs exist:
   - `docs/context/`
   - `docs/backlog/`
   - `docs/requirements/`
   - `docs/design/`
   - `docs/architecture/`
3. Check whether `project` exists. If it exists, treat it as legacy or
   personal process memory, not as team attractor docs.
4. If the attractor docs are missing, route to `rs-onboard`.
5. Read the user's request and pick one skill from the routing table.

## System Overview

RelayStack keeps team repositories small by converging on durable attractor
docs, while personal project notes hold heavy process memory.

```text
team repo
├── docs/context/       mandatory context and source-of-truth rules
├── docs/backlog/       prioritized work and next actions
├── docs/requirements/  stable capability goals and behavior
├── docs/design/        stable app behavior and feature owner docs
└── docs/architecture/  current technical structure and boundaries

personal project notes
└── project/features/, project/issues/, agent records, validation logs
```

## Routing Table

| User intent | Route |
|---|---|
| Not sure which skill to use / wants overview | `rs` |
| Repository has not adopted attractor docs | `rs-onboard` |
| Idea is fuzzy / needs discussion | `rs-brainstorm` |
| Add a new capability | `rs-feat` |
| Design a clear feature | `rs-feat-design` |
| Implement an approved feature design | `rs-feat-impl` |
| Accept a completed feature and update docs | `rs-feat-accept` |
| Tiny clear feature, direct implementation | `rs-feat-ff` |
| Existing behavior is broken | `rs-issue` |
| Record a reproducible issue | `rs-issue-report` |
| Analyze root cause | `rs-issue-analyze` |
| Apply a confirmed issue fix | `rs-issue-fix` |
| Generate a handoff snapshot | `rs-handoff` |
| Draft or update capability requirements | `rs-req` |
| Backfill, update, or check architecture docs | `rs-arch` |
| Large work that needs decomposition | `rs-roadmap` |
| Capture a reusable lesson | `rs-learn` |
| Capture a reusable recipe or pattern | `rs-trick` |
| Record a settled decision | `rs-decide` |
| Explore code to answer a focused question | `rs-explore` |
| Write task-oriented guide docs | `rs-guide` |
| Write public API/reference docs | `rs-libdoc` |

If two routes both seem plausible, ask one short question instead of guessing.

## Rules

- Recommend one next skill, not a menu.
- Do not create files from this root entry.
- Do not route feature work into `rs-issue`, or issue work into `rs-feat`.
- If a request is too large for one feature, route to `rs-roadmap`.
- If the user asks only for an audit or judgment, do not route to a writer that
  creates files until the user confirms.
