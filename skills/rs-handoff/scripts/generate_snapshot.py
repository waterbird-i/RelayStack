#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


MISSING = "未发现"
NOT_PROVIDED = "未提供"


def run(command: list[str], cwd: Path) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return MISSING
    return result.stdout.strip() or MISSING


def git_root(cwd: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip())
    return cwd


def first_existing_branch(root: Path) -> str:
    return run(["git", "branch", "--show-current"], root)


def read_text(path: Path, max_chars: int = 2400) -> str:
    if not path.exists() or not path.is_file():
        return MISSING
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return MISSING
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "\n...（已截断）"


def project_files(root: Path, name: str) -> str:
    base = root / name
    if not base.exists():
        return MISSING
    files = sorted(
        str(path.relative_to(root))
        for path in base.rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    )
    return "\n".join(files) if files else MISSING


def status_files(status: str) -> list[str]:
    if status == MISSING:
        return []
    paths: list[str] = []
    for line in status.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[1]
        if path:
            paths.append(path)
    return paths


def unique_lines(*values: str, extra: list[str] | None = None) -> str:
    seen: set[str] = set()
    lines: list[str] = []
    for value in values:
        if value == MISSING:
            continue
        for line in value.splitlines():
            item = line.strip()
            if item and item not in seen:
                seen.add(item)
                lines.append(item)
    for item in extra or []:
        if item and item not in seen:
            seen.add(item)
            lines.append(item)
    return "\n".join(lines) if lines else MISSING


def bullet(items: list[str] | None) -> str:
    clean = [item.strip() for item in items or [] if item.strip()]
    if not clean:
        return f"- {MISSING}"
    return "\n".join(f"- {item}" for item in clean)


def code_block(value: str) -> str:
    if value == MISSING:
        return MISSING
    return f"```text\n{value}\n```"


@dataclass
class Evidence:
    root: Path
    branch: str
    log: str
    status: str
    diff_stat: str
    diff_names: str
    changed_files: str
    readme: str
    docs: str
    handoff: str
    skills: str


@dataclass
class AgentRecord:
    source: str
    agent: str
    role: str
    task: str
    input: str
    output: str
    conclusion: str
    adopted_output: str
    rejected_reason: str
    write_scope: list[str]
    status: str
    adoption: str
    conflicts: list[str]
    verification: list[str]
    warnings: list[str]


def collect_evidence(root: Path) -> Evidence:
    status = run(["git", "status", "--short"], root)
    diff_names = run(["git", "diff", "--name-only"], root)
    return Evidence(
        root=root,
        branch=first_existing_branch(root),
        log=run(["git", "log", "--oneline", "-n", "5"], root),
        status=status,
        diff_stat=run(["git", "diff", "--stat"], root),
        diff_names=diff_names,
        changed_files=unique_lines(diff_names, extra=status_files(status)),
        readme=read_text(root / "README.md"),
        docs=project_files(root, "docs"),
        handoff=project_files(root, "handoff"),
        skills=project_files(root, "skills"),
    )


def list_value(value: object) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return [str(value)]


def text_value(data: dict[str, object], key: str, default: str = MISSING) -> str:
    value = data.get(key)
    if value is None or value == "":
        return default
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value)


def record_from_data(data: dict[str, object], source_path: Path, warnings: list[str] | None = None) -> AgentRecord:
    return AgentRecord(
        source=text_value(data, "source", "agent-record"),
        agent=text_value(data, "agent", source_path.stem),
        role=text_value(data, "role", "unknown"),
        task=text_value(data, "task"),
        input=text_value(data, "input"),
        output=text_value(data, "output"),
        conclusion=text_value(data, "conclusion"),
        adopted_output=text_value(data, "adopted_output"),
        rejected_reason=text_value(data, "rejected_reason"),
        write_scope=list_value(data.get("write_scope")),
        status=text_value(data, "status", "unknown"),
        adoption=text_value(data, "adoption", "unknown"),
        conflicts=list_value(data.get("conflicts")),
        verification=list_value(data.get("verification")),
        warnings=warnings or [],
    )


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    meta: dict[str, object] = {}
    current_key: str | None = None
    for raw_line in text[4:end].splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line.startswith("  - ") and current_key:
            meta.setdefault(current_key, [])
            if isinstance(meta[current_key], list):
                meta[current_key].append(line[4:].strip())
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        current_key = key.strip()
        value = value.strip()
        if value == "[]":
            meta[current_key] = []
        elif value:
            meta[current_key] = value.strip("\"'")
        else:
            meta[current_key] = []
    return meta, text[end + 4 :].lstrip()


