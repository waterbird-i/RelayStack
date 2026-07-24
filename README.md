<p align="right">
  English | <a href="./README.zh-CN.md">简体中文</a>
</p>

# RelayStack

![RelayStack project introduction](reports/assets/relaystack-intro.png)

[Watch the RelayStack introduction video](reports/assets/relaystack-intro.mp4)

RelayStack is a Codex plugin that provides evidence-driven project workflows
and handoff skills for AI-assisted software work. It turns chat context, local
Git evidence, project docs, and agent records into a Markdown snapshot that the
next person or agent can use without reading the whole previous session.

It is not an agent orchestrator, task tracker, web app, or workflow platform.
The first useful version stays small: install one plugin, use its skill group,
run one snapshot generator, and make the next handoff usable.

## Why It Exists

AI coding agents are good at doing work inside one session. Team delivery
breaks when that work has to move:

- decisions live in chat instead of the project
- changed files do not explain why they changed
- parallel agents can overlap without an explicit write boundary
- the next owner cannot see blockers, risks, or validation status
- project knowledge decays into repeated mistakes

RelayStack focuses on the handoff: what changed, why it changed, what is risky,
and how the next owner should continue.

## Design Philosophy

The person responsible for the software stays in the loop. They can let an
agent handle parts of the implementation, but they still own intent,
boundaries, quality, and validation. If the system behaves strangely, they need
enough evidence to inspect it.

RelayStack keeps that boundary explicit:

- AI executes, but people own the software direction.
- Workflow artifacts should make decisions traceable, not replace judgment.
- Project docs should hold stable facts, not every messy step.
- Handoffs should preserve evidence, risks, and next actions.
- The smallest durable project memory is better than a large process archive
  nobody reads.

## How It Works

```text
current workspace evidence
├── live current-work-state: the only active state, when continuation needs it
│   └── id/work id, stage, owner, next action, fingerprint, context manifest
├── local Git evidence: status, diff summary, changed files, recent commits
├── related owner docs only: context first, then the touched owner scope
└── optional agent records: worker notes, reviewer notes, conflict notes
    ↓ rs-handoff
<personal-root>/project/handoffs/snapshot-<timestamp>.md (read-only transfer artifact)
    ↓
rs-continue validates the snapshot, claims the live state, and updates that one
state; rs-finish-work closes it
```

The only team-maintained project-document categories are:

```text
docs/context/
docs/backlog/
docs/requirements/
docs/design/
docs/architecture/
```

`docs/context/` is the mandatory project-wide entry point. `docs/backlog/`,
`docs/requirements/`, `docs/design/`, and `docs/architecture/` are lazy:
read or create them only when a task produces a durable fact in their scope. A
missing optional owner directory is not an onboarding failure. The owner
triggers are `context` for project-wide rules, `backlog` for ongoing team
coordination, `requirements` for reusable
user-observable capability contracts, `design` for approval-worthy
pre-implementation choices, and `architecture` for implemented technical
boundaries.

Roadmaps, optional feature and issue process records, raw knowledge, and handoff
snapshots are personal records under `<personal-root>/project/`, not
team-maintained project documentation. In this repository, the repository root
is the personal root and `/project/` is ignored by Git. A multi-stage work item
may use at most one process record; one-turn work defaults to no record. The
formal feature design is never stored in the personal record:

```text
<personal-root>/project/
├── roadmaps/
├── features/
├── issues/
├── knowledge/
└── handoffs/
```

`docs/backlog/` may hold team-visible priorities and next steps, but roadmap
prose stays personal. A formal feature design is required only when the work
has an approval-worthy behavior, state, permission, migration, terminology, or
cross-module contract decision. When required, it lives at
`docs/design/{slug}.md` and is the authoritative implementation and acceptance
input; a personal feature record cannot replace it. Clear, bounded, low-risk
work may proceed without a design.

Skill invocation alone does not require a `docs/` update. Each durable fact has
one canonical owner; other documents link to that owner instead of copying the
fact. Update multiple owners only when multiple distinct facts or contracts
changed. Formal acceptance is always reported, including when no team doc is
updated.

