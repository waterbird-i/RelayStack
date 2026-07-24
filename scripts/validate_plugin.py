#!/usr/bin/env python3
"""Validate RelayStack's Codex plugin package and skill metadata."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
SKILLS_ROOT = ROOT / "skills"


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError(f"{path}: unterminated YAML frontmatter")

    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def validate() -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid plugin manifest: {exc}"]

    if manifest.get("name") != "relaystack":
        errors.append("plugin name must be relaystack")
    if manifest.get("skills") != "./skills/":
        errors.append("plugin skills must be ./skills/")

    skill_dirs = sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append("no skill directories found")

    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{skill_dir.name}: missing SKILL.md")
            continue
        try:
            metadata = parse_frontmatter(skill_file)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if metadata.get("name") != skill_dir.name:
            errors.append(f"{skill_file}: frontmatter name must be {skill_dir.name}")
        if not metadata.get("description"):
            errors.append(f"{skill_file}: missing description")

        text = skill_file.read_text(encoding="utf-8")
        if re.search(r"python3\s+skills/rs-[^\s`]+", text):
            errors.append(f"{skill_file}: contains repo-relative skill path")

    if (SKILLS_ROOT / "rs.zip").exists():
        errors.append("obsolete skills/rs.zip must be removed")
    return errors


def main() -> None:
    errors = validate()
    if errors:
        for error in errors:
            print(f"error: {error}")
        raise SystemExit(1)
    print("plugin validation ok")


if __name__ == "__main__":
    main()
