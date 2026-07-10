#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


FORBIDDEN = [
    "runner",
    "rs_handoff",
    "no_handoff",
    "snapshot_generated",
    "snapshot_chars",
    "snapshot_elapsed_seconds",
    "workdir",
    "benchmark-rs-handoff",
]


def check_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    leaks = [token for token in FORBIDDEN if token in text]
    for line_no, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            leaks.extend(key for key in row if key in FORBIDDEN)
    return sorted(set(leaks))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check reviewer-facing blind packets for runner identity leaks.")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    failed: dict[str, list[str]] = {}
    for path in args.paths:
        if path.is_dir():
            candidates = [p for p in path.rglob("*") if p.name in {"packets.jsonl", "continuation-packets.jsonl"}]
        else:
            candidates = [path]
        for candidate in candidates:
            leaks = check_file(candidate)
            if leaks:
                failed[str(candidate)] = leaks
    if failed:
        print(json.dumps({"ok": False, "leaks": failed}, ensure_ascii=False, indent=2, sort_keys=True))
        return 1
    print(json.dumps({"ok": True}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
