# Backlog Attractor

This directory is created only when the team needs ongoing coordination of
priority, owner, status, or next action. It is not the full truth about a
requirement, feature design, or current implementation.

Keep:

- candidate features
- known issues worth fixing
- status and owner when known
- the smallest useful next action
- a short closure reference when the work is complete
- roadmap slices only when they represent team-visible priority

Do not keep:

- full implementation checklists
- abandoned brainstorming trails
- private agent task records

Typical writers: `rs-roadmap` when a team-visible coordination summary is
needed, `rs-brainstorm` after an idea is stable enough to enter team planning,
`rs-feat-accept`, or `rs-issue-fix` when their final Documentation Decision
identifies an ongoing team action.

Keep the canonical requirement in `docs/requirements/`, feature behavior in
`docs/design/`, and technical structure in `docs/architecture/`. Link to those
documents instead of copying their content into backlog entries.
