---
name: rs-feat-accept
description: Validate feature implementation against the approved design and update durable RelayStack attractor docs.
---

# RS Feat Accept

Use this skill after feature implementation.

## Workflow

1. Read the approved design note and current diff.
2. Verify behavior against acceptance criteria.
3. Check that non-goals stayed out.
4. Update only durable attractor docs:
   - `docs/backlog/`: status and verification
   - `docs/requirements/`: settled capability behavior
   - `docs/design/`: final user flow or app behavior
   - `docs/architecture/`: real module boundaries or contracts
5. Put detailed acceptance notes in personal project notes or `rs-handoff`.
6. Suggest `rs-learn`, `rs-trick`, `rs-decide`, `rs-guide`, or `rs-libdoc` only
   when the completed work created durable knowledge.

## Rules

- Do not treat passing tests as full acceptance.
- Do not leave stable facts only in personal notes.
- Do not update architecture with future target state.
