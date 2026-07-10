#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


def read_jsonl(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise SystemExit(f"{path}: expected object lines")
        rows.append(row)
    return rows


def packet_id(seed: str, task: str, source: str) -> str:
    digest = hashlib.sha256(f"{seed}:{task}:{source}".encode("utf-8")).hexdigest()[:10]
    return f"cont-{digest}"


def build_packet(row: dict[str, object], output_dir: Path, tasks_root: Path, seed: str) -> tuple[dict[str, object], dict[str, object]] | None:
    artifact_dir = Path(str(row.get("artifact_dir") or ""))
    snapshot = artifact_dir / "snapshot.md"
    result = artifact_dir / "result.json"
    task = str(row.get("task") or row.get("pair_id") or artifact_dir.name)
    instruction = tasks_root / task / "instruction.md"
    if not snapshot.exists() or not instruction.exists():
        return None
    pid = packet_id(seed, task, str(artifact_dir))
    packet_dir = output_dir / "runs" / pid
    packet_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(snapshot, packet_dir / "snapshot.md")
    shutil.copyfile(instruction, packet_dir / "upstream-task.md")
    if result.exists():
        shutil.copyfile(result, packet_dir / "oracle-result.json")
    packet = {
        "packet_id": pid,
        "task": task,
        "snapshot": str((packet_dir / "snapshot.md").relative_to(output_dir)),
        "upstream_task": str((packet_dir / "upstream-task.md").relative_to(output_dir)),
        "instructions": [
            "Read only snapshot.md and upstream-task.md.",
            "Do not read original chat transcripts, agent-output.txt, raw-runs.jsonl, or unblind-map.json.",
            "Continue the task in a clean worktree and report whether validation passes.",
        ],
    }
    oracle = {
        "packet_id": pid,
        "task": task,
        "oracle_result": str((packet_dir / "oracle-result.json").relative_to(output_dir)) if result.exists() else None,
        "source_artifact": str(artifact_dir),
    }
    return packet, oracle


def main() -> int:
    parser = argparse.ArgumentParser(description="Build snapshot-only continuation blind packets from existing blind run artifacts.")
    parser.add_argument("blind_dir", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--tasks-root", type=Path, default=Path("tasks"))
    parser.add_argument("--seed", default="continuation")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    packets: list[dict[str, object]] = []
    oracle_map: list[dict[str, object]] = []
    for row in read_jsonl(args.blind_dir / "raw-runs.jsonl"):
        built = build_packet(row, args.output_dir, args.tasks_root, args.seed)
        if built:
            packet, oracle = built
            packets.append(packet)
            oracle_map.append(oracle)
    out = args.output_dir / "continuation-packets.jsonl"
    out.write_text("".join(json.dumps(packet, ensure_ascii=False, sort_keys=True) + "\n" for packet in packets), encoding="utf-8")
    (args.output_dir / "oracle-map.json").write_text(json.dumps(oracle_map, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"packets": len(packets), "output": str(out)}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if packets else 1


if __name__ == "__main__":
    raise SystemExit(main())
