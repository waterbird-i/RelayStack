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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", default="suites/authoritative/multi-swe-bench.json")
    parser.add_argument("--output", default="reports/authoritative-ab-20260629.json")
    parser.add_argument("--run-dir", default="reports/multi-swe-one-20260629")
    args = parser.parse_args()

    suite_path = ROOT / args.suite
    run_dir = ROOT / args.run_dir
    dataset_row = load_jsonl_first(run_dir / "dataset.jsonl")
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
        "dataset": {
            "name": "ByteDance-Seed/Multi-SWE-bench-flash",
            "instance_id": None if dataset_row is None else dataset_row.get("instance_id"),
            "org": None if dataset_row is None else dataset_row.get("org"),
            "repo": None if dataset_row is None else dataset_row.get("repo"),
            "number": None if dataset_row is None else dataset_row.get("number"),
            "title": None if dataset_row is None else dataset_row.get("title"),
            "issue_url": None if dataset_row is None else f"https://github.com/{dataset_row.get('org')}/{dataset_row.get('repo')}/issues/7238",
            "pr_url": None if dataset_row is None else f"https://github.com/{dataset_row.get('org')}/{dataset_row.get('repo')}/pull/{dataset_row.get('number')}",
            "base_commit": None if dataset_row is None else dataset_row.get("base", {}).get("sha"),
            "language": None if dataset_row is None else dataset_row.get("language"),
            "license": "MIT",
        },
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
        "artifacts": [
            "reports/multi-swe-one-20260629/dataset.jsonl",
            "reports/multi-swe-one-20260629/baseline.jsonl",
            "reports/multi-swe-one-20260629/relaystack_handoff.jsonl",
            "reports/multi-swe-one-20260629/baseline-output/final_report.json",
            "reports/multi-swe-one-20260629/relaystack_handoff-output/final_report.json",
            "reports/multi-swe-one-20260629/baseline-agent-output.jsonl",
            "reports/multi-swe-one-20260629/relaystack_handoff-agent-output.jsonl",
            "reports/multi-swe-one-20260629/summary.json",
        ],
    }
    result.update(summary_metrics)
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output.relative_to(ROOT))
    return 0 if status == "official_evaluated" else 1


if __name__ == "__main__":
    raise SystemExit(main())
