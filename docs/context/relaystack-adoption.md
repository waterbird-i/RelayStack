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

- `docs/context/` records operating rules, verification, and contribution facts.
- `docs/backlog/` records prioritized team-visible next actions.
- `docs/requirements/` records stable capability goals and constraints.
- `docs/design/` records approved behavior and feature design.
- `docs/architecture/` records current technical structure and boundaries.

Do not add another project-document category under `docs/`. Route a document to
one of these owners or keep it as personal process memory.

## Documentation Trigger

Invoking a RelayStack skill does not automatically require a team-doc update.
At the end of the work, determine whether it produced durable facts that future
contributors need. The correct result may be:

- no `docs/` change when no durable team fact changed;
- one owner-doc change when the fact has one clear owner; or
- multiple owner-doc changes when the work genuinely changes several contracts.

Do not create placeholder entries or touch all five directories merely to prove
that documentation was considered. Documentation-specific requests routed to
skills such as `rs-req`, `rs-arch`, `rs-guide`, or `rs-libdoc` are different:
the requested document is their deliverable.

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

These files are local process records. They must not be committed or treated as
team source of truth. Promote a durable conclusion only when future contributors
need it, and only to the applicable team-doc directories.

## Adoption History

On 2026-07-10, the repository was audited with `rs-onboard`. Legacy documents
were routed into the five owner directories, and tracked snapshots from the
root `handoff/` directory were preserved under local `project/handoffs/`.

## Lightweight Checks

```bash
find docs -mindepth 1 -maxdepth 1 -type d -print | sort
git check-ignore -q project/handoffs
python3 skills/rs-handoff/scripts/generate_snapshot.py --self-test
git diff --check
```
