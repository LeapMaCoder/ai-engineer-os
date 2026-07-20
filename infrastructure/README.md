# infrastructure/

Infrastructure as Code, deployment, and cloud/runtime ops assets.

## Purpose

- Docker / compose definitions (when approved by Architecture).
- Deployment manifests, environments, and cloud infrastructure configs.
- Keep ops concerns out of application source trees.

## Rules

- No cloud vendor or orchestrator lock-in decisions without an ADR in `docs/05_ADR/`.
- Secrets never live here — use `.env` locally and a secrets manager in real environments.
- Changes here should reference the Architecture doc and relevant ADRs.

## Status

Phase 0 placeholder. No infrastructure defined yet.
