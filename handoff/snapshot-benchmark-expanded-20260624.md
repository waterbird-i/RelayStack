# Handoff Snapshot: terminal-bench expanded benchmark

生成时间：2026-06-24 21:46:11

## 1. 当前目标
- 本轮目标：新增 20 道 terminal-bench 风格任务，并沉淀 A/B 盲评链路
- 当前阶段：本地题库、盲评采集和汇总闭环已完成；新增 20 题真实外部 A/B 执行待明确授权
- 负责人：codex
- 是否可继续：需要处理阻塞

## 2. 工作区状态
- 工作区：`/Users/liancong/Documents/RelayStack`
- 分支：main
- 最近提交：
```text
89c2954 Refine README for RelayStack handoff protocol
c0d2ede Document skill installation and update skill metadata
801b49b Add RelayStack workflow skill family
35b928f Add RelayStack routing skills
096aa4c Initial RelayStack skills
```
- 未提交变更：
```text
M runners/_runner.py
 M tasks/task-001/handoff.md
 D tasks/task-001/initial-repo/src/components/icode/Markdown/DevOpsMarkdown.tsx
 M tasks/task-001/instruction.md
 M tasks/task-001/test.sh
 M tasks/task-002/handoff.md
 D tasks/task-002/initial-repo/src/index.tsx
 D tasks/task-002/initial-repo/src/utils/comatemobile/url.ts
 M tasks/task-002/instruction.md
 M tasks/task-002/test.sh
 M tasks/task-003/handoff.md
 D tasks/task-003/initial-repo/src/mcp/Skills/SkillDetail/SquareDetail/QuickInstallDropdown.styles.ts
 D tasks/task-003/initial-repo/src/mcp/Skills/SkillDetail/SquareDetail/SkillHeaderActions.tsx
 M tasks/task-003/instruction.md
 M tasks/task-003/test.sh
 M tasks/task-004/handoff.md
 D tasks/task-004/initial-repo/src/mcp/Skills/SkillDetail/SquareDetail/SkillHeader.tsx
 D tasks/task-004/initial-repo/src/mcp/Skills/SkillDetail/SquareDetail/SkillHeaderActions.tsx
 M tasks/task-004/instruction.md
 M tasks/task-004/test.sh
 M tasks/task-005/handoff.md
 D tasks/task-005/initial-repo/src/components/icode/Markdown/index.tsx
 M tasks/task-005/instruction.md
 M tasks/task-005/test.sh
?? docs/dev/
?? handoff/snapshot-benchmark-expanded-20260624.md
?? reports/blind/
?? reports/no_handoff-real-20260624.jsonl
?? reports/rs_handoff-real-20260624.jsonl
?? scripts/add_benchmark_tasks.py
?? scripts/summarize_blind_benchmark.py
?? tasks/task-001/initial-repo/packages/
?? tasks/task-002/initial-repo/packages/
?? tasks/task-003/initial-repo/src/listParser.js
?? tasks/task-004/initial-repo/packages/
?? tasks/task-005/initial-repo/bin/
?? tasks/task-006/
?? tasks/task-007/
?? tasks/task-008/
?? tasks/task-009/
?? tasks/task-010/
?? tasks/task-011/
?? tasks/task-012/
?? tasks/task-013/
?? tasks/task-014/
?? tasks/task-015/
?? tasks/task-016/
?? tasks/task-017/
?? tasks/task-018/
?? tasks/task-019/
?? tasks/task-020/
?? tasks/task-021/
?? tasks/task-022/
?? tasks/task-023/
?? tasks/task-024/
?? tasks/task-025/
?? video/
```
- diff 统计：
```text
runners/_runner.py                                 | 185 ++++++++++++++++++++-
 tasks/task-001/handoff.md                          |   8 +-
 .../components/icode/Markdown/DevOpsMarkdown.tsx   |  19 ---
 tasks/task-001/instruction.md                      |  26 +--
 tasks/task-001/test.sh                             |  37 ++++-
 tasks/task-002/handoff.md                          |   8 +-
 tasks/task-002/initial-repo/src/index.tsx          |  10 --
 .../initial-repo/src/utils/comatemobile/url.ts     |  18 --
 tasks/task-002/instruction.md                      |  15 +-
 tasks/task-002/test.sh                             |  25 +--
 tasks/task-003/handoff.md                          |   8 +-
 .../SquareDetail/QuickInstallDropdown.styles.ts    |   5 -
 .../SquareDetail/SkillHeaderActions.tsx            |  20 ---
 tasks/task-003/instruction.md                      |  15 +-
 tasks/task-003/test.sh                             |  22 +--
 tasks/task-004/handoff.md                          |   7 +-
 .../SkillDetail/SquareDetail/SkillHeader.tsx       |  10 --
 .../SquareDetail/SkillHeaderActions.tsx            |  24 ---
 tasks/task-004/instruction.md                      |  14 +-
 tasks/task-004/test.sh                             |  18 +-
 tasks/task-005/handoff.md                          |   8 +-
 .../src/components/icode/Markdown/index.tsx        |  27 ---
 tasks/task-005/instruction.md                      |  15 +-
 tasks/task-005/test.sh                             |  14 +-
 24 files changed, 307 insertions(+), 251 deletions(-)
```
- 主要改动文件：
```text
runners/_runner.py
tasks/task-001/handoff.md
tasks/task-001/initial-repo/src/components/icode/Markdown/DevOpsMarkdown.tsx
tasks/task-001/instruction.md
tasks/task-001/test.sh
tasks/task-002/handoff.md
tasks/task-002/initial-repo/src/index.tsx
tasks/task-002/initial-repo/src/utils/comatemobile/url.ts
tasks/task-002/instruction.md
tasks/task-002/test.sh
tasks/task-003/handoff.md
tasks/task-003/initial-repo/src/mcp/Skills/SkillDetail/SquareDetail/QuickInstallDropdown.styles.ts
tasks/task-003/initial-repo/src/mcp/Skills/SkillDetail/SquareDetail/SkillHeaderActions.tsx
tasks/task-003/instruction.md
tasks/task-003/test.sh
tasks/task-004/handoff.md
tasks/task-004/initial-repo/src/mcp/Skills/SkillDetail/SquareDetail/SkillHeader.tsx
tasks/task-004/initial-repo/src/mcp/Skills/SkillDetail/SquareDetail/SkillHeaderActions.tsx
tasks/task-004/instruction.md
tasks/task-004/test.sh
tasks/task-005/handoff.md
tasks/task-005/initial-repo/src/components/icode/Markdown/index.tsx
tasks/task-005/instruction.md
tasks/task-005/test.sh
unners/_runner.py
docs/dev/
handoff/snapshot-benchmark-expanded-20260624.md
reports/blind/
reports/no_handoff-real-20260624.jsonl
reports/rs_handoff-real-20260624.jsonl
scripts/add_benchmark_tasks.py
scripts/summarize_blind_benchmark.py
tasks/task-001/initial-repo/packages/
tasks/task-002/initial-repo/packages/
tasks/task-003/initial-repo/src/listParser.js
tasks/task-004/initial-repo/packages/
tasks/task-005/initial-repo/bin/
tasks/task-006/
tasks/task-007/
tasks/task-008/
tasks/task-009/
tasks/task-010/
tasks/task-011/
tasks/task-012/
tasks/task-013/
tasks/task-014/
tasks/task-015/
tasks/task-016/
tasks/task-017/
tasks/task-018/
tasks/task-019/
tasks/task-020/
tasks/task-021/
tasks/task-022/
tasks/task-023/
tasks/task-024/
tasks/task-025/
video/
```

