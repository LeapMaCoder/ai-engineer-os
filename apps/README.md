# apps/

User-facing applications live here.

## Purpose

- Host independently deployable clients (e.g. web, future mobile).
- Keep UI/runtime concerns out of `services/` and `packages/`.

## Rules

- Do **not** add app code until Specification + Architecture exist for that app.
- Each app should have its own `README.md` describing scope and ownership.
- Shared logic belongs in `packages/`, not copied across apps.

## Status

Phase 0 placeholder. No applications created yet.
