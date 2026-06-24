# Architecture Attractor

This directory holds stable technical structure and module boundaries.

Keep:

- system baseline
- module ownership
- data flow and integration contracts
- constraints exposed by debugging
- architecture changes caused by features
- source-backed findings from `rs-explore`
- settled architecture decisions from `rs-decide`
- public API or command reference from `rs-libdoc`
- reusable implementation patterns from `rs-trick`

Do not keep:

- stack traces
- local experiment notes
- personal investigation logs

Typical writers: `rs-arch`, `rs-feat-accept`, `rs-issue-fix`,
`rs-explore`, `rs-decide`, `rs-trick`, `rs-libdoc`.