## 3. 已完成
- 已新增 tasks/task-006 到 task-025；已更新 docs/dev/benchmark-evaluation.md；已生成 reports/blind 基线盲评产物；已实现 runners/_runner.py --blind-dir 证据采集；已新增 scripts/summarize_blind_benchmark.py 并生成 reports/blind/final.generated.md；已修正新增题测试歧义和覆盖缺口

## 4. 未完成
- 尚未对新增 20 题执行 40 次外部 agent A/B 跑分；尚未基于新增 20 题真实 run 派 3 个 reviewer 重新盲评

## 5. 阻塞与风险
- 阻塞：外部 codex exec benchmark 执行会把本地 benchmark 任务内容与执行上下文交给外部模型服务处理，之前已被审批器拒绝；继续需要用户明确授权
- 风险：新增题目前已通过本地结构、语法、fail-before-fix、runner blind-dir smoke、JSON/whitespace/diff 检查；但没有新增 20 题真实 agent pass rate
- 需要用户确认：未发现

## 6. 项目上下文
- README：
```text
<p align="right">
  English | <a href="./README.zh-CN.md">简体中文</a>
</p>

# RelayStack

RelayStack is a skill-based handoff protocol for AI-assisted software work.
It turns scattered chat context, local Git evidence, project docs, and agent
records into a Markdown handoff snapshot the next person or agent can continue
from.

It is not an agent orchestrator, task tracker, web app, or workflow platform.
The first useful version is deliberately small: install a few repo-local
skills, run one snapshot generator, and prove that the next owner can keep
working without reading the whole previous session.

## Why It Exists

AI coding agents are good at doing work inside one session. Team delivery
breaks when that work has to move:

- decisions live in chat instead of the project
- changed files do not explain why they changed
- parallel agents can overlap without an explicit write boundary
- the next owner cannot see blockers, risks, or validation status
- project knowledge decays into repeated mistakes

RelayStack makes the handoff itself the product surface.

## Design Philosophy

The programmer is the in-loop owner of software delivery. They can treat parts
of the implementation as a black box, but they must keep control of intent,
boundaries, quality, and validation. When the system behaves strangely, they
must be able to dive deeper.

RelayStack is built around that stance:

- AI executes, but people own the software direction.
- Workflow artifacts should make decisions traceable, not replace judgment.
- Project docs should act as attractors for stable facts, not as a transcript
  of every messy step.
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

RelayStack uses a small set of owner docs as attractors for durable team truth:

```text
docs/context/
docs/backlog/
docs/requirements/
docs/design/
docs/architecture/
```

Temporary planning, he
...（已截断）
```
- docs：
```text
docs/architecture/README.md
docs/backlog/README.md
docs/context/README.md
docs/creative-brief.md
docs/design/README.md
docs/dev/benchmark-evaluation.md
docs/product-direction.md
docs/requirements/README.md
```
- handoff：
```text
handoff/snapshot-20260623-004625.md
handoff/snapshot-benchmark-expanded-20260624.md
```
- skills：
```text
skills/rs-arch/SKILL.md
skills/rs-brainstorm/SKILL.md
skills/rs-decide/SKILL.md
skills/rs-explore/SKILL.md
skills/rs-feat-accept/SKILL.md
skills/rs-feat-design/SKILL.md
skills/rs-feat-ff/SKILL.md
skills/rs-feat-impl/SKILL.md
skills/rs-feat/SKILL.md
skills/rs-guide/SKILL.md
skills/rs-handoff/SKILL.md
skills/rs-handoff/scripts/generate_snapshot.py
skills/rs-issue-analyze/SKILL.md
skills/rs-issue-fix/SKILL.md
skills/rs-issue-report/SKILL.md
skills/rs-issue/SKILL.md
skills/rs-learn/SKILL.md
skills/rs-libdoc/SKILL.md
skills/rs-onboard/SKILL.md
skills/rs-req/SKILL.md
skills/rs-roadmap/SKILL.md
skills/rs-trick/SKILL.md
skills/rs/SKILL.md
```

