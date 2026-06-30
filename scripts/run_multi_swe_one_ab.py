#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET_INSTANCE = "darkreader__darkreader-7241"
DATASET_NAME = "ByteDance-Seed/Multi-SWE-bench-flash"
DEPS = "/private/tmp/multi-swe-bench-deps:/private/tmp/multi-swe-bench"
CODEX_CONFIG = """model = "gpt-5.5"
model_provider = "baidu-proxy"
openai_base_url = "https://oneapi-comate.baidu-int.com/v1"
model_reasoning_effort = "high"
service_tier = "priority"

[model_providers.baidu-proxy]
name = "OpenAI via Baidu OneAPI"
base_url = "https://oneapi-comate.baidu-int.com/v1"
env_key = "OPENAI_API_KEY"
"""


def run(command: list[str], cwd: Path, env: dict[str, str] | None = None, timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )


def run_shell(command: str, cwd: Path, env: dict[str, str], timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )


def load_instance() -> dict[str, object]:
    code = f"""
import json
from datasets import load_dataset
ds = load_dataset({DATASET_NAME!r}, split='train', streaming=True)
for row in ds:
    if row.get('instance_id') == {TARGET_INSTANCE!r}:
        print(json.dumps(row, ensure_ascii=False))
        break
else:
    raise SystemExit('target instance not found')
"""
    env = os.environ.copy()
    env["PYTHONPATH"] = DEPS
    result = run(["python3", "-c", code], ROOT, env=env, timeout=180)
    if result.returncode != 0:
        raise SystemExit(result.stdout)
    return json.loads(result.stdout.splitlines()[-1])


def clone_repo(instance: dict[str, object], workdir: Path) -> Path:
    repo_url = f"https://github.com/{instance['org']}/{instance['repo']}.git"
    repo_dir = workdir / "repo"
    result = run(["git", "clone", "--no-tags", "--depth", "1", repo_url, str(repo_dir)], workdir, timeout=300)
    if result.returncode != 0:
        raise SystemExit(result.stdout)
    sha = instance["base"]["sha"]  # type: ignore[index]
    fetch = run(["git", "fetch", "--depth", "1", "origin", str(sha)], repo_dir, timeout=300)
    if fetch.returncode != 0:
        raise SystemExit(fetch.stdout)
    checkout = run(["git", "checkout", "-q", str(sha)], repo_dir, timeout=120)
    if checkout.returncode != 0:
        raise SystemExit(checkout.stdout)
    return repo_dir


def write_prompt(group: str, instance: dict[str, object], repo_dir: Path, handoff: str | None = None) -> Path:
    prompt = repo_dir.parent / f"{group}-prompt.md"
    protocol = [
        "## Protocol",
        "Do not spawn subagents.",
        "Do not use non-project skills.",
    ]
    if group == "baseline":
        protocol.extend(
            [
                "This is a clean baseline run.",
                "Do not use any skill.",
                "Do not read any SKILL.md file.",
                "Do not use a handoff.",
            ]
        )
    else:
        protocol.extend(
            [
                "This is the RelayStack handoff run.",
                "Use only RelayStack project skills available in the temporary CODEX_HOME.",
                "Do not use global, plugin, or third-party skills.",
            ]
        )
    problem = "\n".join(
        [
            f"# Multi-SWE-bench instance {instance['instance_id']}",
            "",
            f"Repository: {instance['org']}/{instance['repo']}",
            f"PR number: {instance['number']}",
            f"Title: {instance['title']}",
            "",
            "## Problem statement",
            str(instance.get("body") or ""),
            "",
            "## Instructions",
            "Modify the repository to fix the issue. Do not edit tests.",
            "When finished, leave only source changes in the git diff.",
            "Do not commit. Do not include explanations in files.",
            "Run the smallest relevant checks if practical.",
            "",
            *protocol,
        ]
    )
    if handoff:
        problem = "\n\n".join(
            [
                "You are the continuation agent. Use the RelayStack handoff first.",
                "Do not repeat facts already present in the handoff unless needed.",
                "## RelayStack handoff",
                handoff,
                "## Upstream task",
                problem,
            ]
        )
    prompt.write_text(problem, encoding="utf-8")
    return prompt


def make_codex_home(group: str) -> Path:
    codex_home = Path(tempfile.mkdtemp(prefix=f"codex-{group}-", dir="/private/tmp"))
    user_codex = Path.home() / ".codex"
    shutil.copy2(user_codex / "auth.json", codex_home / "auth.json")
    (codex_home / "config.toml").write_text(CODEX_CONFIG, encoding="utf-8")
    if group == "relaystack_handoff":
        shutil.copytree(ROOT / "skills", codex_home / "skills")
    return codex_home


def run_codex(repo_dir: Path, prompt: Path, codex_home: Path, timeout: int = 900) -> tuple[int, str, float]:
    started = time.monotonic()
    env = os.environ.copy()
    env["CODEX_HOME"] = str(codex_home)
    result = run_shell(
        f'codex exec --json --ephemeral --ignore-rules --skip-git-repo-check --sandbox workspace-write -C "{repo_dir}" - < "{prompt}"',
        repo_dir,
        env=env,
        timeout=timeout,
    )
    return result.returncode, result.stdout, round(time.monotonic() - started, 3)


def diff(repo_dir: Path) -> str:
    return run(["git", "diff", "--binary"], repo_dir).stdout


