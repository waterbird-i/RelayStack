---
name: rs-handoff
description: Generate RelayStack handoff snapshots for AI coding work. Use when a person or agent needs to hand off current workspace state, changed files, project context, blockers, risks, next steps, and validation evidence to the next owner.
version: "0.1.0"
updated: 2026-06-24
---

# RS Handoff

Use this skill to turn the current workspace state into a verifiable handoff
snapshot. The snapshot is not a prettier chat summary; it must include real
local evidence another person or agent can use to continue the work.

## Workflow

1. Identify the manual handoff fields from the current conversation:
   - task name
   - current goal
   - current stage
   - owner
   - completed work
   - unfinished work
   - blocker
   - risk
   - risk trigger, impact, and mitigation when known
   - next step
   - next inputs and touched files when known
   - validation plan
   - relevant agent or sub-agent summaries
2. Run the bundled generator from the workspace root.
3. Report the generated `handoff/snapshot-<timestamp>.md` path.

```bash
python3 skills/rs-handoff/scripts/generate_snapshot.py \
  --task "任务名" \
  --goal "本轮目标" \
  --stage "当前阶段" \
  --owner "负责人" \
  --completed "已完成事项" \
  --unfinished "未完成事项" \
  --blocker "阻塞，没有则写未发现" \
  --risk "风险，没有则写未发现" \
  --risk-trigger "风险触发条件" \
  --risk-impact "风险影响" \
  --risk-mitigation "缓解动作" \
  --next-step "下一步动作" \
  --next-input "下一步输入" \
  --next-file "下一步触达文件" \
  --validation "验证方式" \
  --agent-summary "参与代理及结论" \
  --agent-record "path/to/worker-a.json" \
  --agent-record "path/to/reviewer-b.md"
```

## Rules

- Do not auto-commit, auto-edit project context stores, or create task management data.
- Do not fail when optional sources are missing. The snapshot should say `未发现`.
- Keep evidence local and cheap: git status, diff summary, changed files,
  recent commits, and project notes when present.
- Include enough manual context to answer why the current change exists.
- Include `Evidence Map`, `Risk Register`, and `Next Action Contract` so the
  next owner can trace claims, understand risk, and execute the next step.
- Use `--agent-record` for local Agent / task records. JSON and Markdown are
  supported; missing or invalid files should be rendered as warnings.
- When multiple records are provided, include `Agent 并行边界`: role, write
  scope, status, adoption, adopted output, rejected reason, explicit conflicts,
  verification, and overlapping write scopes.

## Validation

Run the generator self-check after changing the script:

```bash
python3 skills/rs-handoff/scripts/generate_snapshot.py --self-test
```
