---
name: rs
description: RelayStack root router. Use when the user asks which rs-* skill to use, wants the system overview, or gives an open-ended request.
version: "0.1.4"
updated: 2026-07-23
---

# RS

`rs` is the RelayStack root entry. It explains the system and routes open-ended
requests to exactly one `rs-*` skill.

It does not implement work. It only routes.

## Storage Contract

- Team-maintained, committable project docs use only five owner categories:
  `docs/context/`, `docs/backlog/`, `docs/requirements/`, `docs/design/`, and
  `docs/architecture/`. Only `docs/context/` is mandatory at adoption time;
  other owner directories are created on demand.
- Roadmap bodies, Feature process notes, Issue records, raw Knowledge, and
  Handoff Snapshots are personal records under
  `<personal-root>/project/{roadmaps,features,issues,knowledge,handoffs}/`.
- `<personal-root>` defaults to the current project root: use the Git repository
  top-level when available, otherwise use the current working directory. Do not
  ask the user to choose it.
- Before writing personal records, ensure `/project/` is ignored by Git. These
  records remain personal and must not be committed.
- `docs/backlog/` may hold team-visible priorities and next steps, but not the
  roadmap body. A formal feature design belongs in `docs/design/` only when the
  work has an approval-worthy behavior, state, permission, migration,
  terminology, or cross-module contract decision.
- When stable knowledge adds durable team truth, promote it into the applicable
  team doc categories; keep raw exploration and experience in personal
  `project/knowledge/`.
- Invoking a skill does not by itself require a `docs/` update. The first
  write-capable terminal stage makes one Documentation Decision after evidence
  is available. Update zero, one, or multiple owners only for distinct durable
  facts, and never touch every owner directory merely to show that documentation
  was considered.
- A documentation-specific skill such as `rs-req`, `rs-arch`, `rs-guide`, or
  `rs-libdoc` still produces the document explicitly requested by the user.

## Quick Scan

Before routing:

1. Verify the repository root and the existence of the relevant path.
2. Read `docs/context/` first.
3. When `project/handoffs/current-work-state.md` exists and applies to the
   request, read it next and follow only its `backlinks` and
   `context_manifest` paths after checking freshness.
4. Read only slug-matched or directly related requirements, backlog, design, or
   architecture docs needed for the selected route.
5. Check whether `project/` exists and whether Git ignores it before any
   personal record is written. An ignored `project/` is personal process
   memory; a tracked or unignored one is legacy or misconfigured process memory.
6. If `docs/context/` or its adoption contract is missing, route to
   `rs-onboard`. A missing optional owner directory is not a failure.
7. Do not read every attractor directory by default. Expand reads only when a
   related contract, dependency, or acceptance fact is missing.
8. Read the user's request and pick one skill from the routing table.

## System Overview

RelayStack keeps team repositories small by converging on durable attractor
docs, while personal project notes hold heavy process memory.

```text
team repo
├── docs/context/       mandatory project-wide context
├── docs/backlog/       optional team priorities and next actions
├── docs/requirements/  optional capability constraints
├── docs/design/        optional approved feature behavior
└── docs/architecture/  optional current technical structure

personal project notes
└── project/
    ├── roadmaps/
    ├── features/
    ├── issues/
    ├── knowledge/
    └── handoffs/
```

`project/handoffs/current-work-state.md` may hold one lightweight active work
state with `id` / `work_id`, `stage`, `owner`, `next_action`, an evidence
fingerprint, `backlinks` / linked docs, and a docs/code/evidence context
manifest. `rs-continue` and `rs-finish-work` are concepts over this shared
state: continue checks freshness, verifies the active manifest, and claims the
next step; finish closes the state and routes remaining work to handoff or
knowledge sediment. They are not a task platform or separate team journal.

## Routing Table

| User intent | Route |
|---|---|
| Not sure which skill to use / wants overview | `rs` |
| Repository has not adopted attractor docs | `rs-onboard` |
| Idea is fuzzy / needs discussion | `rs-brainstorm` |
| Add a new capability | `rs-feat` |
| Design a clear feature | `rs-feat-design` |
| Implement an approved feature design | `rs-feat-impl` |
| Accept a completed feature and make one documentation decision | `rs-feat-accept` |
| Tiny clear feature, direct implementation | `rs-feat-ff` |
| Existing behavior is broken | `rs-issue` |
| Record structured reproduction evidence when explicitly needed | `rs-issue-report` |
| Diagnose an unclear or risky issue | `rs-issue-analyze` |
| Apply a confirmed issue fix | `rs-issue-fix` |
| Generate a handoff snapshot | `rs-handoff` |
| Continue from an active handoff snapshot | `rs-continue` |
| Finish an active work state | `rs-finish-work` |
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
- Do not implement code or update team owner docs from this root entry.
- Do not route feature work into `rs-issue`, or issue work into `rs-feat`.
- If a request is too large for one feature, route to `rs-roadmap`.
- If the user asks only for an audit or judgment, do not route to a writer that
  creates files until the user confirms.
