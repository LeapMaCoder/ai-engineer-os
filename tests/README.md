# tests/

Cross-cutting automated tests that do not belong to a single app or service.

## Purpose

- Integration, end-to-end, contract, and smoke tests spanning multiple components.
- Unit tests generally live next to the code they cover inside `apps/`, `services/`, or `packages/`.

## Rules

- Tests follow Specifications: behavior under test must be specified first.
- Prefer documenting test strategy in `docs/08_Testing/` before adding large suites.
- Do not invent a test framework choice without Architecture / ADR.

## Status

Phase 0 placeholder. No test suites yet.
