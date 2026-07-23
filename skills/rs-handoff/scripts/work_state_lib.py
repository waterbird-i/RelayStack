#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


MISSING = "未发现"
STATE_HEADING = "0. 机器可读状态"
STATE_SCHEMA_VERSION = 1
DEFAULT_STATE_PATH = Path("project/handoffs/current-work-state.md")

PHASE_SKILL_MAP: dict[str, str] = {
    "report": "rs-issue-report",
    "analysis": "rs-issue-analyze",
    "fix": "rs-issue-fix",
    "roadmap": "rs-roadmap",
    "design": "rs-feat-design",
    "implement": "rs-feat-impl",
    "accept": "rs-feat-accept",
    "handoff": "rs-handoff",
    "sediment": "rs-learn",
    "unknown": "rs-handoff",
}


@dataclass
class CurrentWorkState:
    path: Path
    present: bool
    data: dict[str, object]
    warnings: list[str]


def normalize_list(value: object) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    item = str(value).strip()
    return [item] if item else []


def text_value(data: dict[str, object], key: str, default: str = MISSING) -> str:
    value = data.get(key)
    if value is None or value == "":
        return default
    if isinstance(value, list):
        return ", ".join(str(item) for item in value if str(item).strip()) or default
    text = str(value).strip()
    return text or default


def normalize_manifest(value: object) -> tuple[dict[str, list[str]], list[str]]:
    manifest: dict[str, list[str]] = {"docs": [], "code": [], "evidence": []}
    warnings: list[str] = []
    if value is None or value == "":
        return manifest, warnings
    if not isinstance(value, dict):
        return manifest, ["context_manifest 应为对象"]

    for bucket in manifest:
        if bucket not in value:
            continue
        manifest[bucket] = normalize_list(value.get(bucket))
    extra_keys = sorted(key for key in value if key not in manifest)
    if extra_keys:
        warnings.append(f"context_manifest 包含未识别字段：{', '.join(extra_keys)}")
    return manifest, warnings


def parse_json_block(text: str, heading: str) -> tuple[dict[str, object], list[str]]:
    pattern = rf"(?s)^## {re.escape(heading)}\s*```json\s*(.*?)\s*```"
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        return {}, [f"缺少 `{heading}` JSON 块"]
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        return {}, [f"JSON 无法解析：{exc.msg}"]
    if not isinstance(data, dict):
        return {}, ["JSON 顶层必须是对象"]
    return data, []


def canonical_phase(value: object) -> str:
    text = str(value or "").strip().lower()
    if not text or text in {MISSING.lower(), "not provided", "未提供"}:
        return "unknown"
    if any(token in text for token in ("report", "issue-report", "repro", "报告")):
        return "report"
    if any(token in text for token in ("analysis", "analyse", "analyze", "分析")):
        return "analysis"
    if any(token in text for token in ("fix", "修复")):
        return "fix"
    if any(token in text for token in ("roadmap", "路线图")):
        return "roadmap"
    if any(token in text for token in ("design", "设计")):
        return "design"
    if any(token in text for token in ("implement", "implementation", "实现", "开发")):
        return "implement"
    if any(token in text for token in ("accept", "验收")):
        return "accept"
    if any(token in text for token in ("handoff", "交接", "transfer")):
        return "handoff"
    if any(token in text for token in ("sediment", "沉淀", "learn", "knowledge", "知识")):
        return "sediment"
    return "unknown"


def recommended_phase(next_action: object, stage: object | None = None) -> str:
    phase = canonical_phase(next_action)
    if phase == "unknown" and stage is not None:
        phase = canonical_phase(stage)
    return phase


def recommended_skill(next_action: object, stage: object | None = None) -> str:
    phase = recommended_phase(next_action, stage)
    return PHASE_SKILL_MAP.get(phase, "rs-handoff")


def load_current_work_state(root: Path, path: Path | None = None) -> CurrentWorkState:
    state_path = path or DEFAULT_STATE_PATH
    if not state_path.is_absolute():
        state_path = root / state_path
    if not state_path.exists() or not state_path.is_file():
        return CurrentWorkState(state_path, False, {}, [f"{state_path}: current-work-state 不存在"])

    text = state_path.read_text(encoding="utf-8", errors="replace").strip()
    data, warnings = parse_json_block(text, STATE_HEADING)
    if not data:
        warnings.append(f"{state_path}: 缺少机器可读状态块")
    data.setdefault("schema_version", STATE_SCHEMA_VERSION)
    if not data.get("work_id") and data.get("id"):
        data["work_id"] = data["id"]
    if not data.get("id") and data.get("work_id"):
        data["id"] = data["work_id"]
    linked_docs = normalize_list(data.get("linked_docs") or data.get("backlinks"))
    manifest, manifest_warnings = normalize_manifest(data.get("context_manifest"))
    data["linked_docs"] = linked_docs
    data["backlinks"] = linked_docs
    data["context_manifest"] = manifest
    warnings.extend(manifest_warnings)
    if not text_value(data, "next_skill", "").strip():
        data["next_skill"] = recommended_skill(data.get("next_action"), data.get("stage"))
    if text_value(data, "status", "").strip().lower() == "finished":
        warnings.append("current-work-state 已结束，不能作为 active state 继续认领")
    return CurrentWorkState(state_path, True, data, warnings)


