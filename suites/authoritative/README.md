# Authoritative Benchmark Suites

This directory records third-party or externally traceable benchmark suites.

The repo does not vendor large external datasets here. Each suite manifest must
point to the upstream dataset or harness, name its license, and define how every
task instance exposes provenance.

Current suites:

- `swe-bench-lite.json`: adopts SWE-bench Lite as the authority target for
  repository-level software engineering tasks.
- `multi-swe-bench.json`: adopts Multi-SWE-bench as the better-fit authority
  target for RelayStack handoff experiments because it keeps third-party
  software tasks and adds multilingual coverage, including JavaScript and
  TypeScript.

Local RelayStack fixtures are tracked separately in `../local-25.json`. Do not
describe those 25 tasks as a third-party authoritative suite.
