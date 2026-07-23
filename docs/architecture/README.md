# Architecture Attractor

This directory is created or updated after implementation when real module
boundaries, data flows, or integration contracts change. It holds the current
technical structure and describes how the implemented system is organized, not
the product behavior it should provide.

Keep:

- system baseline
- module ownership
- data flow and integration contracts
- constraints exposed by debugging
- architecture changes caused by features
- source-backed findings from `rs-explore` only when they establish current
  technical structure or boundaries
- settled architecture decisions from `rs-decide`
- public API or command reference from `rs-libdoc` only when it documents an
  architecture-facing interface
- reusable implementation patterns from `rs-trick` only when they are
  architecture constraints or integration conventions

Do not keep:

- stack traces
- local experiment notes
- personal investigation logs

Typical writers: `rs-arch`, or a terminal `rs-feat-accept` / `rs-issue-fix`
decision that identifies a real implemented boundary. `rs-explore`,
`rs-decide`, `rs-trick`, or `rs-libdoc` may write here only when their evidence
establishes current technical structure or an integration contract.

Keep capability goals and acceptance constraints in `docs/requirements/`, and
approved feature behavior in `docs/design/`. Link to those owners instead of
restating them here.
