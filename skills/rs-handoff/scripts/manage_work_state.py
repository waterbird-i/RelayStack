#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from generate_snapshot import collect_evidence, evidence_fingerprint, git_root
from work_state_lib import (
    DEFAULT_STATE_PATH,
    MISSING,
    canonical_phase,
    load_current_work_state,
    normalize_list,
    recommended_phase,
    recommended_skill,
    text_value,
    summarize_current_work_state,
    write_current_work_state,
)


QUALITY_HEADING = "0. 机器可读质量评分"
CHECK_FRESHNESS_SCRIPT = Path(__file__).resolve().parents[3] / "scripts" / "check_snapshot_freshness.py"


def parse_snapshot_quality(snapshot: Path) -> dict[str, object]:
    text = snapshot.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"(?s)^## 0\. 机器可读质量评分\s*```json\s*(.*?)\s*```", text, re.MULTILINE)
    if not match:
        raise SystemExit(f"{snapshot}: missing machine-readable quality block")
    data = json.loads(match.group(1))
    if not isinstance(data, dict):
        raise SystemExit(f"{snapshot}: quality block must be a JSON object")
    return data


def verify_snapshot_freshness(root: Path, snapshot: Path) -> dict[str, object]:
    result = subprocess.run(
        [sys.executable, str(CHECK_FRESHNESS_SCRIPT), str(snapshot), "--root", str(root)],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    payload: dict[str, object] = {}
    if result.stdout.strip():
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError:
            payload = {}
    if result.returncode != 0 or not payload.get("fresh"):
        if payload:
            raise SystemExit(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        raise SystemExit(result.stderr.strip() or f"{snapshot}: snapshot is stale")
    return payload


def parse_snapshot_state(quality: dict[str, object]) -> dict[str, object]:
    state = quality.get("current_work_state", {})
    if isinstance(state, dict):
        return state
    return {}


def state_key(state: dict[str, object]) -> str:
    return text_value(state, "work_id", text_value(state, "id"))


def validate_live_state(state: dict[str, object], source: str) -> None:
    if not state:
        raise SystemExit(f"{source}: current-work-state 不存在")
    if not bool(state.get("context_manifest_present")):
        raise SystemExit(f"{source}: current-work-state 缺少 context manifest")
    if not bool(state.get("active")):
        raise SystemExit(f"{source}: current-work-state 已结束，无法继续")
    if state_key(state) == MISSING:
        raise SystemExit(f"{source}: current-work-state 缺少 work_id")


def merge_state(
    root: Path,
    snapshot_path: Path,
    quality: dict[str, object],
    existing_state: dict[str, object],
    freshness: dict[str, object],
    command: str,
    owner: str | None,
    claimed_by: str | None,
    next_action: str | None,
    note: list[str],
) -> dict[str, object]:
    snapshot_state = parse_snapshot_state(quality)
    manual_fields = quality.get("manual_fields", {})
    if not isinstance(manual_fields, dict):
        manual_fields = {}

    source_stage = snapshot_state.get("stage") or manual_fields.get("stage") or existing_state.get("stage")
    source_owner = owner or snapshot_state.get("owner") or existing_state.get("owner") or claimed_by or "current agent"
    source_action = next_action or snapshot_state.get("next_action") or manual_fields.get("next_step") or existing_state.get("next_action")
    if not source_action or source_action == MISSING:
        source_action = "sediment" if command == "finish" else "handoff"

    linked_docs = normalize_list(
        snapshot_state.get("linked_docs")
        or snapshot_state.get("backlinks")
        or existing_state.get("linked_docs")
        or existing_state.get("backlinks")
    )
    context_manifest = snapshot_state.get("context_manifest") or existing_state.get("context_manifest") or {}
    if not isinstance(context_manifest, dict):
        context_manifest = {}
    context_manifest = {
        "docs": normalize_list(context_manifest.get("docs")),
        "code": normalize_list(context_manifest.get("code")),
        "evidence": normalize_list(context_manifest.get("evidence")),
    }
    actor = claimed_by or source_owner
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    snapshot_fingerprint = (
        str(freshness.get("snapshot_fingerprint"))
        if freshness.get("snapshot_fingerprint")
        else MISSING
    )
    current_fingerprint = (
        str(freshness.get("current_fingerprint"))
        if freshness.get("current_fingerprint")
        else MISSING
    )
    phase = recommended_phase(source_action, source_stage)
    work_id = (
        snapshot_state.get("work_id")
        or snapshot_state.get("id")
        or manual_fields.get("work_id")
        or existing_state.get("work_id")
        or existing_state.get("id")
        or quality.get("task")
        or snapshot_path.stem
    )
    stage = source_stage or canonical_phase(source_action)
    summary = {
        "schema_version": 1,
        "id": work_id,
        "work_id": work_id,
        "stage": stage,
        "owner": source_owner,
        "next_action": source_action,
        "next_phase": phase,
        "next_skill": recommended_skill(source_action, stage),
        "status": "finished" if command == "finish" else "claimed",
        "lifecycle_state": "finished" if command == "finish" else "active",
        "active": command != "finish",
        "is_finished": command == "finish",
        "claimed_by": actor,
        "claimed_at": timestamp if command == "continue" else existing_state.get("claimed_at", timestamp),
        "finished_by": existing_state.get("finished_by", MISSING),
        "finished_at": existing_state.get("finished_at", MISSING),
        "closed_by": existing_state.get("closed_by", MISSING),
        "closed_at": existing_state.get("closed_at", MISSING),
        "updated_at": timestamp,
        "source_snapshot": str(snapshot_path),
        "source_snapshot_fingerprint": snapshot_fingerprint,
        "evidence_fingerprint": current_fingerprint,
        "current_fingerprint": current_fingerprint,
        "linked_docs": linked_docs,
        "backlinks": linked_docs,
        "context_manifest": context_manifest,
        "context_manifest_present": any(context_manifest[bucket] for bucket in ("docs", "code", "evidence")),
        "notes": note,
        "warnings": normalize_list(existing_state.get("warnings")) + normalize_list(snapshot_state.get("warnings")),
        "validation": manual_fields.get("validation") or existing_state.get("validation") or MISSING,
    }
    return summary


def prepare_transition(root: Path, args: argparse.Namespace, command: str) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    freshness = verify_snapshot_freshness(root, args.snapshot)
    quality = parse_snapshot_quality(args.snapshot)
    snapshot_state = parse_snapshot_state(quality)
    validate_live_state(snapshot_state, str(args.snapshot))
    current_state = load_current_work_state(root, Path(args.state))
    current_state_summary = summarize_current_work_state(current_state, root, str(freshness.get("current_fingerprint")) if freshness.get("current_fingerprint") else None)
    validate_live_state(current_state_summary, str(Path(args.state)))
    if state_key(snapshot_state) != state_key(current_state_summary):
        raise SystemExit(
            f"{args.snapshot}: work_id {state_key(snapshot_state)} 与 live state {state_key(current_state_summary)} 不一致"
        )
    if command == "finish" and str(current_state_summary.get("status", "")).strip().lower() == "finished":
        raise SystemExit(f"{args.state}: current-work-state 已结束，无法再次 finish")
    return freshness, quality, current_state.data


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Continue or finish the lightweight RelayStack current work state.")
    parser.add_argument("--state", default=str(DEFAULT_STATE_PATH), help="current work state path")
    parser.add_argument("--self-test", action="store_true")

    subparsers = parser.add_subparsers(dest="command")

    continue_parser = subparsers.add_parser("continue", help="claim the next step from a fresh snapshot")
    continue_parser.add_argument("snapshot", type=Path)
    continue_parser.add_argument("--owner")
    continue_parser.add_argument("--claimed-by")
    continue_parser.add_argument("--note", action="append", default=[])

    finish_parser = subparsers.add_parser("finish", help="close the current work state after a fresh snapshot")
    finish_parser.add_argument("snapshot", type=Path)
    finish_parser.add_argument("--owner")
    finish_parser.add_argument("--claimed-by")
    finish_parser.add_argument("--next-action")
    finish_parser.add_argument("--note", action="append", default=[])

    parser.set_defaults(command="continue")
    return parser


def command_continue(root: Path, args: argparse.Namespace) -> dict[str, object]:
    freshness, quality, current_state = prepare_transition(root, args, "continue")
    summary = merge_state(
        root,
        args.snapshot,
        quality,
        current_state,
        freshness,
        "continue",
        args.owner,
        args.claimed_by,
        None,
        normalize_list(args.note),
    )
    write_current_work_state(Path(args.state) if Path(args.state).is_absolute() else root / Path(args.state), summary)
    return {
        "action": "continue",
        "state": summary,
        "freshness": freshness,
    }


def command_finish(root: Path, args: argparse.Namespace) -> dict[str, object]:
    freshness, quality, current_state = prepare_transition(root, args, "finish")
    summary = merge_state(
        root,
        args.snapshot,
        quality,
        current_state,
        freshness,
        "finish",
        args.owner,
        args.claimed_by,
        args.next_action or "sediment",
        normalize_list(args.note),
    )
    summary["status"] = "finished"
    summary["finished_by"] = args.claimed_by or args.owner or summary.get("owner", "current agent")
    summary["finished_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary["closed_by"] = summary["finished_by"]
    summary["closed_at"] = summary["finished_at"]
    summary["lifecycle_state"] = "finished"
    summary["active"] = False
    summary["is_finished"] = True
    write_current_work_state(Path(args.state) if Path(args.state).is_absolute() else root / Path(args.state), summary)
    return {
        "action": "finish",
        "state": summary,
        "freshness": freshness,
    }


def self_test() -> None:
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as temp:
        sandbox = Path(temp)
        root = Path(temp) / "repo"
        root.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        (root / ".gitignore").write_text("/project/\n", encoding="utf-8")
        (root / "README.md").write_text("test readme\n", encoding="utf-8")
        (root / "docs" / "context").mkdir(parents=True)
        (root / "docs" / "context" / "allowed.md").write_text("allowed\n", encoding="utf-8")
        subprocess.run(["git", "config", "user.name", "RelayStack Test"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "relaystack@example.com"], cwd=root, check=True)
        subprocess.run(["git", "add", ".gitignore", "README.md", "docs/context/allowed.md"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "initial"], cwd=root, check=True)
        initial_evidence = collect_evidence(root)
        fingerprint = evidence_fingerprint(initial_evidence)
        write_current_work_state(
            root / "project" / "handoffs" / "current-work-state.md",
            {
                "schema_version": 1,
                "id": "state-a",
                "work_id": "state-a",
                "stage": "design",
                "owner": "owner",
                "next_action": "implement",
                "next_phase": "implement",
                "next_skill": "rs-feat-impl",
                "status": "active",
                "lifecycle_state": "active",
                "active": True,
                "is_finished": False,
                "claimed_by": "owner",
                "claimed_at": "2000-01-01 00:00:00",
                "finished_by": "未发现",
                "finished_at": "未发现",
                "closed_by": "未发现",
                "closed_at": "未发现",
                "updated_at": "2000-01-01 00:00:00",
                "evidence_fingerprint": fingerprint,
                "current_fingerprint": fingerprint,
                "linked_docs": ["docs/context/allowed.md"],
                "backlinks": ["docs/context/allowed.md"],
                "context_manifest": {
                    "docs": ["docs/context/allowed.md"],
                    "code": ["skills/rs-handoff/scripts/manage_work_state.py"],
                    "evidence": ["git status --short"],
                },
                "context_manifest_present": True,
                "notes": ["self-test state"],
                "warnings": [],
            },
        )
        snapshot = sandbox / "snapshot.md"
        snapshot.write_text(
            "\n".join(
                [
                    "# Handoff Snapshot: 测试",
                    "",
                    "## 0. 机器可读质量评分",
                    "```json",
                    json.dumps(
                        {
                            "task": "测试",
                            "manual_fields": {"goal": "goal", "stage": "design", "owner": "owner", "next_step": "next"},
                            "current_work_state": {
                                "present": True,
                                "work_id": "state-a",
                                "id": "state-a",
                                "stage": "design",
                                "owner": "owner",
                                "next_action": "implement",
                                "next_phase": "implement",
                                "next_skill": "rs-feat-impl",
                                "status": "active",
                                "lifecycle_state": "active",
                                "active": True,
                                "is_finished": False,
                                "claimed_by": "owner",
                                "claimed_at": "2000-01-01 00:00:00",
                                "finished_by": "未发现",
                                "finished_at": "未发现",
                                "closed_by": "未发现",
                                "closed_at": "未发现",
                                "evidence_fingerprint": fingerprint,
                                "current_fingerprint": fingerprint,
                                "linked_docs": ["docs/context/allowed.md"],
                                "context_manifest": {
                                    "docs": ["docs/context/allowed.md"],
                                    "code": ["skills/rs-handoff/scripts/manage_work_state.py"],
                                    "evidence": ["git status --short"],
                                },
                                "context_manifest_present": True,
                                "warnings": [],
                            },
                            "evidence_freshness": {
                                "fingerprint": fingerprint,
                            },
                        },
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=True,
                    ),
                    "```",
                ]
            ),
            encoding="utf-8",
        )

        args = build_parser().parse_args(
            [
                "--state",
                str(root / "project" / "handoffs" / "current-work-state.md"),
                "continue",
                str(snapshot),
                "--claimed-by",
                "agent-a",
                "--note",
                "ready",
            ]
        )
        output = command_continue(root, args)
        state_path = root / "project" / "handoffs" / "current-work-state.md"
        text = state_path.read_text(encoding="utf-8")
        assert output["action"] == "continue"
        assert '"status": "claimed"' in text
        assert '"next_skill": "rs-feat-impl"' in text
        assert '"id": "state-a"' in text
        assert '"next_phase": "implement"' in text
        assert '"lifecycle_state": "active"' in text
        assert "agent-a" in text

        fresh_state_snapshot = sandbox / "fresh-state-snapshot.md"
        fresh_snapshot_text = "\n".join(
            [
                "# Handoff Snapshot: 缺失 manifest",
                "",
                "## 0. 机器可读质量评分",
                "```json",
                json.dumps(
                    {
                        "task": "测试",
                        "manual_fields": {"goal": "goal", "stage": "design", "owner": "owner", "next_step": "next"},
                        "current_work_state": {
                            "present": True,
                            "work_id": "state-a",
                            "id": "state-a",
                            "stage": "design",
                            "owner": "owner",
                            "next_action": "implement",
                            "next_phase": "implement",
                            "next_skill": "rs-feat-impl",
                            "status": "active",
                            "lifecycle_state": "active",
                            "active": True,
                            "claimed_by": "owner",
                            "claimed_at": "2000-01-01 00:00:00",
                            "evidence_fingerprint": fingerprint,
                            "current_fingerprint": fingerprint,
                            "linked_docs": ["docs/context/allowed.md"],
                            "context_manifest": {
                                "docs": [],
                                "code": [],
                                "evidence": [],
                            },
                            "context_manifest_present": False,
                            "warnings": [],
                        },
                        "evidence_freshness": {
                            "fingerprint": fingerprint,
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                ),
                "```",
            ]
        )
        fresh_state_snapshot.write_text(fresh_snapshot_text, encoding="utf-8")
        no_manifest_args = build_parser().parse_args(
            [
                "--state",
                str(state_path),
                "continue",
                str(fresh_state_snapshot),
            ]
        )
        try:
            command_continue(root, no_manifest_args)
        except SystemExit as exc:
            assert "context manifest" in str(exc)
        else:
            raise AssertionError("expected missing manifest rejection")

        stale_snapshot = sandbox / "stale-snapshot.md"
        stale_snapshot.write_text(snapshot.read_text(encoding="utf-8"), encoding="utf-8")
        original_readme = (root / "README.md").read_text(encoding="utf-8")
        (root / "README.md").write_text("changed readme\n", encoding="utf-8")
        stale_args = build_parser().parse_args(
            [
                "--state",
                str(state_path),
                "continue",
                str(stale_snapshot),
            ]
        )
        try:
            command_continue(root, stale_args)
        except SystemExit as exc:
            assert "snapshot is stale" in str(exc) or "fingerprint mismatch" in str(exc)
        else:
            raise AssertionError("expected stale snapshot rejection")
        (root / "README.md").write_text(original_readme, encoding="utf-8")

        finish_args = build_parser().parse_args(
            [
                "--state",
                str(state_path),
                "finish",
                str(snapshot),
                "--claimed-by",
                "agent-b",
                "--next-action",
                "sediment",
                "--note",
                "done",
            ]
        )
        finish_output = command_finish(root, finish_args)
        finished_text = state_path.read_text(encoding="utf-8")
        assert finish_output["action"] == "finish"
        assert '"status": "finished"' in finished_text
        assert '"next_action": "sediment"' in finished_text
        assert "agent-b" in finished_text
        assert '"lifecycle_state": "finished"' in finished_text
        assert '"closed_by": "agent-b"' in finished_text

        try:
            command_finish(root, finish_args)
        except SystemExit as exc:
            assert "已结束" in str(exc) or "cannot" in str(exc)
        else:
            raise AssertionError("expected finished state rejection")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print("self-test ok")
        return 0
    root = git_root(Path.cwd())
    if args.command == "finish":
        result = command_finish(root, args)
    else:
        result = command_continue(root, args)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
