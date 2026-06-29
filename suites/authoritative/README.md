# Authoritative Benchmark Suites

This directory records third-party or externally traceable benchmark suites.

The repo does not vendor large external datasets here. Each suite manifest must
point to the upstream dataset or harness, name its license, and define how every
task instance exposes provenance.

Current suite:

- `swe-bench-lite.json`: adopts SWE-bench Lite as the authority target for
  repository-level software engineering tasks.
