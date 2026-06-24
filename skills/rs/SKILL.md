---
name: rs
description: RelayStack root entry. Use when the user says rs, asks which RelayStack skill to use, wants the system overview, or gives an open-ended request that should be routed to an rs-* skill.
---

# RS

`rs` is the RelayStack root entry. It explains the system and routes open-ended
requests to the right `rs-*` skill.

It does not implement work. It only routes.

## Quick Scan

Before answering:

1. Check whether these attractor docs exist:
   - `docs/context/`
   - `docs/backlog/`
   - `docs/requirements/`
   - `docs/design/`
   - `docs/architecture/`
2. If they are missing, route to `rs-onboard`.
3. Read the user's request and pick one skill from the routing table.

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
└── brainstorms, reports, analysis, fix notes, agent records, validation logs
```

## Routing Table

| User intent | Route |
|---|---|
| Not sure which skill to use / wants overview | `rs` |
| Repository has not adopted attractor docs | `rs-onboard` |
| Add a new capability | `rs-feat` |
| Existing behavior is broken | `rs-issue` |
| Generate a handoff snapshot | `rs-handoff` |
| Draft or update capability requirements | `rs-req` |
| Backfill, update, or check architecture docs | `rs-arch` |
| Large work that needs decomposition | `rs-roadmap` |

If two routes both seem plausible, ask one short question instead of guessing.

## Rules

- Recommend one next skill, not a menu.
- Do not create files from this root entry.
- Do not route feature work into `rs-issue`, or issue work into `rs-feat`.
- If a request is too large for one feature, route to `rs-roadmap`.
