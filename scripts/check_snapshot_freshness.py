#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], cwd: Path) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if result.returncode != 0:
        return "未发现"
    return result.stdout.strip() or "未发现"


def without_path(text: str, excluded: str) -> str:
    if text == "未发现":
        return text
    lines = [line for line in text.splitlines() if excluded not in line]
    return "\n".join(lines) if lines else "未发现"


def fingerprint(root: Path, exclude: Path | None = None) -> str:
    excluded = str(exclude.relative_to(root)) if exclude and exclude.is_relative_to(root) else None
    status = run(["git", "status", "--short"], root)
    diff_stat = run(["git", "diff", "--stat"], root)
    diff_names = run(["git", "diff", "--name-only"], root)
    if excluded:
        status = without_path(status, excluded)
        diff_stat = without_path(diff_stat, excluded)
        diff_names = without_path(diff_names, excluded)
    payload = "\n".join(
        [
            run(["git", "branch", "--show-current"], root),
            status,
            diff_stat,
            diff_names,
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def quality_block(snapshot: Path) -> dict[str, object]:
    text = snapshot.read_text(encoding="utf-8")
    match = re.search(r"(?s)^## 0\. 机器可读质量评分\s*```json\s*(.*?)\s*```", text, re.MULTILINE)
    if not match:
        raise SystemExit(f"{snapshot}: missing machine-readable quality block")
    data = json.loads(match.group(1))
    if not isinstance(data, dict):
        raise SystemExit(f"{snapshot}: quality block must be a JSON object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether a RelayStack snapshot still matches the current git diff.")
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()

    data = quality_block(args.snapshot)
    freshness = data.get("evidence_freshness", {})
    if not isinstance(freshness, dict):
        raise SystemExit(f"{args.snapshot}: missing evidence_freshness object")
    expected = freshness.get("fingerprint")
    current = fingerprint(args.root, args.snapshot.resolve())
    result = {
        "snapshot": str(args.snapshot),
        "fresh": expected == current,
        "snapshot_fingerprint": expected,
        "current_fingerprint": current,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["fresh"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
