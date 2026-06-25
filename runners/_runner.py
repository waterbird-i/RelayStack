#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
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
BENCHMARK_FILES = {"agent-metrics.json", "prompt.md"}


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
    metrics_note = "\n".join(
        [
            "",
            "## Benchmark metrics",
            "完成修改和验证后，写入 `$RS_BENCH_METRICS` 指向的 JSON 文件：",
            '{"steps_after_handoff": <number>, "repeated_known_info": <true|false>}',
            "steps_after_handoff 统计你开始执行后用于理解/修改/验证的主要动作数。",
            "repeated_known_info 表示你是否重复探索了 prompt 或 handoff 已明确给出的文件/事实。",
        ]
    )
    if runner_name == "no_handoff":
        return instruction + metrics_note, None

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
            metrics_note,
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


def append_jsonl(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def candidate_id(seed: str, runner_name: str, task_name: str) -> str:
    digest = hashlib.sha1(f"{seed}:{runner_name}:{task_name}".encode("utf-8")).hexdigest()
    return f"cand-{digest[:8]}"


def run_id(pair_id: str, candidate: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    suffix = hashlib.sha1(f"{stamp}:{pair_id}:{candidate}:{time.monotonic()}".encode("utf-8")).hexdigest()[:6]
    return f"{stamp}-{safe_name(pair_id)}-{safe_name(candidate)}-{suffix}"


def safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "-", value).strip("-") or "unknown"


def init_diff_baseline(workdir: Path) -> None:
    ensure_git_repo(workdir)
    run(["git", "add", "-A"], workdir)


def code_change_lines(workdir: Path) -> list[str]:
    tracked = run(["git", "diff", "--name-status"], workdir).stdout.splitlines()
    untracked = run(["git", "ls-files", "--others", "--exclude-standard"], workdir).stdout.splitlines()
    lines = tracked + [f"A\t{path}" for path in untracked]
    return [
        line
        for line in lines
        if line and not any(line.endswith(f"\t{name}") or line == name for name in BENCHMARK_FILES)
    ]


def output_summary(output: str, returncode: int) -> dict[str, object]:
    lines = output.splitlines()
    return {
        "returncode": returncode,
        "line_count": len(lines),
        "tail": "\n".join(lines[-20:]),
    }


def write_blind_artifacts(
    blind_dir: Path,
    pair_id: str,
    candidate: str,
    runner_name: str,
    result: dict[str, object],
    agent_output: str,
    test_output: str,
    workdir: Path,
    prompt_path: Path,
    snapshot: Path | None,
    seed: str,
) -> None:
    current_run_id = run_id(pair_id, candidate)
    artifact_dir = blind_dir / "runs" / current_run_id
    artifact_dir.mkdir(parents=True, exist_ok=True)
    (artifact_dir / "agent-output.txt").write_text(agent_output, encoding="utf-8")
    (artifact_dir / "test-output.txt").write_text(test_output, encoding="utf-8")
    (artifact_dir / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    shutil.copyfile(prompt_path, artifact_dir / "prompt.md")
    if snapshot and snapshot.exists():
        shutil.copyfile(snapshot, artifact_dir / "snapshot.md")

    diff_lines = code_change_lines(workdir)
    (artifact_dir / "diff-summary.txt").write_text("\n".join(diff_lines) + ("\n" if diff_lines else ""), encoding="utf-8")
    (artifact_dir / "diff.patch").write_text(run(["git", "diff"], workdir).stdout, encoding="utf-8")

    raw = dict(result)
    raw.update(
        {
            "run_id": current_run_id,
            "pair_id": pair_id,
            "candidate_id": candidate,
            "seed": seed,
            "runner": runner_name,
            "artifact_dir": str(artifact_dir),
        }
    )
    append_jsonl(blind_dir / "raw-runs.jsonl", raw)

    packet = {
        "pair_id": pair_id,
        "candidate_id": candidate,
        "run_id": current_run_id,
        "seed": seed,
        "task": result["task"],
        "passed": result["passed"],
        "elapsed_seconds": result["elapsed_seconds"],
        "total_tokens": result["total_tokens"],
        "cost_usd": result["cost_usd"],
        "agent_returncode": result["agent_returncode"],
        "test_returncode": result["test_returncode"],
        "steps_after_handoff": result["steps_after_handoff"],
        "repeated_known_info": result["repeated_known_info"],
        "diff_summary": diff_lines,
        "test_summary": output_summary(test_output, result["test_returncode"]),
        "transcript_summary": output_summary(agent_output, result["agent_returncode"]),
        "redactions": ["runner_name", "group_name", "prompt_branding", "workdir"],
    }
    append_jsonl(blind_dir / "packets.jsonl", packet)

    debug_packet = dict(packet)
    debug_packet["context_packet_summary"] = (
        "provided target entry, root-cause hint, validation command"
        if snapshot is not None
        else "none"
    )
    append_jsonl(blind_dir / "debug-packets.jsonl", debug_packet)

    map_path = blind_dir / "unblind-map.json"
    try:
        unblind = json.loads(map_path.read_text(encoding="utf-8")) if map_path.exists() else {}
    except json.JSONDecodeError:
        unblind = {}
    unblind.setdefault(pair_id, {})[candidate] = {"runner": runner_name, "run_id": current_run_id}
    map_path.write_text(json.dumps(unblind, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_task(
    task_dir: Path,
    runner_name: str,
    agent_cmd: str,
    report_path: Path,
    keep_workdir: bool,
    blind_dir: Path | None,
    seed: str,
    pair_id_arg: str | None,
) -> dict[str, object]:
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
    if blind_dir is not None:
        init_diff_baseline(workdir)

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
    if blind_dir is not None:
        pair_id = pair_id_arg or task_dir.name
        candidate = candidate_id(seed, runner_name, task_dir.name)
        write_blind_artifacts(
            blind_dir,
            pair_id,
            candidate,
            runner_name,
            result,
            agent.stdout,
            test.stdout,
            workdir,
            prompt_path,
            snapshot,
            seed,
        )
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
    parser.add_argument("--blind-dir", type=Path, help="Write blind-review packets and artifacts into this directory.")
    parser.add_argument("--seed", default="0", help="Seed used for stable anonymized candidate ids.")
    parser.add_argument("--pair-id", help="Override pair id. Best for single-task runs; batch runs default to task name.")
    args = parser.parse_args()

    results = [
        run_task(
            task,
            runner_name,
            args.agent_cmd,
            args.report,
            args.keep_workdir,
            args.blind_dir,
            args.seed,
            args.pair_id,
        )
        for task in args.tasks
    ]
    return 0 if all(result["passed"] for result in results) else 1
