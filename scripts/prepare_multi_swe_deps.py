#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path


DEPS = Path("/private/tmp/multi-swe-bench-deps")
REPO = Path("/private/tmp/multi-swe-bench")
UPSTREAM = "https://github.com/multi-swe-bench/multi-swe-bench.git"


def run(command: list[str], cwd: Path | None = None) -> None:
    result = subprocess.run(command, cwd=cwd, text=True)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def module_exists(name: str, paths: list[Path]) -> bool:
    old_path = list(sys.path)
    sys.path[:0] = [str(path) for path in paths]
    try:
        return importlib.util.find_spec(name) is not None
    finally:
        sys.path = old_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare temporary Multi-SWE-bench Python deps without installing into the global environment.")
    parser.add_argument("--case-sensitive-root", type=Path, help="Case-sensitive volume root, for example /Volumes/RelayStackCase.")
    parser.add_argument("--deps", type=Path)
    parser.add_argument("--repo", type=Path)
    args = parser.parse_args()

    deps = args.deps or ((args.case_sensitive_root / "multi-swe-bench-deps") if args.case_sensitive_root else DEPS)
    repo = args.repo or ((args.case_sensitive_root / "multi-swe-bench") if args.case_sensitive_root else REPO)

    deps.mkdir(parents=True, exist_ok=True)
    if not repo.exists():
        run(["git", "clone", "--depth", "1", UPSTREAM, str(repo)])
    run([sys.executable, "-m", "pip", "install", "--target", str(deps), "datasets", str(repo)])
    paths = [repo, deps]
    missing = [name for name in ["datasets", "multi_swe_bench"] if not module_exists(name, paths)]
    if missing:
        raise SystemExit("missing modules after install: " + ", ".join(missing))
    print(":".join(str(path) for path in paths))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
