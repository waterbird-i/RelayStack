# RelayStack Product Direction

> Status: brainstormed direction
> Date: 2026-06-23
> Next step: split into a roadmap, then design the first skill

## 1. Positioning

RelayStack is an AI agent collaboration handoff protocol.

It should not be positioned as a generic multi-agent orchestration tool. The
hackathon story is sharper:

> RelayStack lets AI agents hand off work, not just finish tasks.

Superpower makes agents more capable. CodeStable gives capable agents memory,
boundaries, validation, and reviewability. RelayStack turns the current work
state into a handoff snapshot the next person or agent can continue from.

## 2. Problem

AI coding is no longer blocked by whether an agent can write code. The harder
team problem is handoff:

- Prompts, decisions, and assumptions are scattered across chat.
- Parallel agents can step on each other without clear boundaries.
- A new person or agent cannot tell why a change was made.
- Changed requirements do not clearly map back to affected decisions.
- A demo may run, but the team cannot prove how to validate or continue it.

RelayStack focuses on this gap:

> Make agent work handoff-ready, verifiable, and reusable.

## 3. MVP Shape

Build a skill, not a CLI.

The skill is invoked inside the agent workflow. It reads the current work state
and writes a Markdown handoff snapshot:

```text
handoff/snapshot-<timestamp>.md
```

The skill is useful when:

- A person wants another person to continue the work.
- A parent agent wants a new agent to take over.
- A hackathon team wants to prove what changed, why, and how to continue.
- A project needs lightweight evidence without building a workflow platform.

## 4. P0 Inputs

The skill should collect only cheap, local evidence:

- Current user-provided goal, next step, blocker, and owner
- `git status --short`
- `git diff --stat`
- `git diff --name-only`
- `git log --oneline -n 5`
- `docs/context/**`, if present
- `docs/backlog/**`, if present
- `docs/requirements/**`, if present
- `docs/design/**`, if present
- `docs/architecture/**`, if present
- Visible agent task records or sub-agent summaries, if the environment exposes them
- Personal project notes, if the user explicitly points to them

Missing sources should not fail the skill. The snapshot should say `未发现`.

## 5. P0 Output

The generated handoff snapshot should answer:

1. 当前目标是什么？
2. 当前做到哪一步？
3. 哪些文件被改过？
4. 为什么这样改？
5. 有哪些风险或阻塞？
6. 下一步做什么？
7. 怎么验证完成？

Suggested template:

````md
# Handoff Snapshot: <任务名>

## 1. 当前目标
- 本轮目标：
- 当前阶段：
- 是否可继续：

## 2. 工作区状态
- 分支：
- 最近提交：
- 未提交变更：
- 主要改动文件：

## 3. 已完成
- ...

## 4. 未完成
- ...

## 5. 阻塞与风险
- 阻塞：
- 风险：
- 需要用户确认：

## 6. Attractor Docs 上下文
- context：
- backlog：
- requirements：
- design：
- architecture：
- 关键注意事项：

## 7. Agent 交接信息
- 参与代理：
- 各代理结论：
- 可复用发现：

## 8. 下一步
1. 下一步动作
2. 验证方式
3. 完成标志

## 9. 复现命令
```bash
git status --short
git diff --stat
git diff --name-only
git log --oneline -n 5
```
````

## 6. Non-goals

The MVP should not include:

- Web UI
- Database
- Account or permission model
- Real-time collaboration
- Auto-committing Git changes
- Auto-editing personal process archives
- Full semantic code analysis
- Task management system
- Hard dependency on an LLM API

## 7. Demo

The strongest hackathon demo is a handoff test:

```text
Agent A or person A does the first half of a task.
  -> RelayStack skill generates a handoff snapshot.
  -> Agent B or person B only reads the snapshot.
  -> B continues the next step within 5 minutes.
```

3-minute narrative:

```text
0:00 - 0:30
AI coding is not only about writing faster. The breakage happens when context
has to move between agents or people.

0:30 - 1:10
Show the usual failure mode: chat history, diff, decisions, and validation are
scattered.

1:10 - 2:10
Invoke the RelayStack skill and generate a handoff snapshot.

2:10 - 2:45
A new agent reads only the snapshot, explains current state, and performs the
next small step.

2:45 - 3:00
Show the handoff score and close on verifiable agent delivery.
```

## 8. Success Metric

Primary metric:

```text
handoff success rate = correctly answered handoff questions / total handoff questions
```

This is stronger than generated lines of code, token count, or vague efficiency
claims. The product succeeds when the next owner can continue the work.

## 9. Biggest Risk

The biggest risk is being understood as a summary generator.

The product must keep the line clear:

> RelayStack does not generate prettier summaries. It proves whether AI work can
> be handed off and continued.

For the first version, boring evidence beats clever automation.
