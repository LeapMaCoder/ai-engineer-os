# services/

Backend and AI runtime services live here.

## Purpose

- Host APIs, workers, and AI agent services.
- Separate deployable units from shared libraries (`packages/`) and clients (`apps/`).

## Rules

- No service implementation before Product Definition → Specification → Architecture → ADR (when needed).
- Prefer clear service boundaries over premature microservices.
- Cross-cutting contracts (types, OpenAPI, events) should eventually live in `packages/` once decided by Architecture.

## Status

Phase 0 placeholder. No services created yet.