def _relative_path(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def summarize_current_work_state(
    state: CurrentWorkState,
    root: Path,
    current_fingerprint: str | None = None,
) -> dict[str, object]:
    data = state.data
    linked_docs = normalize_list(data.get("linked_docs") or data.get("backlinks"))
    context_manifest, manifest_warnings = normalize_manifest(data.get("context_manifest"))
    warnings = [*state.warnings, *manifest_warnings]
    stored_fingerprint = text_value(data, "evidence_fingerprint")
    current = current_fingerprint or MISSING
    fresh = False
    fresh_reason = "missing current-work-state"
    if state.present:
        if stored_fingerprint == MISSING:
            fresh_reason = "missing evidence_fingerprint"
        elif current_fingerprint in {None, "", MISSING}:
            fresh_reason = "missing current fingerprint"
        else:
            fresh = stored_fingerprint == current_fingerprint
            fresh_reason = "matching fingerprint" if fresh else "fingerprint mismatch"

    work_id = text_value(data, "work_id", text_value(data, "id"))
    record_id = text_value(data, "id", work_id)
    stage = text_value(data, "stage")
    status = text_value(data, "status", "unknown")
    is_finished = status.strip().lower() == "finished"
    lifecycle_state = "finished" if is_finished else ("active" if state.present else "missing")
    next_action = text_value(data, "next_action")
    next_phase = recommended_phase(next_action, stage)
    next_skill = text_value(data, "next_skill", "").strip()
    if not next_skill or next_skill == MISSING:
        next_skill = PHASE_SKILL_MAP.get(next_phase, "rs-handoff")

    return {
        "schema_version": int(data.get("schema_version", STATE_SCHEMA_VERSION) or STATE_SCHEMA_VERSION),
        "path": _relative_path(state.path, root),
        "present": state.present,
        "fresh": fresh,
        "fresh_reason": fresh_reason,
        "id": record_id,
        "work_id": work_id,
        "stage": stage,
        "owner": text_value(data, "owner"),
        "next_action": next_action,
        "next_phase": next_phase,
        "next_skill": next_skill,
        "status": status,
        "lifecycle_state": lifecycle_state,
        "active": state.present and not is_finished,
        "is_finished": is_finished,
        "claimed_by": text_value(data, "claimed_by"),
        "claimed_at": text_value(data, "claimed_at"),
        "finished_by": text_value(data, "finished_by"),
        "finished_at": text_value(data, "finished_at"),
        "closed_by": text_value(data, "closed_by"),
        "closed_at": text_value(data, "closed_at"),
        "updated_at": text_value(data, "updated_at"),
        "source_snapshot": text_value(data, "source_snapshot"),
        "source_snapshot_fingerprint": text_value(data, "source_snapshot_fingerprint"),
        "evidence_fingerprint": stored_fingerprint,
        "current_fingerprint": current,
        "linked_docs": linked_docs,
        "backlinks": linked_docs,
        "context_manifest": context_manifest,
        "context_manifest_present": any(context_manifest[bucket] for bucket in ("docs", "code", "evidence")),
        "notes": normalize_list(data.get("notes")),
        "warnings": warnings,
    }


def _bullet_block(items: list[str], empty: str = MISSING) -> str:
    if not items:
        return f"- {empty}"
    return "\n".join(f"- {item}" for item in items)


def render_current_work_state(summary: dict[str, object]) -> str:
    generated_at = summary.get("updated_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_fingerprint = summary.get("current_fingerprint", MISSING)
    fresh = summary.get("fresh")
    if summary.get("present"):
        freshness = "fresh" if fresh else "stale"
    else:
        freshness = MISSING
    manifest = summary.get("context_manifest", {"docs": [], "code": [], "evidence": []})
    if not isinstance(manifest, dict):
        manifest = {"docs": [], "code": [], "evidence": []}
    docs = normalize_list(manifest.get("docs"))
    code = normalize_list(manifest.get("code"))
    evidence = normalize_list(manifest.get("evidence"))
    notes = normalize_list(summary.get("notes"))
    linked_docs = normalize_list(summary.get("linked_docs"))
    warnings = normalize_list(summary.get("warnings"))

    return f"""# Current Work State: {summary.get("id", summary.get("work_id", MISSING))}

生成时间：{generated_at}

## 0. 机器可读状态
```json
{json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)}
```

## 1. 当前状态
- ID：{summary.get("id", MISSING)}
- 工作 ID：{summary.get("work_id", MISSING)}
- 阶段：{summary.get("stage", MISSING)}
- 负责人：{summary.get("owner", MISSING)}
- 下一步：{summary.get("next_action", MISSING)}
- 下一阶段：{summary.get("next_phase", MISSING)}
- 推荐 skill：{summary.get("next_skill", MISSING)}
- 状态：{summary.get("status", MISSING)}
- 生命周期：{summary.get("lifecycle_state", MISSING)}
- 认领人：{summary.get("claimed_by", MISSING)}
- 认领时间：{summary.get("claimed_at", MISSING)}
- 证据指纹：{summary.get("evidence_fingerprint", MISSING)}
- 当前指纹：{current_fingerprint}
- 新鲜度：{freshness}

## 2. 关联 docs
{_bullet_block(linked_docs)}

## 3. Context Manifest
- docs：
{_bullet_block(docs, empty=MISSING)}
- code：
{_bullet_block(code, empty=MISSING)}
- evidence：
{_bullet_block(evidence, empty=MISSING)}

## 4. 备注
{_bullet_block(notes)}

## 5. 警告
{_bullet_block(warnings)}
"""


def write_current_work_state(path: Path, summary: dict[str, object]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = render_current_work_state(summary)
    temp_path = path.with_name(f"{path.name}.tmp")
    temp_path.write_text(content, encoding="utf-8")
    temp_path.replace(path)
    return path
