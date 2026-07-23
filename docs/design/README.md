# Design Attractor

This directory is created when implementation must be preceded by human
approval of behavior, state, permission, migration, terminology, or a solution
tradeoff. It holds approved feature behavior, user flows, and app-layer
interaction decisions. A design document is authoritative for how that feature
should behave after approval.

Keep:

- user flows
- supported states
- feature behavior
- UX and interaction decisions
- final feature behavior when it changes the approved user-facing contract
- stable user-facing flows that belong to a feature
- design patterns only when they define feature-level interaction behavior

Do not keep:

- transient mock notes
- implementation logs
- checklist progress

Typical writers: `rs-feat-design`, and a terminal `rs-feat-accept` or
`rs-issue-fix` decision only when an existing approved behavior must be
corrected. `rs-guide`, `rs-trick`, or `rs-decide` may write here only for a
stable feature-level interaction fact.

Do not copy capability goals from `docs/requirements/` or technical structure
from `docs/architecture/`. Link to those canonical owners when a design depends
on them.
