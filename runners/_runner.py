#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "reports" / "results.jsonl"
GENERATOR = ROOT / "skills" / "rs-handoff" / "scripts" / "generate_snapshot.py"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def run(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def run_shell(command: str, cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def copy_initial_repo(task_dir: Path, workdir: Path) -> None:
    initial_repo = task_dir / "initial-repo"
    if not initial_repo.is_dir():
        raise SystemExit(f"missing initial repo: {initial_repo}")
    shutil.copytree(initial_repo, workdir, dirs_exist_ok=True)


def ensure_git_repo(workdir: Path) -> None:
    if not (workdir / ".git").exists():
        run(["git", "init", "-q"], workdir)


def make_handoff(task_dir: Path, workdir: Path) -> Path:
    ensure_git_repo(workdir)
    handoff_note = read_text(task_dir / "handoff.md").strip() or "未提供"
    result = run(
        [
            sys.executable,
            str(GENERATOR),
            "--task",
            task_dir.name,
            "--goal",
            read_text(task_dir / "instruction.md").splitlines()[0].lstrip("# ").strip(),
            "--stage",
            "接手执行",
            "--owner",
            "benchmark-rs-handoff",
            "--completed",
            handoff_note,
            "--next-step",
            "按 instruction.md 完成最小实现",
            "--validation",
            "bash test.sh",
            "--timestamp",
            "benchmark",
        ],
        workdir,
    )
    if result.returncode != 0:
        raise SystemExit(result.stdout)
    return workdir / "handoff" / "snapshot-benchmark.md"


def build_prompt(task_dir: Path, workdir: Path, runner_name: str) -> tuple[str, Path | None]:
    instruction = read_text(task_dir / "instruction.md")
    if runner_name == "no_handoff":
        return instruction, None

    snapshot = make_handoff(task_dir, workdir)
    task_handoff = read_text(task_dir / "handoff.md").strip()
    prompt = "\n\n".join(
        [
            "你是接手 agent。先读下面的 RelayStack handoff，再执行任务。",
            "不要重复探索 handoff 中已经明确给出的文件和事实。",
            "## RelayStack handoff",
            read_text(snapshot),
            "## 任务补充",
            task_handoff or "未提供",
            "## instruction.md",
            instruction,
        ]
    )
    return prompt, snapshot


def load_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"metrics_parse_error": str(path)}
    return data if isinstance(data, dict) else {}


def first_number(patterns: list[str], text: str) -> int | float | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            raw = match.group(1).replace(",", "")
            return float(raw) if "." in raw else int(raw)
    return None


def merged_metrics(agent_output: str, metrics_path: Path) -> dict[str, object]:
    metrics = load_json(metrics_path)
    metrics.setdefault(
        "total_tokens",
        first_number([r"total[_ ]tokens[\"':= ]+([0-9,]+)", r"tokens[\"':= ]+([0-9,]+)"], agent_output),
    )
    metrics.setdefault(
        "cost_usd",
        first_number([r"cost[_ ]usd[\"':= $]+([0-9.]+)", r"cost[\"':= $]+([0-9.]+)"], agent_output),
    )
    metrics.setdefault("steps_after_handoff", metrics.get("execution_steps"))
    metrics.setdefault("repeated_known_info", None)
    return metrics


def append_result(result: dict[str, object], report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n")


def run_task(task_dir: Path, runner_name: str, agent_cmd: str, report_path: Path, keep_workdir: bool) -> dict[str, object]:
    task_dir = task_dir.resolve()
    started = time.monotonic()
    tmp = tempfile.TemporaryDirectory(prefix=f"rsbench-{task_dir.name}-")
    workdir = Path(tmp.name)
    if keep_workdir:
        tmp.cleanup()
        workdir = Path(tempfile.mkdtemp(prefix=f"rsbench-{task_dir.name}-"))

    copy_initial_repo(task_dir, workdir)
    prompt, snapshot = build_prompt(task_dir, workdir, runner_name)
    prompt_path = workdir / "prompt.md"
    metrics_path = workdir / "agent-metrics.json"
    prompt_path.write_text(prompt, encoding="utf-8")

    env = os.environ.copy()
    env.update(
        {
            "RS_BENCH_TASK_DIR": str(task_dir),
            "RS_BENCH_WORKDIR": str(workdir),
            "RS_BENCH_PROMPT": str(prompt_path),
            "RS_BENCH_INSTRUCTION": str(task_dir / "instruction.md"),
            "RS_BENCH_METRICS": str(metrics_path),
            "RS_BENCH_RUNNER": runner_name,
        }
    )

    agent = run_shell(agent_cmd, workdir, env)
    test = run(["bash", str(task_dir / "test.sh")], workdir, env)
    elapsed = round(time.monotonic() - started, 3)
    metrics = merged_metrics(agent.stdout, metrics_path)
    passed = test.returncode == 0
    result = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "runner": runner_name,
        "task": task_dir.name,
        "passed": passed,
        "elapsed_seconds": elapsed,
        "total_tokens": metrics.get("total_tokens"),
        "cost_usd": metrics.get("cost_usd"),
        "steps_after_handoff": metrics.get("steps_after_handoff"),
        "repeated_known_info": metrics.get("repeated_known_info"),
        "agent_returncode": agent.returncode,
        "test_returncode": test.returncode,
        "snapshot_generated": snapshot is not None,
        "snapshot": str(snapshot) if snapshot and keep_workdir else None,
        "workdir": str(workdir) if keep_workdir else None,
    }
    append_result(result, report_path)
    if not keep_workdir:
        tmp.cleanup()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return result


def main(runner_name: str) -> int:
    parser = argparse.ArgumentParser(description=f"Run RelayStack benchmark tasks with {runner_name}.")
    parser.add_argument("tasks", nargs="+", type=Path)
    parser.add_argument("--agent-cmd", required=True, help="Command that edits the temp repo. Read $RS_BENCH_PROMPT.")
    parser.add_argument("--report", type=Path, default=RESULTS)
    parser.add_argument("--keep-workdir", action="store_true")
    args = parser.parse_args()

    results = [
        run_task(task, runner_name, args.agent_cmd, args.report, args.keep_workdir)
        for task in args.tasks
    ]
    return 0 if all(result["passed"] for result in results) else 1
