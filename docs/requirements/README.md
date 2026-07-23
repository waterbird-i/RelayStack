# Requirements Attractor

This directory is created when a reusable, long-lived capability contract
changes. It holds settled capability goals, user-visible behavior, and
acceptance constraints. It describes what must be true, not how the system is
implemented.

Keep:

- capability goals
- user-visible behavior
- acceptance criteria
- explicit non-goals
- durable changes to capability or acceptance constraints discovered during fixes
- settled product or capability decisions from `rs-decide`

Do not keep:

- raw ideas
- duplicate design details
- temporary debugging hypotheses

Typical writers: `rs-req`, or a terminal `rs-feat-accept` / `rs-issue-fix`
decision that identifies a changed reusable capability contract. `rs-decide`
may write here when a settled decision changes that boundary; `rs-feat-design`
links an existing requirement or routes explicitly to `rs-req`, but does not
create one as a side effect.

Put approved feature flows and interaction details in `docs/design/`, and put
technical structure or integration contracts in `docs/architecture/`. Link to
those owners instead of duplicating their content here.
