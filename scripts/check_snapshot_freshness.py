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
    text = snapshot.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"(?s)^## 0\. 机器可读质量评分\s*```json\s*(.*?)\s*```", text, re.MULTILINE)
    if not match:
        raise ValueError("missing machine-readable quality block")
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise ValueError(f"quality block JSON invalid: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise ValueError("quality block must be a JSON object")
    return data


def state_flags(data: dict[str, object]) -> tuple[bool, bool]:
    state = data.get("current_work_state", {})
    if not isinstance(state, dict):
        return False, False
    return bool(state.get("present")), bool(state.get("context_manifest_present"))


def emit_result(
    snapshot: Path,
    status: str,
    reason: str,
    current: str,
    expected: object = None,
    data: dict[str, object] | None = None,
) -> int:
    state_present, manifest_present = state_flags(data or {})
    payload = {
        "snapshot": str(snapshot),
        "fresh": status == "fresh",
        "status": status,
        "reason": reason,
        "snapshot_fingerprint": expected,
        "current_fingerprint": current,
        "current_work_state_present": state_present,
        "context_manifest_present": manifest_present,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload["fresh"] else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether a RelayStack snapshot still matches the current git diff.")
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()

    root = args.root.resolve()
    snapshot = args.snapshot
    current = fingerprint(root, snapshot.resolve())

    try:
        data = quality_block(snapshot)
    except FileNotFoundError:
        return emit_result(snapshot, "missing_snapshot", "snapshot file not found", current)
    except OSError as exc:
        return emit_result(snapshot, "unreadable_snapshot", str(exc), current)
    except ValueError as exc:
        return emit_result(snapshot, "malformed_snapshot", str(exc), current)

    freshness = data.get("evidence_freshness", {})
    if not isinstance(freshness, dict):
        return emit_result(snapshot, "missing_freshness", "missing evidence_freshness object", current, data=data)
    expected = freshness.get("fingerprint")
    if not expected:
        return emit_result(snapshot, "missing_fingerprint", "missing evidence_freshness.fingerprint", current, expected, data)
    if expected == current:
        return emit_result(snapshot, "fresh", "matching fingerprint", current, expected, data)
    return emit_result(snapshot, "stale", "fingerprint mismatch", current, expected, data)


if __name__ == "__main__":
    raise SystemExit(main())