def markdown_section(body: str, heading: str) -> str:
    pattern = rf"(?ims)^#\s+{re.escape(heading)}\s*\n(.*?)(?=^#\s+|\Z)"
    match = re.search(pattern, body)
    if not match:
        return MISSING
    return match.group(1).strip() or MISSING


def parse_markdown_record(path: Path, text: str) -> AgentRecord:
    meta, body = parse_frontmatter(text)
    data = dict(meta)
    data.setdefault("task", markdown_section(body, "Task"))
    data.setdefault("output", markdown_section(body, "Output"))
    data.setdefault("conclusion", markdown_section(body, "Conclusion"))
    return record_from_data(data, path)


def parse_agent_record(path_text: str, root: Path) -> AgentRecord:
    path = Path(path_text)
    if not path.is_absolute():
        path = root / path
    if not path.exists() or not path.is_file():
        return record_from_data(
            {"agent": Path(path_text).stem, "source": "unknown"},
            path,
            [f"记录文件不存在：{path_text}"],
        )

    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if path.suffix.lower() == ".json":
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            return record_from_data(
                {"agent": path.stem, "source": "unknown"},
                path,
                [f"JSON 无法解析：{exc.msg}"],
            )
        if not isinstance(data, dict):
            return record_from_data(
                {"agent": path.stem, "source": "unknown"},
                path,
                ["JSON 顶层必须是对象"],
            )
        return record_from_data(data, path)

    return parse_markdown_record(path, text)


def collect_agent_records(paths: list[str], root: Path) -> list[AgentRecord]:
    return [parse_agent_record(path, root) for path in paths]


def agent_record_markdown(records: list[AgentRecord]) -> str:
    if not records:
        return MISSING
    chunks: list[str] = []
    for record in records:
        chunks.append(
            "\n".join(
                [
                    f"### {record.agent}",
                    f"- 来源：{record.source}",
                    f"- 角色：{record.role}",
                    f"- 状态：{record.status}",
                    f"- 采纳状态：{record.adoption}",
                    f"- 任务：{record.task}",
                    f"- 输入：{record.input}",
                    f"- 输出：{record.output}",
                    f"- 结论：{record.conclusion}",
                    f"- 已采纳输出：{record.adopted_output}",
                    f"- 未采纳原因：{record.rejected_reason}",
                    f"- 写入范围：{', '.join(record.write_scope) if record.write_scope else MISSING}",
                    f"- 冲突：{', '.join(record.conflicts) if record.conflicts else MISSING}",
                    f"- 验证：{', '.join(record.verification) if record.verification else MISSING}",
                    f"- 警告：{', '.join(record.warnings) if record.warnings else MISSING}",
                ]
            )
        )
    return "\n\n".join(chunks)


def overlapping_scopes(records: list[AgentRecord]) -> list[str]:
    owners: dict[str, list[str]] = {}
    for record in records:
        for scope in record.write_scope:
            owners.setdefault(scope, []).append(record.agent)
    conflicts: list[str] = []
    for scope, agents in sorted(owners.items()):
        unique_agents = sorted(set(agents))
        if len(unique_agents) > 1:
            conflicts.append(f"{scope}：{', '.join(unique_agents)}")
    return conflicts


def boundary_markdown(records: list[AgentRecord]) -> str:
    if not records:
        return MISSING

    lines: list[str] = []
    for record in records:
        lines.extend(
            [
                f"- Agent：{record.agent}",
                f"  - 职责：{record.role}",
                f"  - 写入范围：{', '.join(record.write_scope) if record.write_scope else MISSING}",
                f"  - 状态：{record.status}",
                f"  - 采纳状态：{record.adoption}",
                f"  - 已采纳输出：{record.adopted_output}",
                f"  - 未采纳原因：{record.rejected_reason}",
                f"  - 显式冲突：{', '.join(record.conflicts) if record.conflicts else MISSING}",
                f"  - 验证：{', '.join(record.verification) if record.verification else MISSING}",
            ]
        )

    scope_conflicts = overlapping_scopes(records)
    failed = [record.agent for record in records if record.status == "failed"]
    rejected = [record.agent for record in records if record.adoption == "rejected"]
    lines.extend(
        [
            "",
            f"- 潜在写入冲突：{', '.join(scope_conflicts) if scope_conflicts else MISSING}",
            f"- 失败记录观察项：{', '.join(failed) if failed else MISSING}",
            f"- 未采纳记录观察项：{', '.join(rejected) if rejected else MISSING}",
        ]
    )
    return "\n".join(lines)


