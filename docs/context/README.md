# Context Attractor

This directory is the mandatory project-wide context entry point that future
people or agents must read before changing the repository. The other owner
directories are lazy inputs and are read only when a task touches their scope.

Keep:

- source-of-truth rules
- project-wide constraints
- verification commands that are known to work
- current collaboration assumptions
- settled decisions from `rs-decide` that every future session must know
- durable recipes from `rs-trick` when they affect normal project work
- guide content from `rs-guide` when it is about setup or contribution flow

A fact belongs here only when it is a repository-wide rule, constraint,
contribution convention, or mandatory verification contract. Do not copy
requirements, feature behavior, backlog items, or architecture descriptions
here; link to their canonical owner when context needs to point at them.

Do not keep:

- chat summaries
- temporary plans
- full debug logs
- one-off agent scratch notes

Typical writers: `rs-onboard`, `rs-decide`, `rs-trick`, `rs-guide`,
`rs-explore` when a finding becomes source-of-truth context.
