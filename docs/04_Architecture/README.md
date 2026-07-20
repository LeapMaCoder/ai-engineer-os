# 04_Architecture

## Purpose

Describe **how** the system realizes approved Specifications.

Architecture sits between Spec and Code:

Vision → Product → Specification → **Architecture** → Code → Test

## Contains

- System context and container diagrams
- Service / app boundaries
- Data flow and trust boundaries
- AI agent topology (when relevant)
- Cross-cutting concerns (authn/z, observability, tenancy) at design level

## Rules

- Architecture must map to Specifications (traceability).
- Significant choices require an ADR in `05_ADR/`.
- Do not select stacks casually in chat — record them here + ADR.
- No “architecture by PR” without docs update.

## Templates

Use `docs/templates/Architecture_Template.md`.
