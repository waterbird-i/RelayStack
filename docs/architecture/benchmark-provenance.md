---
doc_type: architecture
slug: benchmark-provenance
component: relaystack-benchmark
status: current
---

# Benchmark Provenance Architecture

The local task format stays small:

```text
tasks/task-xxx/
├── initial-repo/
├── instruction.md
├── handoff.md
├── test.sh
└── provenance.json   # optional
```

`runners/_runner.py` is the single report boundary. It reads
`provenance.json` once per task and copies that object into:

- the normal JSONL result row
- blind `raw-runs.jsonl`
- blind `packets.jsonl`
- blind `debug-packets.jsonl`

Authoritative third-party suites are tracked separately:

```text
suites/authoritative/
├── swe-bench-lite.json
└── multi-swe-bench.json
```

Those manifests declare authority, license, citation, and field mapping. They do
not make local benchmark runs equivalent to official upstream scores until the
official harness evaluates compatible predictions.

The local 25-task benchmark is tracked as a local suite:

```text
suites/local-25.json
```

It is a mixed baseline: `task-001..005` are public-PR-derived fixtures, while
`task-006..025` are project-authored scenarios. Reports must not merge this
local suite into third-party authoritative results.
