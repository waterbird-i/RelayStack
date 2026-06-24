<p align="right">
  <a href="./README.md">English</a> | 简体中文
</p>

# RelayStack

RelayStack 是一个以 skill 形式落地的 AI 编程工作流增强层。
它通过 handoff snapshot 协议，把 agent 的工作变成可交接、可验证、可复用的证据。

它不是另一个 agent 编排层，也不是工作流平台。MVP 是一个 Codex 风格的 skill，用来把当前开发状态转换成 handoff snapshot，让另一个人或 agent 可以继续工作。

## 产品方向

> 让 AI agent 的工作可交接、可验证、可复用。

现代 AI 编程工具让 agent 更有能力，但团队仍然需要有边界、可追踪、可评审的交接。RelayStack 嵌入 AI 编程工作流，把当前协作状态转换成下一个 owner 可以直接行动的快照。

当前需求和 hackathon 叙事见 [docs/product-direction.md](docs/product-direction.md)。
创意简介见 [docs/creative-brief.md](docs/creative-brief.md)。

## MVP

构建一个 skill，而不是 CLI。

当前实现保留 handoff 作为主要演示路径，并补充两个围绕吸引子文档工作的轻量入口：

```text
skills/
├── rs-handoff/
│   ├── SKILL.md
│   └── scripts/generate_snapshot.py
├── rs-feat/
│   └── SKILL.md
└── rs-issue/
    └── SKILL.md
```

`rs-handoff` 会读取当前工作区上下文：

- Git 状态、已改文件、diff 摘要和最近提交
- 存在时读取项目 notes
- 可用时读取 agent task records 或对话上下文
- 手动交接字段，例如目标、下一步、阻塞点和 owner

它会写入：

```text
handoff/snapshot-<timestamp>.md
```

`rs-feat` 是开发新能力的入口。编码前先读项目吸引子文档；实现后只更新未来会复用的团队稳定事实。

`rs-issue` 是 issue 修复入口。详细根因过程优先沉淀到个人 project 目录；团队仓库只更新稳定的行为、设计、架构、backlog 和验证事实。

## 吸引子文档

RelayStack 不把 CodeStable 的 feature / issue 全过程记录搬进团队仓库。团队协作仓库只维护少量稳定 owner docs：

```text
docs/context/
docs/backlog/
docs/requirements/
docs/design/
docs/architecture/
```

这些目录只写稳定事实。brainstorm、临时 plan、子代理记录、详细 fix-note、验证草稿默认放个人 project 目录；需要换人接手时，再用 handoff snapshot 汇总。

## 成功指标

核心指标是 handoff success rate：

```text
handoff success rate = correctly answered handoff questions / total handoff questions
```

Demo 应该证明：一个新的人或新 agent 可以阅读 snapshot，并在 5 分钟内继续下一步。

## 范围保护

MVP 不包含 Web 应用、数据库、账号系统、实时协作、自动提交、任务管理或完整语义代码分析。

第一版应保持朴素：基于真实项目证据生成一份有用的 handoff snapshot。

## 运行 MVP

在工作区根目录执行：

```bash
python3 skills/rs-handoff/scripts/generate_snapshot.py \
  --task "RelayStack MVP" \
  --goal "Generate one useful handoff snapshot from real project evidence" \
  --stage "MVP implementation" \
  --next-step "Give the snapshot to the next owner" \
  --validation "Read the snapshot and answer the handoff questions"
```

可以附加可选的 Agent records：

```bash
python3 skills/rs-handoff/scripts/generate_snapshot.py \
  --agent-record path/to/worker-a.json \
  --agent-record path/to/reviewer-b.md
```

当附加多个 records 时，snapshot 会包含 `Agent 并行边界` 章节，记录写入范围、采纳状态、显式冲突、验证结果，以及文件范围重叠警告。
