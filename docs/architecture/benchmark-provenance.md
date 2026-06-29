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
└── swe-bench-lite.json
```

Those manifests declare authority, license, citation, and field mapping. They do
not make local benchmark runs equivalent to official upstream scores until the
official harness evaluates compatible predictions.
