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
6. The local 25-task suite must be reported separately from third-party
   authoritative suites.
7. RelayStack handoff claims on third-party suites must keep the upstream task
   and oracle unchanged; RelayStack may only add the A/B handoff protocol and
   extra continuation metrics.

Non-goal:

- Do not reimplement the official SWE-bench Docker harness in the local
  RelayStack runner.
- Do not claim official third-party benchmark scores from manifest-only
  adoption.
