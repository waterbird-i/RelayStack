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
DEPS = "/private/tmp/multi-swe-bench:/private/tmp/multi-swe-bench-deps"
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


def load_sample_ids(path: Path) -> list[str]:
    ids: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if not text or text.startswith("#"):
            continue
        if text.startswith("{"):
            row = json.loads(text)
            if not isinstance(row, dict) or not row.get("instance_id"):
                raise SystemExit(f"{path}: JSONL rows must contain instance_id")
            ids.append(str(row["instance_id"]))
        else:
            ids.append(text)
    return ids


def load_instances(instance_ids: list[str], pythonpath: str) -> list[dict[str, object]]:
    wanted = set(instance_ids)
    found: list[dict[str, object]] = []
    code = f"""
import json
from datasets import load_dataset
ds = load_dataset({DATASET_NAME!r}, split='train', streaming=True)
wanted = {sorted(wanted)!r}
seen = set()
for row in ds:
    if row.get('instance_id') in wanted:
        print(json.dumps(row, ensure_ascii=False))
        seen.add(row.get('instance_id'))
        if seen == set(wanted):
            break
missing = sorted(set(wanted) - seen)
if missing:
    raise SystemExit('target instances not found: ' + ', '.join(missing))
"""
    env = os.environ.copy()
    env["PYTHONPATH"] = pythonpath
    result = run(["python3", "-c", code], ROOT, env=env, timeout=180)
    if result.returncode != 0:
        raise SystemExit(result.stdout)
    for line in result.stdout.splitlines():
        if line.startswith("{"):
            row = json.loads(line)
            if isinstance(row, dict):
                found.append(row)
    return found


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
    return "\n".join(
        [
            f"任务：修复 Multi-SWE-bench 实例 {instance['instance_id']}。",
            f"仓库：{instance['org']}/{instance['repo']}。",
            f"上游标题：{instance['title']}",
            f"语言：{instance.get('language', 'unknown')}；难度：{instance.get('difficulty', 'unknown')}。",
            "已知事实：只以上游 problem statement、仓库代码和最小相关验证为准。",
            "建议验证：优先运行与修改文件最接近的测试；最终以 Multi-SWE-bench 官方 harness 为准。",
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
    parser.add_argument("--instance-id", action="append", dest="instance_ids", help="Multi-SWE instance id. Repeat for multiple samples.")
    parser.add_argument("--sample-file", type=Path, help="Plain text or JSONL file containing instance_id values.")
    parser.add_argument("--multi-swe-pythonpath", default=os.environ.get("MULTI_SWE_PYTHONPATH", DEPS))
    args = parser.parse_args()

    out = ROOT / args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    instance_ids = list(args.instance_ids or [])
    if args.sample_file:
        instance_ids.extend(load_sample_ids(args.sample_file))
    if not instance_ids:
        instance_ids = [TARGET_INSTANCE]
    instances = load_instances(instance_ids, args.multi_swe_pythonpath)
    (out / "dataset.jsonl").write_text(
        "".join(json.dumps(instance, ensure_ascii=False) + "\n" for instance in instances),
        encoding="utf-8",
    )

    summary: dict[str, object] = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "dataset": DATASET_NAME,
        "instance_ids": [instance["instance_id"] for instance in instances],
        "groups": {},
    }
    for group in ["baseline", "relaystack_handoff"]:
        agent_output_path = out / f"{group}-agent-output.jsonl"
        patch_path = out / f"{group}.patch"
        prediction_path = out / f"{group}.jsonl"
        agent_output_path.write_text("", encoding="utf-8")
        patch_path.write_text("", encoding="utf-8")
        prediction_path.write_text("", encoding="utf-8")
        runs: list[dict[str, object]] = []
        started = time.monotonic()
        for instance in instances:
            work = Path(tempfile.mkdtemp(prefix=f"multi-swe-{group}-"))
            repo = clone_repo(instance, work)
            codex_home = make_codex_home(group)
            handoff = make_handoff(instance, repo) if group == "relaystack_handoff" else None
            if handoff:
                with (out / "handoff.md").open("a", encoding="utf-8") as stream:
                    stream.write(f"## {instance['instance_id']}\n\n{handoff}\n\n")
            prompt = write_prompt(group, instance, repo, handoff)
            code, output, elapsed = run_codex(repo, prompt, codex_home)
            fix = diff(repo)
            with agent_output_path.open("a", encoding="utf-8") as stream:
                stream.write(output)
            with patch_path.open("a", encoding="utf-8") as stream:
                stream.write(f"# {instance['instance_id']}\n{fix}\n")
            with prediction_path.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(patch_row(instance, fix), ensure_ascii=False) + "\n")
            runs.append(
                {
                    "instance_id": instance["instance_id"],
                    "agent_returncode": code,
                    "elapsed_seconds": elapsed,
                    "workdir": str(work),
                    "codex_home": str(codex_home),
                    "diff_bytes": len(fix.encode("utf-8")),
                    "has_patch": bool(fix.strip()),
                }
            )
        summary["groups"][group] = {
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "runs": runs,
            "patch_file": str(prediction_path.relative_to(ROOT)),
            "diff_bytes": sum(int(run["diff_bytes"]) for run in runs),
            "has_patch": any(bool(run["has_patch"]) for run in runs),
            "agent_metrics": summarize_agent_output(agent_output_path.read_text(encoding="utf-8"), group),
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