## 7. Agent 交接信息
- 参与代理与结论：
- 已按并行规范使用子代理完成题源探索、runner 约定复核、盲评方案设计、题目质量审查、盲评产物一致性审查；当前仅外部真实 A/B 运行需要用户授权
- Agent records：
未发现
- 可复用发现：
- 未发现
- 修改原因：未提供

## 8. 下一步
1. 下一步动作：用户明确授权外部 Codex/model 服务执行后，先用 --blind-dir 跑 task-006 smoke，再跑 task-006..025 的 no_handoff 与 rs_handoff 正式扩样，随后让 3 个 reviewer 读取 packets/debug-packets 打分，最后运行 scripts/summarize_blind_benchmark.py 输出 final.generated.md
2. 验证方式：python3 -m py_compile runners/_runner.py runners/no_handoff.py runners/rs_handoff.py scripts/add_benchmark_tasks.py scripts/summarize_blind_benchmark.py；bash -n tasks/task-{006..025}/test.sh；reports/blind JSON/泄露检查；python3 scripts/summarize_blind_benchmark.py reports/blind --output reports/blind/final.generated.md；git diff --check
3. 完成标志：未提供

## 9. 复现命令
```bash
git status --short
git diff --stat
git diff --name-only
git log --oneline -n 5
```

## 10. Agent 并行边界
未发现
