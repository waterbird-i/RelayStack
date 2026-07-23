> Status: implemented
> Date: 2026-07-23
> Storage: team-owned feature design

# RelayStack Artifact Lifecycle And Routing

## Context

RelayStack is a repo-local skill set and handoff protocol. Its durable project
memory is intentionally small: five owner categories in `docs/`, plus personal
process records and handoff artifacts under ignored `project/`.

The previous routing design made the right distinction between team facts and
personal notes, but still treated every workflow as if it needed a full set of
owner documents. It also spread continuation state across several stage
outputs. That made a small local change look like a requirements, design, and
architecture change even when no stable contract moved.

This design takes the useful Trellis shape without importing its runtime:

- keep one live state source for an active handoff;
- create stage artifacts only when their gate is needed;
- let implementation produce evidence and candidate facts;
- make one closeout decision after the evidence is available.

RelayStack does not add `.odd` state, odd-flow memory, a task graph, or a second
workflow runtime.

## Goal

Make the smallest artifact that preserves the next useful fact. A normal local
request may produce no team document and no personal process record. When a
stable fact does change, it must have one canonical owner and every other
document must link to that owner.

## Non-Goals

- Do not remove existing owner directories, historical records, or snapshots.
- Do not migrate or rename historical feature and issue files.
- Do not make every feature pass through a formal design.
- Do not make `rs`, `rs-feat`, or `rs-issue` implement code or write owner docs.
- Do not turn RelayStack into a task manager, workflow engine, or orchestration
  runtime.
- Do not change the machine-readable `current-work-state` schema.
- Do not create a second persistent workflow-state or navigation schema.

## Owner Contract

The five owner meanings remain, but creation and updates are conditional:

| Owner | Unique trigger |
|---|---|
| `context` | Project-wide rules, conventions, verification methods, or source-of-truth boundaries change. |
| `backlog` | The team needs ongoing coordination of priority, owner, status, or next action. |
| `requirements` | A reusable, long-lived, user-observable capability contract changes. |
| `design` | Before implementation, a behavior, state, permission, migration, terminology, or solution tradeoff needs human approval. |
| `architecture` | After implementation, real module boundaries, data flow, or integration contracts change. |

Apply these rules to every owner update:

1. One durable fact has one canonical owner.
2. A non-owner document links to the canonical owner and does not copy its body.
3. Update multiple owners only for multiple distinct facts or contracts.
4. Existing requirements are the source for a design's goals and acceptance
   criteria; an existing architecture document is the source for its technical
   contract and impact. The design links to both instead of duplicating them.
5. A missing optional owner directory is normal. Create it only when its unique
   trigger is true.

## Artifact Lifecycle

### Read Contract

Every ordinary workflow starts with targeted context:

1. Read `docs/context/` and the adoption contract.
2. Read `project/handoffs/current-work-state.md` when it exists and is relevant.
3. Resolve its `backlinks` and `context_manifest` buckets (`docs`, `code`, and
   `evidence`) before expanding the search.
4. Read only owner documents directly related to the request or matching the
   current work item's slug.
5. Use Git and source files for current implementation facts.

Do not scan all five owner directories merely because they exist. The five
directories are an owner allowlist, not a default read set.

For continuation, the live `current-work-state` is the only active-work state
source. It supplies continuation metadata such as `next_action`, `next_skill`,
backlinks, and the context manifest. It cannot silently override an approved
owner document or current code. A stale, incomplete, or contradictory state is
reported as missing/unknown and requires confirmation before continuing.

Use this authority order when facts conflict:

1. explicit user instruction;
2. a fresh live state for continuation metadata;
3. the relevant approved owner document for its contract;
4. current code, Git, and verification for implemented behavior;
5. personal records as evidence only;
6. an explicit missing-fact or confirmation gate.

The router must stop on a real conflict instead of merging sources by size,
recency, or apparent richness.

### Process Records

Create a personal process record only when the work needs cross-round memory,
handoff, or an explicit record requested by the user:

| Work | Default process record |
|---|---|
| One-turn local change | `none` |
| Multi-stage feature | At most `project/features/{slug}.md` |
| Issue investigation or fix | At most `project/issues/{slug}.md` |
| Multiple feature slices | `project/roadmaps/{slug}.md` |
| Handoff | One timestamped snapshot when transferred; current state only when machine-consumable continuation is needed |

Issue Report, Analysis, Fix, and Verification are optional sections appended to
the same issue record. They are not separate files and are not mandatory stages
for every bug. A small issue can go directly from `rs-issue` to a confirmed fix.

Feature brainstorm, implementation, and acceptance evidence may share the one
feature record when useful; do not create a separate checklist or acceptance
archive. A one-turn feature or issue defaults to no personal record.

### Feature Flow

- `rs-feat` only classifies and routes.
- A clear, local, low-risk request with no shared contract change uses
  `rs-feat-ff` and creates no design by default.
- A feature needing human approval creates exactly one
  `docs/design/{slug}.md` through `rs-feat-design`.
- `rs-feat-design` does not create or update requirements or architecture as a
  side effect. If a reusable capability contract is missing, route explicitly
  to `rs-req` first; if a technical fact is missing, use the relevant existing
  architecture source or an explicit architecture route.
- `rs-feat-impl` implements and verifies only. It reports candidate durable
  facts and does not write team docs.
