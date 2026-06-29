---
doc_type: requirement
slug: benchmark-provenance
component: relaystack-benchmark
status: current
---

# Benchmark Provenance Requirements

RelayStack benchmark reports must preserve task authority and provenance when a
task provides it.

Acceptance criteria:

1. A task may include `provenance.json` beside `instruction.md`.
2. Runner results include the full `provenance` object plus flattened fields for
   `suite_id`, `provenance_status`, `source_url`, `issue_url`, `pr_url`, and
   `license`.
3. Blind packets include provenance because source authority is not a runner
   identity and should be reviewable.
4. Third-party public suites live under `suites/authoritative/` as manifests,
   not vendored dataset copies.
5. A suite cannot be called authoritative unless it names the upstream dataset,
   license, citation, and per-instance provenance mapping.

Non-goal:

- Do not reimplement the official SWE-bench Docker harness in the local
  RelayStack runner.
