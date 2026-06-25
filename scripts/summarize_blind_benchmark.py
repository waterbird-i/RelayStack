#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def read_jsonl(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                data = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            if isinstance(data, dict):
                rows.append(data)
    return rows


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def runner_for(unblind: dict[str, object], pair_id: str, candidate_id: str) -> str:
    pair = unblind.get(pair_id, {})
    if not isinstance(pair, dict):
        return "unknown"
    value = pair.get(candidate_id, "unknown")
    if isinstance(value, dict):
        return str(value.get("runner", "unknown"))
    return str(value)


def score_winners(reviews: list[dict[str, object]]) -> dict[str, dict[str, str]]:
    by_reviewer_pair: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for review in reviews:
        reviewer = str(review.get("reviewer", "unknown"))
        pair_id = str(review.get("pair_id", "unknown"))
        by_reviewer_pair[(reviewer, pair_id)].append(review)

    winners: dict[str, dict[str, str]] = defaultdict(dict)
    for (reviewer, pair_id), rows in by_reviewer_pair.items():
        scored = [row for row in rows if isinstance(row.get("score"), (int, float))]
        if not scored:
            continue
        winner = max(scored, key=lambda row: float(row["score"]))
        winners[reviewer][pair_id] = str(winner.get("candidate_id", "unknown"))
    return winners


def pct(part: float, whole: float) -> str:
    return "0.0%" if whole == 0 else f"{part / whole * 100:.1f}%"


def build_summary(blind_dir: Path) -> str:
    raw_runs = read_jsonl(blind_dir / "raw-runs.jsonl")
    reviews = read_jsonl(blind_dir / "reviews.jsonl")
    unblind = read_json(blind_dir / "unblind-map.json")

    by_runner: dict[str, dict[str, float]] = defaultdict(lambda: {"runs": 0, "passed": 0, "seconds": 0, "tokens": 0})
    for row in raw_runs:
        runner = str(row.get("runner", "unknown"))
        by_runner[runner]["runs"] += 1
        by_runner[runner]["passed"] += 1 if row.get("passed") is True else 0
        by_runner[runner]["seconds"] += float(row.get("elapsed_seconds") or 0)
        by_runner[runner]["tokens"] += float(row.get("total_tokens") or 0)

    reviewer_wins: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for reviewer, winners in score_winners(reviews).items():
        for pair_id, candidate_id in winners.items():
            reviewer_wins[reviewer][runner_for(unblind, pair_id, candidate_id)] += 1

    lines = [
        "# Blind Benchmark Summary",
        "",
        "## Runner Totals",
        "",
        "| Runner | Runs | Pass Rate | Total Seconds | Total Tokens |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for runner, stats in sorted(by_runner.items()):
        lines.append(
            f"| `{runner}` | {int(stats['runs'])} | {pct(stats['passed'], stats['runs'])} | "
            f"{stats['seconds']:.3f} | {int(stats['tokens']):,} |"
        )

    lines.extend(["", "## Reviewer Wins", ""])
    if reviewer_wins:
        lines.extend(["| Reviewer | Runner | Wins |", "| --- | --- | ---: |"])
        for reviewer, counts in sorted(reviewer_wins.items()):
            for runner, wins in sorted(counts.items()):
                lines.append(f"| `{reviewer}` | `{runner}` | {wins} |")
    else:
        lines.append("No reviewer scores found.")

    missing = []
    for name in ["raw-runs.jsonl", "packets.jsonl", "debug-packets.jsonl", "reviews.jsonl", "unblind-map.json"]:
        if not (blind_dir / name).exists():
            missing.append(name)
    if missing:
        lines.extend(["", "## Missing Inputs", "", "- " + "\n- ".join(missing)])

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- `raw-runs.jsonl` is the only file that should expose real runner names.",
            "- Reviewer packets should stay anonymized until `unblind-map.json` is used by the aggregator.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize RelayStack blind benchmark results.")
    parser.add_argument("blind_dir", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    summary = build_summary(args.blind_dir)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(summary, encoding="utf-8")
    else:
        print(summary, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
