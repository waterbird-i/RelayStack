<p align="right">
  English | <a href="./README.zh-CN.md">简体中文</a>
</p>

# RelayStack

![RelayStack project introduction](reports/assets/relaystack-intro.png)

[Watch the RelayStack introduction video](reports/assets/relaystack-intro.mp4)

RelayStack is a repo-local skill set and handoff protocol for AI-assisted
software work. It turns chat context, local Git evidence, project docs, and
agent records into a Markdown snapshot that the next person or agent can use
without reading the whole previous session.

It is not an agent orchestrator, task tracker, web app, or workflow platform.
The first useful version stays small: install a few repo-local skills, run one
snapshot generator, and make the next handoff usable.

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
current work state
├── manual fields: goal, stage, owner, blocker, risk, next step
├── local Git evidence: status, diff summary, changed files, recent commits
├── stable project docs: context, backlog, requirements, design, architecture
└── optional agent records: worker notes, reviewer notes, conflict notes
    ↓
handoff/snapshot-<timestamp>.md
    ↓
next person or agent continues the work
```

RelayStack uses a small set of owner docs for facts that should survive the
current session:

```text
docs/context/
docs/backlog/
docs/requirements/
docs/design/
docs/architecture/
```

Temporary plans, process notes, and agent scratch work stay out of the team
repository until they become stable facts. When the work moves, put the useful
parts into a handoff snapshot.

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
| Issue | A root-cause path for reporting, analyzing, and fixing broken behavior |
| Knowledge | Reusable lessons, recipes, decisions, and code exploration evidence |
| Handoff Snapshot | The transfer artifact that lets the next owner continue safely |

## Workflows

```text
adopt repo       rs-onboard
fuzzy idea       rs-brainstorm → rs-feat / rs-roadmap
large work       rs-roadmap → smaller feature passes
new capability   rs-feat → rs-feat-design → rs-feat-impl → rs-feat-accept
fast feature     rs-feat-ff
broken behavior  rs-issue-report → rs-issue-analyze → rs-issue-fix
knowledge        rs-learn / rs-trick / rs-decide / rs-explore
public docs      rs-guide / rs-libdoc
handoff          rs-handoff
```

## Handoff Snapshot

`rs-handoff` generates:

```text
handoff/snapshot-<timestamp>.md
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

## Quick Start

RelayStack is used through repo-local skills. Install them into
`$CODEX_HOME/skills` or `~/.codex/skills`:

```bash
python3 scripts/install_skills.py --all
```

In Codex, use `rs` when you are not sure which RelayStack skill fits. Use
`rs-handoff` when you want a handoff snapshot for the current workspace.

The Python commands below are the underlying scripts for manual use, CI, and
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

Attach optional agent records:

```bash
python3 skills/rs-handoff/scripts/generate_snapshot.py \
  --agent-record path/to/worker-a.json \
  --agent-record path/to/reviewer-b.md
```

Useful checks:

```bash
python3 scripts/install_skills.py --self-test
python3 skills/rs-handoff/scripts/generate_snapshot.py --self-test
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
|  | `rs-feat-design` | Draft the design that later implementation should follow |
|  | `rs-feat-impl` | Implement according to the approved design order |
|  | `rs-feat-accept` | Check the implementation against design and update durable docs |
|  | `rs-feat-ff` | Fast path for tiny clear features |
| Issue Flow | `rs-issue` | Entry point for broken behavior |
|  | `rs-issue-report` | Turn a suspected bug into a reproducible report |
|  | `rs-issue-analyze` | Find root cause, assess risk, and propose a fix |
|  | `rs-issue-fix` | Apply a confirmed fix and record validation |
| Knowledge | `rs-learn` | Capture reusable lessons from work already done |
|  | `rs-trick` | Capture reusable coding recipes or library usage |
|  | `rs-decide` | Record settled technical decisions and long-term constraints |
| Exploration & Docs | `rs-explore` | Preserve focused code exploration evidence |
|  | `rs-guide` / `rs-libdoc` | Write task-oriented guides or API/reference docs |
| Handoff | `rs-handoff` | Generate a snapshot for the next person or agent |

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

A demo succeeds when a new person or agent can read only the snapshot and
continue within 5 minutes.

## Scope Guard

RelayStack does not include a web UI, database, account system, real-time
collaboration, auto-commit, task management, full semantic code analysis, or a
hard dependency on an LLM API.

Add platform pieces only when one useful snapshot is no longer enough.
