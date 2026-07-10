#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: expected JSON object")
    return data


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


def instance_key(row: dict[str, object]) -> str:
    if row.get("instance_id"):
        return str(row["instance_id"])
    org = row.get("org")
    repo = row.get("repo")
    number = row.get("number")
    return f"{org}__{repo}-{number}"


def task_type(row: dict[str, object]) -> str:
    if row.get("task_type"):
        return str(row["task_type"])
    title = str(row.get("title") or "").lower()
    if "parser" in title or "parse" in title:
        return "parser"
    if "ffi" in title or "codegen" in title:
        return "compiler-codegen"
    if "string" in title or "character" in title:
        return "language-semantics"
    return str(row.get("difficulty") or "unknown")


def result_for(report: dict[str, object], row: dict[str, object]) -> str:
    keys = {
        instance_key(row),
        f"{row.get('org')}/{row.get('repo')}:pr-{row.get('number')}",
    }
    for name in ["resolved_ids", "unresolved_ids", "error_ids"]:
        values = report.get(name, [])
        if isinstance(values, list) and keys.intersection(str(value) for value in values):
            return name.removesuffix("_ids")
    return "unknown"


def add_metric(bucket: dict[str, int], status: str) -> None:
    bucket["total"] += 1
    bucket[status] += 1


def summarize(run_dir: Path) -> dict[str, object]:
    run_dir = run_dir.resolve()
    rows = read_jsonl(run_dir / "dataset.jsonl")
    reports = {
        group: read_json(run_dir / group / "final_report.json")
        for group in ["baseline-output", "relaystack_handoff-output"]
        if (run_dir / group / "final_report.json").exists()
    }
    groups = {
        "baseline": reports.get("baseline-output", {}),
        "relaystack_handoff": reports.get("relaystack_handoff-output", {}),
    }
    strata: dict[str, dict[str, dict[str, dict[str, int]]]] = {
        "language": defaultdict(lambda: defaultdict(lambda: defaultdict(int))),
        "repo": defaultdict(lambda: defaultdict(lambda: defaultdict(int))),
        "task_type": defaultdict(lambda: defaultdict(lambda: defaultdict(int))),
    }
    instances: list[dict[str, object]] = []
    for row in rows:
        key = instance_key(row)
        repo = f"{row.get('org')}/{row.get('repo')}"
        item = {
            "instance_id": key,
            "repo": repo,
            "language": row.get("language") or "unknown",
            "difficulty": row.get("difficulty") or "unknown",
            "task_type": task_type(row),
            "title": row.get("title"),
            "base_commit": (row.get("base") or {}).get("sha") if isinstance(row.get("base"), dict) else row.get("base_commit"),
            "groups": {},
        }
        for group, report in groups.items():
            status = result_for(report, row) if report else "missing_report"
            item["groups"][group] = status  # type: ignore[index]
            add_metric(strata["language"][str(item["language"])][group], status)
            add_metric(strata["repo"][repo][group], status)
            add_metric(strata["task_type"][str(item["task_type"])][group], status)
        instances.append(item)
    return {
        "run_dir": str(run_dir.relative_to(ROOT) if run_dir.is_relative_to(ROOT) else run_dir),
        "instances": instances,
        "strata": {
            level: {name: dict(groups) for name, groups in buckets.items()}
            for level, buckets in strata.items()
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize Multi-SWE A/B results by language, repo, and task type.")
    parser.add_argument("--run-dir", type=Path, default=ROOT / "reports/multi-swe-one-20260629")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = summarize(args.run_dir)
    text = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