def evidence_map_markdown(args: argparse.Namespace, evidence: Evidence, records: list[AgentRecord]) -> str:
    changed_source = "git diff --name-only + git status --short"
    docs_source = "docs/** + README.md + handoff/** + skills/**"
    agent_source = "--agent-record" if records else MISSING
    return "\n".join(
        [
            f"- 当前目标：{args.goal}",
            "  - 证据来源：用户输入 `--goal`",
            "  - 可信度：高" if args.goal != NOT_PROVIDED else "  - 可信度：未验证",
            f"- 当前阶段：{args.stage}",
            "  - 证据来源：用户输入 `--stage`",
            "  - 可信度：高" if args.stage != NOT_PROVIDED else "  - 可信度：未验证",
            f"- 主要改动文件：{evidence.changed_files}",
            f"  - 证据来源：{changed_source}",
            "  - 可信度：高" if evidence.changed_files != MISSING else "  - 可信度：未验证",
            f"- 项目上下文：{docs_source}",
            "  - 证据来源：本地文件系统",
            "  - 可信度：高",
            f"- Agent 记录：{agent_source}",
            "  - 证据来源：本地 agent record 文件" if records else "  - 证据来源：未发现",
            "  - 可信度：高" if records else "  - 可信度：未验证",
        ]
    )


def risk_register_markdown(args: argparse.Namespace) -> str:
    risk = args.risk or MISSING
    mitigation = args.risk_mitigation or args.next_step
    if risk == MISSING:
        mitigation = MISSING
    return "\n".join(
        [
            f"- 风险：{risk}",
            f"- 触发条件：{args.risk_trigger if risk != MISSING else MISSING}",
            f"- 影响：{args.risk_impact if risk != MISSING else MISSING}",
            f"- 缓解动作：{mitigation}",
        ]
    )


def next_action_contract_markdown(args: argparse.Namespace) -> str:
    return "\n".join(
        [
            f"- 下一步动作：{args.next_step}",
            f"- 输入：{', '.join(args.next_input) if args.next_input else NOT_PROVIDED}",
            f"- 触达文件：{', '.join(args.next_file) if args.next_file else NOT_PROVIDED}",
            f"- 验证命令：{args.validation}",
            f"- 完成标志：{args.done_when}",
        ]
    )


def render(args: argparse.Namespace, evidence: Evidence, agent_records: list[AgentRecord]) -> str:
    blocker = args.blocker or MISSING
    risk = args.risk or MISSING
    can_continue = "是" if blocker == MISSING else "需要处理阻塞"
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""# Handoff Snapshot: {args.task}

生成时间：{generated_at}

## 1. 当前目标
- 本轮目标：{args.goal}
- 当前阶段：{args.stage}
- 负责人：{args.owner}
- 是否可继续：{can_continue}

## 2. 工作区状态
- 工作区：`{evidence.root}`
- 分支：{evidence.branch}
- 最近提交：
{code_block(evidence.log)}
- 未提交变更：
{code_block(evidence.status)}
- diff 统计：
{code_block(evidence.diff_stat)}
- 主要改动文件：
{code_block(evidence.changed_files)}

## 3. 已完成
{bullet(args.completed)}

## 4. 未完成
{bullet(args.unfinished)}

## 5. 阻塞与风险
- 阻塞：{blocker}
- 风险：{risk}
- 需要用户确认：{args.needs_confirmation}

## 6. Evidence Map
{evidence_map_markdown(args, evidence, agent_records)}

## 7. Risk Register
{risk_register_markdown(args)}

## 8. Next Action Contract
{next_action_contract_markdown(args)}

## 9. 项目上下文
- README：
{code_block(evidence.readme)}
- docs：
{code_block(evidence.docs)}
- handoff：
{code_block(evidence.handoff)}
- skills：
{code_block(evidence.skills)}

## 10. Agent 交接信息
- 参与代理与结论：
{bullet(args.agent_summary)}
- Agent records：
{agent_record_markdown(agent_records)}
- 可复用发现：
{bullet(args.reusable_finding)}
- 修改原因：{args.why}

## 11. 下一步
1. 下一步动作：{args.next_step}
2. 验证方式：{args.validation}
3. 完成标志：{args.done_when}

## 12. 复现命令
```bash
git status --short
git diff --stat
git diff --name-only
git log --oneline -n 5
```