- `rs-feat-accept` verifies the implementation once and makes the single final
  Documentation Decision. Task-local changes produce no team doc; non-local
  changes update only the triggered owner paths.

### Issue Flow

- `rs-issue` only classifies and routes; it does not implement or write owner
  docs.
- `rs-issue-report` is an optional structured-reproduction helper, used when
  evidence must be recorded or the user asks for a report.
- `rs-issue-analyze` is an optional diagnostic helper for unclear, risky, or
  multi-candidate root causes. It does not require a report to exist.
- `rs-issue-fix` applies a confirmed narrow fix, verifies it, and makes one final
  Documentation Decision.
- Report, Analysis, Fix, and Verification evidence, when retained, belongs in
  the one personal issue record.

### Roadmap And Knowledge

- `rs-roadmap` writes one personal roadmap. It adds a backlog summary only when
  the team actually needs ongoing coordination; a roadmap alone is not a
  backlog trigger.
- `rs-req` and `rs-arch` remain explicit maintenance/backfill entry points, not
  mandatory feature or issue substeps.
- `rs-learn`, `rs-trick`, `rs-decide`, `rs-explore`, `rs-guide`, and `rs-libdoc`
  write only the artifact explicitly requested or the stable fact their own
  contract owns.

## Router Contract

`rs`, `rs-feat`, and `rs-issue` are pure routers. Each one:

- reads targeted context and relevant continuation state;
- recommends exactly one next skill, or asks one blocking question;
- names the evidence and gate behind that recommendation;
- does not implement code, create process records, or update team owner docs.

The common routing output is:

```text
Route Recommendation
- Detected intent: <feature | issue | handoff | other>
- Evidence: <paths, state fields, or user facts>
- Next skill: <exactly one rs-* skill>
- Gate: <none | user confirmation | design approval | root-cause confirmation>
- Missing fact: <none | one fact needed before continuing>
```

Stage skills remain directly callable when the user explicitly requests them or
when the route has already established their gate.

## Documentation Decision

The first stage that writes a process or team artifact returns exactly one
decision for that write. Pure routers and read-only exploration do not invent a
decision. A later terminal stage may replace a deferred implementation note
with the final decision, but it must not create a second record.

```text
Documentation Decision
- Process record: none | <one path>
- Team docs: none | <one or more owner paths>
- Reason: <durable fact, or why no stable fact changed>
```

The process path is `none` for one-turn work. If a record already exists, append
to it; never create a second feature, issue, roadmap, checklist, analysis, or
acceptance file for the same work item.

## Handoff Contract

`current-work-state.md` remains the single live state file. Its existing
machine-readable schema is unchanged. `backlinks` and `context_manifest` point
the next owner at the relevant docs, code, and evidence.

Handoff snapshots are timestamped personal transfer artifacts. They may cite
the current state and selected owner docs, but they do not become owner docs and
do not create another workflow state. Handoff generation reads `docs/context/`
and only the manifest/backlink/slug-matched paths relevant to the current work;
it does not scan every owner directory by default.

Handoff and state closeout update only personal handoff artifacts. They do not
automatically promote a fact into an owner document; the same Documentation
Decision rules apply when a separate durable fact is identified.

## Acceptance Scenarios

The following fixed scenarios define the expected lifecycle:

1. Local copy or style change: no process record and no team docs.
2. Clear low-risk feature: direct implementation through `rs-feat-ff`, with no
   requirements, design, or architecture artifact by default.
3. Approval-worthy behavior or permission change: one design only before
   implementation; requirements is an explicit separate route if its reusable
   capability contract is missing.
4. Real API, data-shape, or permission-boundary change: acceptance updates
   architecture; requirements changes only when the user-observable capability
   contract also changed.
5. Ordinary bug fix: at most one personal issue record; no team docs when no
   stable fact changed.
6. Multi-slice goal: one personal roadmap; no backlog change without a team
   coordination need.
7. Handoff: only current state and a timestamped snapshot change; no owner doc
   is generated automatically.
8. Onboarding an empty repository: adoption context and `/project/` ignore rule
   only; no empty optional owner directories.
9. A stale state, missing manifest, broken backlink, or state/design conflict:
   continuation stops with an explicit missing/unknown fact.
10. Every write-capable scenario returns one `Documentation Decision` whose
    process record is `none` or the one canonical personal path and whose team
    docs list is `none` or the minimal owner paths.

Each scenario records pass, fail, or missing evidence in ignored
`project/knowledge/`; it does not create a tracked test document.

## Implementation And Rollout

This design is implemented through repository-local instructions and the
existing handoff scripts:

1. Keep `rs`, `rs-feat`, and `rs-issue` as routing-only entries.
2. Keep `rs-feat-design`, `rs-feat-impl`, `rs-feat-accept`, and issue helpers on
   the single-artifact lifecycle above.
3. Keep `current-work-state` and its schema as the only live state contract.
4. Make handoff evidence selection manifest-aware and lazy.
5. Verify the scripts, state transitions, ignore rule, and fixed scenarios.

No odd-flow state, task graph, or second runtime is introduced.

## Verification

```bash
python3 scripts/install_skills.py --self-test
python3 skills/rs-handoff/scripts/generate_snapshot.py --self-test
python3 skills/rs-handoff/scripts/manage_work_state.py --self-test
git check-ignore -q project/handoffs
git diff --check
```

The design status becomes `implemented` only after these checks and the fixed
scenario review pass.
