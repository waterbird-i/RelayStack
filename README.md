<p align="right">
  English | <a href="./README.zh-CN.md">简体中文</a>
</p>

# RelayStack

RelayStack is a skill-based workflow enhancement layer for AI coding handoffs.
It uses a handoff snapshot protocol to make agent work transferable,
verifiable, and reusable.

It is not another agent orchestration layer or workflow platform. The MVP is a
Codex-style skill that turns the current development state into a handoff
snapshot another person or agent can use to continue the work.

## Product Direction

> Make AI agent work handoff-ready, verifiable, and reusable.

Modern AI coding tools make agents more capable, but teams still need bounded,
traceable, and reviewable handoffs. RelayStack sits inside the AI coding
workflow and turns the current collaboration state into a snapshot the next
owner can act on.

See [docs/product-direction.md](docs/product-direction.md) for the current
requirements and hackathon narrative.
See [docs/creative-brief.md](docs/creative-brief.md) for the Chinese creative
brief.

## MVP

Build a skill, not a CLI.

Current implementation keeps handoff as the main demo path and adds small
workflow entry skills around attractor docs:

```text
skills/
├── rs/
│   └── SKILL.md
├── rs-onboard/
│   └── SKILL.md
├── rs-brainstorm/
│   └── SKILL.md
├── rs-req/
│   └── SKILL.md
├── rs-arch/
│   └── SKILL.md
├── rs-roadmap/
│   └── SKILL.md
├── rs-explore/
│   └── SKILL.md
├── rs-learn/
│   └── SKILL.md
├── rs-trick/
│   └── SKILL.md
├── rs-decide/
│   └── SKILL.md
├── rs-guide/
│   └── SKILL.md
├── rs-libdoc/
│   └── SKILL.md
├── rs-handoff/
│   ├── SKILL.md
│   └── scripts/generate_snapshot.py
├── rs-feat/
│   └── SKILL.md
├── rs-feat-design/
│   └── SKILL.md
├── rs-feat-impl/
│   └── SKILL.md
├── rs-feat-accept/
│   └── SKILL.md
├── rs-feat-ff/
│   └── SKILL.md
├── rs-issue-report/
│   └── SKILL.md
├── rs-issue-analyze/
│   └── SKILL.md
├── rs-issue-fix/
│   └── SKILL.md
└── rs-issue/
    └── SKILL.md
```

`rs` is the root entry. Use it when you are not sure which RelayStack skill
should handle a request.

`rs-onboard` connects a repository to the attractor doc layout.

`rs-req`, `rs-arch`, and `rs-roadmap` maintain requirements, architecture, and
large-work planning without copying CodeStable's full process archive into the
team repository.

`rs-brainstorm` handles unclear ideas. `rs-feat-*` and `rs-issue-*` provide
stage-specific feature and issue workflows. `rs-learn`, `rs-trick`,
`rs-decide`, `rs-explore`, `rs-guide`, and `rs-libdoc` capture durable lessons,
recipes, decisions, evidence, and public docs only when they belong in the
attractor docs.

`rs-handoff` reads the current workspace context:

- Git status, changed files, diff summary, and recent commits
- Project notes when present
- Agent task records or conversation context when available
- Manual handoff fields such as goal, next step, blocker, and owner

It writes:

```text
handoff/snapshot-<timestamp>.md
```

`rs-feat` is the entry point for new capabilities. Before coding, it
reads the project attractor docs and, after implementation, updates only the
durable team truth that future sessions must reuse.

`rs-issue` is the entry point for issue work. It keeps detailed
root-cause process notes in a personal project area when available, while
updating team docs only with stable behavior, design, architecture, backlog, and
verification facts.

## Attractor Docs

RelayStack should not copy CodeStable's full per-feature and per-issue process
archive into a team repository. Team collaboration should keep converging on a
small set of durable owner docs:

```text
docs/context/
docs/backlog/
docs/requirements/
docs/design/
docs/architecture/
```

Use these for stable facts. Keep brainstorming, temporary plans, sub-agent
records, detailed fix notes, and scratch validation in a personal project area
or in a handoff snapshot when the work needs to move to another owner.

## Success Metric

The primary metric is handoff success rate:

```text
handoff success rate = correctly answered handoff questions / total handoff questions
```

The demo should prove that a new person or new agent can read the snapshot and
continue the next step within 5 minutes.

## Scope Guard

MVP does not include a web app, database, account system, real-time
collaboration, auto-commit, task management, or full semantic code analysis.

The first version should stay boring: generate one useful handoff snapshot from
real project evidence.

## Install Skills

Interactive install lets users choose specific skills or enter `all` to install
everything:

```bash
python3 scripts/install_skills.py
```

Common non-interactive commands:

```bash
# Install all skills into $CODEX_HOME/skills or ~/.codex/skills
python3 scripts/install_skills.py --all

# Install by index. Use --list first to inspect ordering.
python3 scripts/install_skills.py --list
python3 scripts/install_skills.py --select 1,3-5
```

Existing target skill folders are skipped by default. Use `--force` to replace
them.

## Run the MVP

From the workspace root:

```bash
python3 skills/rs-handoff/scripts/generate_snapshot.py \
  --task "RelayStack MVP" \
  --goal "Generate one useful handoff snapshot from real project evidence" \
  --stage "MVP implementation" \
  --next-step "Give the snapshot to the next owner" \
  --validation "Read the snapshot and answer the handoff questions"
```

Optional Agent records can be attached:

```bash
python3 skills/rs-handoff/scripts/generate_snapshot.py \
  --agent-record path/to/worker-a.json \
  --agent-record path/to/reviewer-b.md
```

When multiple records are attached, the snapshot includes an `Agent 并行边界`
section with write scopes, adoption state, explicit conflicts, verification, and
overlapping file-scope warnings.
