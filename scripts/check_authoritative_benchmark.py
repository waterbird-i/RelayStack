#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: expected object")
    return data


def load_jsonl_first(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            data = json.loads(line)
            if not isinstance(data, dict):
                raise SystemExit(f"{path}: expected object line")
            return data
    return None


def load_jsonl_all(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    rows: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        data = json.loads(line)
        if not isinstance(data, dict):
            raise SystemExit(f"{path}: expected object line")
        rows.append(data)
    return rows


def instance_id(row: dict[str, object]) -> str:
    if row.get("instance_id"):
        return str(row["instance_id"])
    return f"{row.get('org')}__{row.get('repo')}-{row.get('number')}"


def official_id(row: dict[str, object]) -> str:
    return f"{row.get('org')}/{row.get('repo')}:pr-{row.get('number')}"


def inferred_task_type(row: dict[str, object]) -> str:
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


def check_suite(path: Path) -> dict[str, object]:
    suite = load_json(path)
    required = ["suite_id", "suite_name", "authority", "status", "dataset", "license", "citation", "provenance_mapping"]
    missing = [key for key in required if key not in suite]
    return {
        "suite_id": suite.get("suite_id"),
        "suite_name": suite.get("suite_name"),
        "authority": suite.get("authority"),
        "status": suite.get("status"),
        "manifest_path": str(path.relative_to(ROOT)),
        "manifest_complete": not missing,
        "missing_manifest_fields": missing,
        "dataset": suite.get("dataset"),
        "license": suite.get("license"),
        "citation": suite.get("citation"),
    }


def patch_prediction_status(path: Path) -> dict[str, object]:
    row = load_jsonl_first(path)
    required = ["org", "repo", "number", "fix_patch"]
    missing = required if row is None else [key for key in required if key not in row]
    return {
        "path": str(path.relative_to(ROOT)),
        "exists": path.exists(),
        "valid_shape": row is not None and not missing,
        "missing_fields": missing,
        "patch_bytes": 0 if row is None else len(str(row.get("fix_patch", "")).encode("utf-8")),
    }


def final_report_status(path: Path) -> dict[str, object]:
    if not path.exists():
        return {
            "path": str(path.relative_to(ROOT)),
            "exists": False,
            "completed_instances": 0,
            "resolved_instances": 0,
            "unresolved_instances": 0,
            "error_instances": 0,
            "resolved_ids": [],
            "unresolved_ids": [],
            "error_ids": [],
        }
    report = load_json(path)
    return {
        "path": str(path.relative_to(ROOT)),
        "exists": True,
        "completed_instances": report.get("completed_instances", 0),
        "resolved_instances": report.get("resolved_instances", 0),
        "unresolved_instances": report.get("unresolved_instances", 0),
        "error_instances": report.get("error_instances", 0),
        "resolved_ids": report.get("resolved_ids", []),
        "unresolved_ids": report.get("unresolved_ids", []),
        "error_ids": report.get("error_ids", []),
    }


def status_for(report: dict[str, object], row: dict[str, object]) -> str:
    keys = {instance_id(row), official_id(row)}
    for key, status in [
        ("resolved_ids", "resolved"),
        ("unresolved_ids", "unresolved"),
        ("error_ids", "error"),
        ("incomplete_ids", "incomplete"),
        ("empty_patch_ids", "empty_patch"),
    ]:
        values = report.get(key, [])
        if isinstance(values, list) and keys.intersection(str(value) for value in values):
            return status
    return "unknown"


def dataset_summary(rows: list[dict[str, object]], reports: dict[str, dict[str, object]]) -> dict[str, object]:
    instances: list[dict[str, object]] = []
    for row in rows:
        item = {
            "instance_id": instance_id(row),
            "official_id": official_id(row),
            "org": row.get("org"),
            "repo": row.get("repo"),
            "number": row.get("number"),
            "title": row.get("title"),
            "base_commit": (row.get("base") or {}).get("sha") if isinstance(row.get("base"), dict) else row.get("base_commit"),
            "language": row.get("language"),
            "difficulty": row.get("difficulty"),
            "task_type": inferred_task_type(row),
            "groups": {
                name: status_for(report, row) for name, report in reports.items()
            },
        }
        instances.append(item)
    return {
        "name": "ByteDance-Seed/Multi-SWE-bench-flash",
        "count": len(rows),
        "instances": instances,
    }


def load_summary_metrics(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    summary = load_json(path)
    groups = summary.get("groups", {})
    if not isinstance(groups, dict):
        return {}
    agent_metrics = {}
    harness_timing = {}
    for group_name, group in groups.items():
        if not isinstance(group, dict):
            continue
        if "agent_metrics" in group:
            agent_metrics[group_name] = group["agent_metrics"]
        official = group.get("official_harness", {})
        if isinstance(official, dict) and "timing" in official:
            harness_timing[group_name] = official["timing"]
    metrics: dict[str, object] = {}
    if agent_metrics:
        metrics["agent_metrics"] = agent_metrics
    if harness_timing:
        metrics["official_harness_timing"] = harness_timing
    if "comparison_metrics" in summary:
        metrics["comparison_metrics"] = summary["comparison_metrics"]
    if "protocol_audit" in summary:
        metrics["protocol_audit"] = summary["protocol_audit"]
    return metrics


def run_artifacts(run_dir: Path) -> list[str]:
    names = [
        "dataset.jsonl",
        "baseline.jsonl",
        "relaystack_handoff.jsonl",
        "baseline-output/final_report.json",
        "relaystack_handoff-output/final_report.json",
        "baseline-agent-output.jsonl",
        "relaystack_handoff-agent-output.jsonl",
        "summary.json",
    ]
    return [str((run_dir / name).relative_to(ROOT)) for name in names]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", default="suites/authoritative/multi-swe-bench.json")
    parser.add_argument("--output", default="reports/authoritative-ab-20260629.json")
    parser.add_argument("--run-dir", default="reports/multi-swe-one-20260629")
    args = parser.parse_args()

    suite_path = ROOT / args.suite
    run_dir = ROOT / args.run_dir
    dataset_rows = load_jsonl_all(run_dir / "dataset.jsonl")
    dataset_row = dataset_rows[0] if dataset_rows else None
    predictions = {
        "baseline": patch_prediction_status(run_dir / "baseline.jsonl"),
        "relaystack_handoff": patch_prediction_status(run_dir / "relaystack_handoff.jsonl"),
    }
    official_reports = {
        "baseline": final_report_status(run_dir / "baseline-output" / "final_report.json"),
        "relaystack_handoff": final_report_status(run_dir / "relaystack_handoff-output" / "final_report.json"),
    }
    predictions_ready = all(group["valid_shape"] for group in predictions.values())
    official_complete = all(group["exists"] and group["error_instances"] == 0 for group in official_reports.values())
    summary_metrics = load_summary_metrics(run_dir / "summary.json")
    status = "official_evaluated" if predictions_ready and official_complete else "blocked"
    blocked_reason = None
    if not predictions_ready:
        blocked_reason = "Missing upstream-compatible prediction patch JSONL for at least one group."
    elif not official_complete:
        blocked_reason = "Official harness report is missing or contains harness errors for at least one group."

    result = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "check_type": "authoritative_handoff_ab",
        "suite": check_suite(suite_path),
        "local_baseline_suite": str(Path("suites/local-25.json")),
        "run_dir": str(run_dir.relative_to(ROOT)),
        "dataset": dataset_summary(dataset_rows, official_reports),
        "ab_groups": ["baseline", "relaystack_handoff"],
        "blind_test_status": status,
        "blocked_reason": blocked_reason,
        "prediction_patch_jsonl": predictions,
        "official_harness_reports": official_reports,
        "result_summary": {
            "baseline_resolved": official_reports["baseline"]["resolved_instances"],
            "relaystack_handoff_resolved": official_reports["relaystack_handoff"]["resolved_instances"],
            "baseline_completed": official_reports["baseline"]["completed_instances"],
            "relaystack_handoff_completed": official_reports["relaystack_handoff"]["completed_instances"],
        },
        "environment": {
            "docker_available": shutil.which("docker") is not None,
            "multi_swe_bench_module_available": importlib.util.find_spec("multi_swe_bench") is not None,
            "datasets_module_available": importlib.util.find_spec("datasets") is not None,
        },
        "artifacts": run_artifacts(run_dir),
    }
    result.update(summary_metrics)
    output = ROOT / args.output
    if Path(args.output).is_absolute():
        output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        print(output.relative_to(ROOT))
    except ValueError:
        print(output)
    return 0 if status == "official_evaluated" else 1


if __name__ == "__main__":
    raise SystemExit(main())
