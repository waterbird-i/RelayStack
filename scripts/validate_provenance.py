#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {"suite_id", "provenance_status", "source_type", "source_url", "license"}


def load_json(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: expected object")
    return data


def validate_task(path: Path) -> None:
    data = load_json(path)
    missing = sorted(REQUIRED - data.keys())
    if missing:
        raise SystemExit(f"{path}: missing {', '.join(missing)}")


def validate_suite(path: Path) -> None:
    data = load_json(path)
    for key in ["suite_id", "suite_name", "authority", "dataset", "license", "provenance_mapping"]:
        if key not in data:
            raise SystemExit(f"{path}: missing {key}")


def main() -> int:
    for path in sorted((ROOT / "tasks").glob("task-*/provenance.json")):
        validate_task(path)
    for path in sorted((ROOT / "suites" / "authoritative").glob("*.json")):
        validate_suite(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