## 13. Agent 并行边界
{boundary_markdown(agent_records)}
"""


def write_snapshot(args: argparse.Namespace, root: Path) -> Path:
    evidence = collect_evidence(root)
    agent_records = collect_agent_records(args.agent_record, root)
    output_dir = root / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = args.timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    output = output_dir / f"snapshot-{timestamp}.md"
    output.write_text(render(args, evidence, agent_records), encoding="utf-8")
    return output


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate a RelayStack handoff snapshot.")
    p.add_argument("--task", default="当前任务")
    p.add_argument("--goal", default=NOT_PROVIDED)
    p.add_argument("--stage", default=NOT_PROVIDED)
    p.add_argument("--owner", default=NOT_PROVIDED)
    p.add_argument("--why", default=NOT_PROVIDED)
    p.add_argument("--next-step", default=NOT_PROVIDED)
    p.add_argument("--blocker", default=MISSING)
    p.add_argument("--risk", default=MISSING)
    p.add_argument("--risk-trigger", default=NOT_PROVIDED)
    p.add_argument("--risk-impact", default=NOT_PROVIDED)
    p.add_argument("--risk-mitigation", default=NOT_PROVIDED)
    p.add_argument("--needs-confirmation", default=MISSING)
    p.add_argument("--validation", default=NOT_PROVIDED)
    p.add_argument("--done-when", default=NOT_PROVIDED)
    p.add_argument("--next-input", action="append", default=[])
    p.add_argument("--next-file", action="append", default=[])
    p.add_argument("--completed", action="append", default=[])
    p.add_argument("--unfinished", action="append", default=[])
    p.add_argument("--agent-record", action="append", default=[])
    p.add_argument("--agent-summary", action="append", default=[])
    p.add_argument("--reusable-finding", action="append", default=[])
    p.add_argument("--output-dir", default="handoff")
    p.add_argument("--timestamp")
    p.add_argument("--self-test", action="store_true")
    return p


def self_test() -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        json_record = root / "worker-a.json"
        json_record.write_text(
            json.dumps(
                {
                    "source": "agent-record",
                    "agent": "worker_a",
                    "role": "worker",
                    "task": "实现 Agent record 输入",
                    "output": "新增 --agent-record",
                    "conclusion": "可以作为 handoff 证据",
                    "adopted_output": "保留 agent record schema",
                    "write_scope": ["skills/rs-handoff/scripts/generate_snapshot.py"],
                    "status": "completed",
                    "adoption": "adopted",
                    "verification": ["self-test"],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        md_record = root / "reviewer.md"
        md_record.write_text(
            """---
source: agent-record
agent: reviewer_a
role: reviewer
status: completed
adoption: reference
write_scope:
  - skills/rs-handoff/scripts/generate_snapshot.py
conflicts: []
verification:
  - read snapshot
---

# Task
审查快照内容。

# Output
确认 record 可进入快照。

# Conclusion
Markdown record 可解析。
""",
            encoding="utf-8",
        )
        args = parser().parse_args(
            [
                "--task",
                "测试任务",
                "--goal",
                "生成交接快照",
                "--stage",
                "自检",
                "--completed",
                "完成脚本渲染",
                "--next-step",
                "读取快照",
                "--validation",
                "检查必要章节",
                "--done-when",
                "snapshot 包含证据、风险和下一步契约",
                "--risk",
                "交接信息不完整",
                "--risk-trigger",
                "下一个 owner 只读 snapshot",
                "--risk-impact",
                "重复探索或误判状态",
                "--risk-mitigation",
                "为关键结论附证据来源",
                "--next-input",
                "snapshot-benchmark.md",
                "--next-file",
                "skills/rs-handoff/scripts/generate_snapshot.py",
                "--agent-record",
                str(json_record),
                "--agent-record",
                str(md_record),
                "--agent-record",
                "missing.json",
                "--timestamp",
                "20000101-000000",
            ]
        )
        output = write_snapshot(args, root)
        text = output.read_text(encoding="utf-8")
        assert output.name == "snapshot-20000101-000000.md"
        assert "# Handoff Snapshot: 测试任务" in text
        assert "## 2. 工作区状态" in text
        assert "## 6. Evidence Map" in text
        assert "## 7. Risk Register" in text
        assert "## 8. Next Action Contract" in text
        assert "## 9. 项目上下文" in text
        assert "git status --short" in text
        assert "完成脚本渲染" in text
        assert "为关键结论附证据来源" in text
        assert "snapshot 包含证据、风险和下一步契约" in text
        assert "worker_a" in text
        assert "reviewer_a" in text
        assert "记录文件不存在：missing.json" in text
        assert "已采纳输出" in text
        assert "## 13. Agent 并行边界" in text
        assert "潜在写入冲突" in text
        assert "reviewer_a, worker_a" in text


def main() -> int:
    args = parser().parse_args()
    if args.self_test:
        self_test()
        print("self-test ok")
        return 0
    root = git_root(Path.cwd())
    output = write_snapshot(args, root)
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
