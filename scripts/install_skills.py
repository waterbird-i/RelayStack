#!/usr/bin/env python3
"""Install selected RelayStack skills into a Codex skills directory."""

from __future__ import annotations

import argparse
import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Skill:
    name: str
    path: Path


def default_dest() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills"
    return Path.home() / ".codex" / "skills"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def discover_skills(root: Path) -> list[Skill]:
    skills_root = root / "skills"
    skills = [
        Skill(path.name, path)
        for path in sorted(skills_root.iterdir())
        if path.is_dir() and (path / "SKILL.md").is_file()
    ]
    if not skills:
        raise SystemExit(f"No skills found under {skills_root}")
    return skills


def parse_selection(raw: str, count: int) -> list[int]:
    text = raw.strip().lower()
    if text in {"all", "*"}:
        return list(range(count))

    selected: set[int] = set()
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            left, right = part.split("-", 1)
            start, end = int(left), int(right)
            if start > end:
                raise ValueError(f"invalid range: {part}")
            selected.update(range(start - 1, end))
        else:
            selected.add(int(part) - 1)

    if not selected:
        raise ValueError("empty selection")
    if min(selected) < 0 or max(selected) >= count:
        raise ValueError(f"selection must be between 1 and {count}")
    return sorted(selected)


def choose_skills(
    skills: list[Skill],
    select_all: bool,
    raw_selection: str | None,
) -> list[Skill]:
    if select_all:
        return skills

    for index, skill in enumerate(skills, 1):
        print(f"{index:2d}. {skill.name}")

    raw = raw_selection
    if raw is None:
        raw = input("\nInstall which skills? Use numbers like 1,3-5, or all: ")
    indexes = parse_selection(raw, len(skills))
    return [skills[index] for index in indexes]


def install_skills(skills: list[Skill], dest: Path, force: bool) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for skill in skills:
        target = dest / skill.name
        if target.exists():
            if not force:
                print(f"skip   {skill.name} (already exists)")
                continue
            shutil.rmtree(target)
        shutil.copytree(skill.path, target)
        print(f"install {skill.name} -> {target}")


def self_test() -> None:
    assert parse_selection("all", 3) == [0, 1, 2]
    assert parse_selection("*", 2) == [0, 1]
    assert parse_selection("1,3-4", 4) == [0, 2, 3]
    try:
        parse_selection("0", 2)
    except ValueError:
        pass
    else:
        raise AssertionError("out-of-range selection should fail")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        skill_dir = root / "skills" / "rs-demo"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            "---\nname: rs-demo\n---\n",
            encoding="utf-8",
        )
        dest = root / "dest"
        skills = discover_skills(root)
        install_skills(skills, dest, force=False)
        assert (dest / "rs-demo" / "SKILL.md").is_file()

    print("self-test ok")


def main() -> None:
    parser = argparse.ArgumentParser(description="Install RelayStack skills.")
    parser.add_argument("--all", action="store_true", help="install every skill")
    parser.add_argument("--select", help="selection like 1,3-5 or all")
    parser.add_argument(
        "--dest",
        type=Path,
        default=default_dest(),
        help="target skills directory",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace existing target skill folders",
    )
    parser.add_argument("--list", action="store_true", help="list available skills and exit")
    parser.add_argument("--self-test", action="store_true", help="run a small self-check")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    skills = discover_skills(repo_root())
    if args.list:
        for skill in skills:
            print(skill.name)
        return

    try:
        selected = choose_skills(skills, select_all=args.all, raw_selection=args.select)
    except ValueError as exc:
        raise SystemExit(f"Invalid selection: {exc}") from exc
    install_skills(selected, args.dest.expanduser(), args.force)


if __name__ == "__main__":
    main()