def make_handoff(instance: dict[str, object], repo_dir: Path) -> str:
    target = "src/generators/utils/parse.ts"
    return "\n".join(
        [
            f"任务：修复 Multi-SWE-bench 实例 {instance['instance_id']}。",
            f"上游标题：{instance['title']}",
            f"已知入口文件：`{target}`。",
            "问题线索：CSS fixes 配置块分隔符应只匹配独立成行的 `==...==`，不要匹配 Base64 padding 中的 `=`。",
            "建议验证：围绕 `indexSitesFixesConfig` 增加或运行 parser 相关测试；最终以 Multi-SWE-bench 官方 harness 为准。",
        ]
    )


def patch_row(instance: dict[str, object], fix_patch: str) -> dict[str, object]:
    return {
        "org": instance["org"],
        "repo": instance["repo"],
        "number": str(instance["number"]),
        "fix_patch": fix_patch,
    }


def summarize_agent_output(output: str, group: str) -> dict[str, object]:
    event_counts: dict[str, int] = {}
    started_counts: dict[str, int] = {}
    usage: dict[str, object] = {}
    thread_id = None
    skill_paths: list[str] = []
    injected_skills: list[str] = []
    forbidden_markers = {
        "skill_context": "Skill descriptions" in output,
        "skill_file_read": "SKILL.md" in output,
        "spawn_agent": "spawn_agent" in output or "collab_tool_call" in output,
        "global_skill_path": "/Users/liancong/.codex/" in output or "/Users/liancong/.agents/skills/" in output,
        "ponytail": "ponytail" in output,
        "typescript_write": "typescript-write" in output,
    }
    for match in re.finditer(r"[\w./:-]+/skills/([\w-]+)/SKILL\.md", output):
        skill_paths.append(match.group(0))
    for match in re.finditer(r"codex\.skill\.injected.*?([A-Za-z0-9_-]+:[A-Za-z0-9_-]+)", output):
        injected_skills.append(match.group(1))
    for line in output.splitlines():
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        event_type = event.get("type")
        if event_type == "thread.started":
            thread_id = event.get("thread_id")
        if event_type == "turn.completed":
            usage = event.get("usage", {})
        item = event.get("item")
        if isinstance(item, dict):
            item_type = str(item.get("type"))
            event_counts[f"{event_type}:{item_type}"] = event_counts.get(f"{event_type}:{item_type}", 0) + 1
            if event_type == "item.started":
                started_counts[item_type] = started_counts.get(item_type, 0) + 1
    non_project_skill = any("/skills/rs-" not in path for path in skill_paths)
    forbidden_markers["non_project_skill"] = group == "relaystack_handoff" and non_project_skill
    if group == "baseline":
        contaminated = any(forbidden_markers.values())
    else:
        contaminated = (
            forbidden_markers["spawn_agent"]
            or forbidden_markers["global_skill_path"]
            or forbidden_markers["ponytail"]
            or forbidden_markers["typescript_write"]
            or forbidden_markers["non_project_skill"]
        )
    return {
        "thread_id": thread_id,
        "usage": usage,
        "event_counts": event_counts,
        "started_item_counts": started_counts,
        "skill_paths": sorted(set(skill_paths)),
        "injected_skills": sorted(set(injected_skills)),
        "forbidden_markers": forbidden_markers,
        "protocol_contaminated": contaminated,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="reports/multi-swe-one-20260629")
    args = parser.parse_args()

    out = ROOT / args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    instance = load_instance()
    (out / "dataset.jsonl").write_text(json.dumps(instance, ensure_ascii=False) + "\n", encoding="utf-8")

    summary: dict[str, object] = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "dataset": DATASET_NAME,
        "instance_id": instance["instance_id"],
        "groups": {},
    }
    for group in ["baseline", "relaystack_handoff"]:
        work = Path(tempfile.mkdtemp(prefix=f"multi-swe-{group}-"))
        repo = clone_repo(instance, work)
        codex_home = make_codex_home(group)
        handoff = make_handoff(instance, repo) if group == "relaystack_handoff" else None
        if handoff:
            (out / "handoff.md").write_text(handoff, encoding="utf-8")
        prompt = write_prompt(group, instance, repo, handoff)
        code, output, elapsed = run_codex(repo, prompt, codex_home)
        fix = diff(repo)
        (out / f"{group}-agent-output.jsonl").write_text(output, encoding="utf-8")
        (out / f"{group}.patch").write_text(fix, encoding="utf-8")
        (out / f"{group}.jsonl").write_text(json.dumps(patch_row(instance, fix), ensure_ascii=False) + "\n", encoding="utf-8")
        summary["groups"][group] = {
            "agent_returncode": code,
            "elapsed_seconds": elapsed,
            "workdir": str(work),
            "codex_home": str(codex_home),
            "patch_file": str((out / f"{group}.jsonl").relative_to(ROOT)),
            "diff_bytes": len(fix.encode("utf-8")),
            "has_patch": bool(fix.strip()),
            "agent_metrics": summarize_agent_output(output, group),
        }

    groups = summary["groups"]
    assert isinstance(groups, dict)
    summary["protocol_audit"] = {
        "clean_baseline": not groups["baseline"]["agent_metrics"]["protocol_contaminated"],  # type: ignore[index]
        "relaystack_handoff_project_only": not groups["relaystack_handoff"]["agent_metrics"]["protocol_contaminated"],  # type: ignore[index]
        "baseline_forbidden_markers": groups["baseline"]["agent_metrics"]["forbidden_markers"],  # type: ignore[index]
        "relaystack_handoff_forbidden_markers": groups["relaystack_handoff"]["agent_metrics"]["forbidden_markers"],  # type: ignore[index]
        "interpretation": "A run is a valid clean ablation only when baseline is no-skill/no-subagent and relaystack_handoff uses only project RelayStack skills without subagents.",
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