When a multi-stage work item needs personal memory, use at most one process
record:
`project/features/{slug}.md`, `project/issues/{slug}.md`, or
`project/roadmaps/{slug}.md`. Issue evidence may append Report, Analysis, Fix,
and Verification sections to that same record, but none of those sections is a
mandatory stage. Use the shared `id` / `backlinks` header and do not rename
historical files just to backfill it. One-turn work needs no process record by
default. `project/knowledge/` is reserved for standalone raw evidence or
explicitly requested reusable notes; it is not a second process record for the
same work item.

Temporary plans, process notes, and agent scratch work stay out of the team
repository until they become stable facts. When the work moves, put process
evidence and next actions into a handoff snapshot.

## Design Entities

| Entity | Purpose |
|---|---|
| Context | Stable project rules, source-of-truth notes, and local conventions |
| Backlog | Prioritized work and next actions |
| Requirements | Capability goals, user-visible behavior, and product constraints |
| Design | Feature behavior, owner docs, and implementation-facing decisions |
| Architecture | Current technical structure, boundaries, and integration points |
| Roadmap | Decomposition for work too large for one feature pass |
| Feature | A staged path for designing, implementing, and accepting new capability |
| Issue | An optional evidence and fix path for broken behavior |
| Knowledge | Reusable lessons, recipes, decisions, and code exploration evidence |
| Handoff Snapshot | The transfer artifact that lets the next owner continue safely |
| Current Work State | The live personal state for one active work item |

## Workflows

```text
adopt repo       rs-onboard
fuzzy idea       rs-brainstorm → rs-feat / rs-roadmap
large work       rs-roadmap → smaller feature passes
new capability   rs-feat → rs-feat-ff or rs-feat-design → rs-feat-impl → rs-feat-accept
fast feature     rs-feat-ff
broken behavior  rs-issue (report/analyze/fix helpers only when needed)
knowledge        rs-learn / rs-trick / rs-decide / rs-explore
public docs      rs-guide / rs-libdoc
handoff          rs-handoff
continue work    rs-continue
finish work      rs-finish-work
```

## Handoff Snapshot

`rs-handoff` generates:

```text
<personal-root>/project/handoffs/snapshot-<timestamp>.md
```

The snapshot answers:

1. What is the current goal?
2. What has already been done?
3. Which files changed?
4. Why did the work move this way?
5. What is blocked or risky?
6. What should happen next?
7. How should the next owner validate completion?

It also carries three small quality contracts:

- `Evidence Map`: ties key claims to local sources such as Git evidence,
  project docs, user input, and agent records.
- `Risk Register`: records the risk, trigger, impact, and mitigation instead
  of a vague warning.
- `Next Action Contract`: names the next action, inputs, touched files,
  validation command, and done signal.

The top of each snapshot also includes a machine-readable quality block: missing
handoff questions, Evidence Map coverage, Next Action Contract completeness, and
the current Git evidence fingerprint. Use `scripts/check_snapshot_freshness.py`
to detect whether the workspace diff changed after snapshot generation.

When machine-consumable continuation is needed, the one live
current-work-state carries its `context manifest` so the next owner can read
only the docs, code, and evidence this round needs. A snapshot can still be
generated without creating live state. `rs-continue` validates the snapshot and
then consumes only an active state with a non-empty manifest; it claims the next
step and rewrites that one state. `rs-finish-work` closes the live state and
leaves the next step as handoff or knowledge sediment.

When multiple agent records are attached, the snapshot also includes an
`Agent parallel boundary` section: write scopes, adoption state, conflicts,
validation, and overlapping file-scope warnings.

Agent records can be JSON or Markdown frontmatter. Useful fields:

```json
{
  "agent": "worker_a",
  "role": "worker",
  "task": "Implement the snapshot contract",
  "write_scope": ["skills/rs-handoff/scripts/generate_snapshot.py"],
  "status": "completed",
  "adoption": "accepted",
  "adopted_output": "Evidence Map was kept",
  "rejected_reason": "No workflow engine added",
  "conflicts": [],
  "verification": ["self-test"]
}
```

