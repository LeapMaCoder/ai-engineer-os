# packages/

Shared libraries and contracts for the monorepo.

## Purpose

- Reusable code shared by `apps/` and `services/` (types, UI primitives, utilities, clients).
- Reduce duplication once multiple consumers exist.

## Rules

- Follow Rule of Three: do not extract a package until reuse is real.
- Do not invent package layout or tech stack in Phase 0.
- Packages must not depend on `apps/` or `services/` (dependency arrow points inward to packages).

## Status

Phase 0 placeholder. No packages created yet.
