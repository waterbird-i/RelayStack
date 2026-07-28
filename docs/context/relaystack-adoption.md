# RelayStack Adoption

This repository uses RelayStack's two-layer storage contract for its own
development.

## Team Facts

Only these directories contain team-maintained project documentation:

```text
docs/context/
docs/backlog/
docs/requirements/
docs/design/
docs/architecture/
```

- `docs/context/` records project-wide rules, conventions, verification, and
  source-of-truth boundaries.
- `docs/backlog/` records team priorities and next actions that need ongoing
  coordination.
- `docs/requirements/` records reusable, long-lived capability goals and
  user-observable constraints.
- `docs/design/` records behavior or solution choices that needed approval
  before implementation.
- `docs/architecture/` records implemented technical structure and boundaries.

Do not add another project-document category under `docs/`. Route a document to
one of these owners or keep it as personal process memory.

## Read Order And Lazy Owners

Read `docs/context/` before changing the repository. It is the mandatory
project-wide context entry point, not merely one peer among the five owner
directories.

Read the other owner directories only when the task touches their scope:

- `docs/backlog/` for team-visible priorities and next actions;
- `docs/requirements/` for capability goals, user-visible behavior, and
  acceptance constraints;
- `docs/design/` for approved feature behavior and user flows;
- `docs/architecture/` for current technical structure, boundaries, and
  integration contracts.

Do not read or update all five owner areas by default. A missing optional owner
directory is normal until a durable fact needs that owner.

The only creation/update trigger for each owner is:

| Owner | Trigger |
| --- | --- |
| `context` | Project-wide rules, conventions, verification methods, or source-of-truth boundaries change. |
| `backlog` | The team needs ongoing coordination of priority, owner, status, or next action. |
| `requirements` | A reusable, long-lived, user-observable capability contract changes. |
| `design` | Before implementation, an approval-worthy behavior, state, permission, migration, terminology, or solution tradeoff exists. |
| `architecture` | After implementation, real module boundaries, data flow, or integration contracts change. |

## Documentation Trigger

Invoking a RelayStack skill does not automatically require a team-doc update.
At the first write-capable terminal stage, determine whether it produced durable
facts that future contributors need. A later acceptance or fix stage may make
the final promotion decision. The correct result may be:

- no `docs/` change when no durable team fact changed;
- one owner-doc change when the fact has one clear owner; or
- multiple owner-doc changes when the work genuinely changes several contracts.

Do not create placeholder entries or touch all five directories merely to prove
that documentation was considered. Documentation-specific requests routed to
skills such as `rs-req`, `rs-arch`, `rs-guide`, or `rs-libdoc` are different:
the requested document is their deliverable.

## One Fact, One Owner

Each durable fact has exactly one canonical owner directory. The owner is
determined by the fact's primary question, not by the skill that discovered it.

| The fact primarily answers | Canonical owner |
| --- | --- |
| What must every contributor know before changing the repository? | `docs/context/` |
| What should the team pick up next? | `docs/backlog/` |
| What capability and user-visible constraints must hold? | `docs/requirements/` |
| How should an approved feature behave? | `docs/design/` |
| How is the implemented system structured and integrated? | `docs/architecture/` |

If a change appears to affect multiple owners, split it into distinct facts or
contracts and update only the owners of those facts. A non-owner document may
link to or cite the canonical owner, but must not duplicate or override it.

## Artifact Lifecycle

Create the smallest artifact that the work actually needs:

- one-turn, clear, low-risk work: no process record and no team doc by default;
- multi-stage feature work: at most one optional
  `project/features/{slug}.md` record;
- issue work: at most one optional `project/issues/{slug}.md` record with
  append-only Report, Analysis, Fix, and Verification sections;
- multi-slice work: one `project/roadmaps/{slug}.md` record;
- handoff work: one timestamped snapshot when ownership transfers; add or update
  `project/handoffs/current-work-state.md` only when machine-consumable
  continuation state is needed.

The formal `docs/design/{slug}.md` artifact is required only when the work has
an approval-worthy behavior, state, permission, migration, terminology, or
cross-module contract decision. It is not required for every feature.

Report, Analysis, Fix, and Verification are optional sections, not mandatory
issue stages. A small issue may go directly to a confirmed fix. A one-turn
feature or issue does not create a personal record by default.

RelayStack does not prescribe a response template. When a task creates or
updates a personal process record or team-owned document, explain the relevant
path and reason in the form that best fits the result. When no documentation is
affected, no dedicated documentation section is required. Documentation choices
are about actual facts, not about which skills ran. Pure routers and read-only
exploration do not fabricate a choice. Existing historical records are not
renamed or merged to satisfy this lifecycle.

## Personal Process Memory

For this repository, the repository root is the explicitly selected personal
root. `/project/` is ignored by Git and contains:

```text
project/
├── roadmaps/
├── features/
├── issues/
├── knowledge/
└── handoffs/
```

These files are local process artifacts. They must not be committed or treated
as team source of truth. Promote a durable conclusion only when future
contributors need it, and only to the applicable team-doc directories.

The live `project/handoffs/current-work-state.md` file is also personal process
memory. It tracks one active work item, its freshness fingerprint, and the
context manifest for `rs-continue` / `rs-finish-work`, but it never becomes a
team task platform or team journal.

It remains the only live active-work state. Timestamped snapshots are transfer
artifacts, not a second state schema or a persistent workflow journal.

Roadmap, feature, issue, and handoff personal records should use the shared
lightweight header: `id` reuses the canonical slug or file stem, and
`backlinks` lists stable related docs or records. Do not rename old files just
to backfill the header.

`project/knowledge/` is an optional raw evidence or standalone learning area,
not a second process record for a feature, issue, or roadmap. For an active work
item, prefer the one process record and link to a knowledge note only when the
note is independently reusable or explicitly requested.

## Adoption History

On 2026-07-10, the repository was audited with `rs-onboard`. Legacy documents
were routed into the five owner directories, and tracked snapshots from the
root `handoff/` directory were preserved under local `project/handoffs/`.

## Lightweight Checks

```bash
find docs -mindepth 1 -maxdepth 1 -type d -print | sort
git check-ignore -q project/handoffs
python3 skills/rs-handoff/scripts/generate_snapshot.py --self-test
python3 skills/rs-handoff/scripts/manage_work_state.py --self-test
git diff --check
```