The JSON AgentRecord contract lives at `schemas/agent-record.schema.json`.

## Quick Start

RelayStack is distributed through the
[RelayStack Marketplace](https://github.com/waterbird-i/relaystack-marketplace).
Add the marketplace once, then install the plugin:

```bash
codex plugin marketplace add waterbird-i/relaystack-marketplace
codex plugin add relaystack@relaystack
```

Confirm that Codex reports `relaystack@relaystack` as `installed, enabled`:

```bash
codex plugin list
```

Restart Codex or open a new task after installation. The plugin exposes the
complete `rs-*` skill group.

For local plugin development, install the repository as a local plugin in
Codex. The repository validator is available for source-checkout development:

```bash
python3 scripts/validate_plugin.py
```

Older environments that cannot load plugins can use the compatibility copier,
but this installs individual skills rather than the RelayStack plugin:

```bash
python3 scripts/install_skills.py --all
```

In Codex, use `rs` when you are not sure which RelayStack skill fits. Use
`rs-handoff` when you want a handoff snapshot for the current workspace.

The Python commands below are source-checkout commands for manual use, CI, and
debugging. They are not the normal agent-facing entry point.

Generate a snapshot manually from the workspace root:

```bash
python3 skills/rs-handoff/scripts/generate_snapshot.py \
  --task "RelayStack MVP" \
  --goal "Generate one useful handoff snapshot from real project evidence" \
  --stage "MVP implementation" \
  --owner "current agent" \
  --next-step "Give the snapshot to the next owner" \
  --validation "Read the snapshot and answer the handoff questions"
```

`--personal-root` writes to `<personal-root>/project/handoffs`. It may equal the
repository root because `/project/` is ignored by Git; other repository-local
personal roots are rejected. An explicit `--output-dir` remains available for
compatibility, but it must resolve outside the repository. When neither option
is provided, the command uses the current project root and writes under its
ignored `/project/handoffs/` directory.

Attach optional agent records:

```bash
python3 skills/rs-handoff/scripts/generate_snapshot.py \
  --agent-record path/to/worker-a.json \
  --agent-record path/to/reviewer-b.md
```

Useful checks:

```bash
python3 scripts/install_skills.py --self-test
python3 scripts/validate_plugin.py
python3 skills/rs-handoff/scripts/generate_snapshot.py --self-test
python3 skills/rs-handoff/scripts/manage_work_state.py --self-test
```

## Skill Overview

Use `rs` when you are not sure which RelayStack skill should handle a request.
It routes to the smallest useful entry point.

| Group | Skill | Purpose |
|---|---|---|
| Adoption | `rs-onboard` | Adopt the owner-doc layout in a new or existing repository |
| Requirements & Architecture | `rs-req` | Capture or update stable capability requirements |
|  | `rs-arch` | Backfill, update, or check architecture docs |
| Roadmap | `rs-roadmap` | Split a large goal into smaller feature passes |
| Discussion Entry | `rs-brainstorm` | Triage a fuzzy idea into design, feature, or roadmap work |
| Feature Flow | `rs-feat` | Entry point for new capability work |
|  | `rs-feat-design` | Create the formal team-owned design under `docs/design/` |
|  | `rs-feat-impl` | Implement from the approved team design |
|  | `rs-feat-accept` | Verify the implementation and make one documentation decision when durable facts changed |
|  | `rs-feat-ff` | Fast path for tiny clear features |
| Issue Flow | `rs-issue` | Entry point for broken behavior |
|  | `rs-issue-report` | Optional: record structured reproduction evidence |
|  | `rs-issue-analyze` | Optional: diagnose an unclear or risky root cause |
|  | `rs-issue-fix` | Apply a confirmed fix and make one documentation decision |
| Knowledge | `rs-learn` | Capture reusable lessons from work already done |
|  | `rs-trick` | Capture reusable coding recipes or library usage |
|  | `rs-decide` | Record settled technical decisions and long-term constraints |
| Exploration & Docs | `rs-explore` | Preserve focused code exploration evidence |
|  | `rs-guide` / `rs-libdoc` | Write task-oriented guides or API/reference docs |
| Handoff | `rs-handoff` | Generate a snapshot for the next person or agent |
|  | `rs-continue` | Consume a fresh snapshot and claim the one active state |
|  | `rs-finish-work` | Close the one active state after verification |

## Compared With

| Tool | Best at | RelayStack differs by |
|---|---|---|
| Superpower | Expanding what an agent can do through skills and reusable capabilities | Adding a handoff contract around the work: evidence, boundaries, risks, next step, and validation |
| Trellis | Keeping a structured project workspace with specs, tasks, workflow notes, and continuity logs | Staying smaller: a few stable owner docs plus one snapshot artifact, without becoming a task system |
| OpenSpec | Driving changes from explicit specs | Treating specs as one input, then packaging the current work state so another owner can continue safely |

Use Superpower when the agent needs more capability. Use Trellis when the team
wants a broader workspace convention. Use OpenSpec when the main gap is
spec-first change definition. Use RelayStack when the main gap is handoff:
what changed, why, what is risky, and how the next owner continues.

## Continuation Cost

![RelayStack continuation cost chart](reports/blind-expanded-20260625/assets/continuation-cost-dials.svg)

Across the current 25-task benchmark, RelayStack handoff reduced elapsed time
by `24.1%` and reported tokens by `23.0%`. On the 20-task expanded blind
review, `rs_handoff` won `53/60` reviewer decisions and reduced repeated
known-info exploration from `4` to `0`. Pass rate remains supporting evidence:
`92.0%` without handoff versus `96.0%` with handoff.

The benchmark measures a narrow slice:

- `elapsed_seconds`: total continuation time through `test.sh`
- `total_tokens` / `cost_usd`: reported model usage when available
- `repeated_known_info` / `repeated_known_files`: whether the agent reopened
  facts already present in the handoff
- `continuation_success`: whether the task test passed
- `handoff_question_score`: optional 0-7 score for the seven handoff questions

### Authoritative A/B Smoke Tests

![RelayStack project skills A/B summary](reports/multi-swe-project-skills-20260629/assets/project-skills-ab-dials.svg)

Two Multi-SWE-bench flash smoke runs now separate the original local 25-task
suite from a third-party authoritative issue-fixing source:

- `reports/multi-swe-clean-20260629`: clean baseline versus `rs-handoff` only.
  Both groups produced the same patch; handoff used `306,137` tokens versus
  `992,884` for baseline and finished `35.830s` faster.
- `reports/multi-swe-project-skills-20260629`: clean baseline versus
  repo-local RelayStack skills only. The handoff run used `rs-handoff` and
  `rs-issue-fix`, with no global/plugin skills and no subagents. It used
  `280,621` tokens versus `822,230` for baseline, finished `64.927s` faster,
  started `16` fewer commands, and produced a `451` byte smaller patch.

These runs are protocol-isolated smoke tests, not leaderboard claims. The
project-skills run also completed the official Multi-SWE-bench harness:
`baseline 1/1 resolved` and `relaystack_handoff 1/1 resolved`.

The expanded six-sample Multi-SWE-bench run is recorded in
`reports/multi-swe-six-20260710`: both groups completed `6/6` official harness
instances with `0` harness errors. Baseline resolved `3/6`; RelayStack handoff
resolved `2/6`. Agent execution time was `2114.644s` for baseline and
`1880.211s` for handoff. Use `reports/multi-swe-six-20260710/strata-summary.json`
for the language / repo / task-type split.

A demo succeeds when a new person or agent can read only the snapshot and
continue within 5 minutes.

## Scope Guard

RelayStack does not include a web UI, database, account system, real-time
collaboration, auto-commit, task management, full semantic code analysis, or a
hard dependency on an LLM API.

Add platform pieces only when one useful snapshot is no longer enough.
