#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import time
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise SystemExit(f"{path}: expected object lines")
        rows.append(row)
    return rows


def run(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def run_shell(command: str, cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, env=env, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def write_prompt(packet: dict[str, object], packet_root: Path, prompt_path: Path) -> None:
    snapshot = packet_root / str(packet["snapshot"])
    upstream = packet_root / str(packet["upstream_task"])
    prompt_path.write_text(
        "\n\n".join(
            [
                "You are a continuation agent in a snapshot-only blind test.",
                "Use only the snapshot and upstream task below. Do not read original chat transcripts, raw run files, or unblind maps.",
                "When finished, write a JSON metrics file to $RS_CONTINUATION_METRICS with keys: continued_from_snapshot, validation_passed, notes.",
                "## snapshot.md",
                snapshot.read_text(encoding="utf-8"),
                "## upstream-task.md",
                upstream.read_text(encoding="utf-8"),
            ]
        ),
        encoding="utf-8",
    )


def run_packet(packet: dict[str, object], packet_root: Path, tasks_root: Path, agent_cmd: str, output_dir: Path, keep_workdir: bool) -> dict[str, object]:
    task = str(packet["task"])
    task_dir = tasks_root / task
    initial = task_dir / "initial-repo"
    if not initial.is_dir():
        raise SystemExit(f"missing initial repo: {initial}")
    workdir = Path(tempfile.mkdtemp(prefix=f"rs-cont-{task}-"))
    shutil.copytree(initial, workdir, dirs_exist_ok=True)
    prompt = workdir / "continuation-prompt.md"
    metrics = workdir / "continuation-metrics.json"
    write_prompt(packet, packet_root, prompt)
    started = time.monotonic()
    env = os.environ.copy()
    env.update(
        {
            "RS_CONTINUATION_PACKET": str(packet_root / str(packet["snapshot"])),
            "RS_CONTINUATION_PROMPT": str(prompt),
            "RS_CONTINUATION_METRICS": str(metrics),
        }
    )
    agent = run_shell(agent_cmd, workdir, env)
    test = run(["bash", str(task_dir / "test.sh")], workdir, env)
    elapsed = round(time.monotonic() - started, 3)
    metrics_data: dict[str, object] = {}
    if metrics.exists():
        try:
            loaded = json.loads(metrics.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                metrics_data = loaded
        except json.JSONDecodeError:
            metrics_data = {"metrics_parse_error": str(metrics)}
    packet_id = str(packet["packet_id"])
    artifact_dir = output_dir / "runs" / packet_id
    artifact_dir.mkdir(parents=True, exist_ok=True)
    (artifact_dir / "agent-output.txt").write_text(agent.stdout, encoding="utf-8")
    (artifact_dir / "test-output.txt").write_text(test.stdout, encoding="utf-8")
    (artifact_dir / "diff.patch").write_text(run(["git", "diff"], workdir).stdout, encoding="utf-8")
    shutil.copyfile(prompt, artifact_dir / "continuation-prompt.md")
    result = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "packet_id": packet_id,
        "task": task,
        "passed": test.returncode == 0,
        "agent_returncode": agent.returncode,
        "test_returncode": test.returncode,
        "elapsed_seconds": elapsed,
        "continued_from_snapshot": metrics_data.get("continued_from_snapshot"),
        "validation_passed": metrics_data.get("validation_passed"),
        "metrics": metrics_data,
        "artifact_dir": str(artifact_dir),
        "workdir": str(workdir) if keep_workdir else None,
    }
    (artifact_dir / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if not keep_workdir:
        shutil.rmtree(workdir)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run snapshot-only continuation blind packets with an agent command.")
    parser.add_argument("packets", type=Path)
    parser.add_argument("--agent-cmd", required=True, help="Command that reads $RS_CONTINUATION_PROMPT and edits the temp repo.")
    parser.add_argument("--tasks-root", type=Path, default=ROOT / "tasks")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--keep-workdir", action="store_true")
    args = parser.parse_args()

    packet_root = args.packets.parent
    rows = read_jsonl(args.packets)
    if args.limit is not None:
        rows = rows[: args.limit]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = [
        run_packet(row, packet_root, args.tasks_root, args.agent_cmd, args.output_dir, args.keep_workdir)
        for row in rows
    ]
    report = args.output_dir / "continuation-results.jsonl"
    report.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in results), encoding="utf-8")
    summary = {
        "packets": len(results),
        "passed": sum(1 for row in results if row["passed"]),
        "results": str(report),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if results and all(row["passed"] for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
