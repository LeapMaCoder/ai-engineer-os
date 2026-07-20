# 05_ADR — Architecture Decision Records

## Purpose

Record **important technical decisions** and their rationale so future humans and AI agents do not reverse them silently.

## When to write an ADR

- Choosing or changing a major dependency / platform
- Changing system boundaries or data ownership
- Security, privacy, or compliance-impacting decisions
- Anything hard to reverse or costly to revisit

## Rules

- ADRs are append-only in spirit: supersede with a new ADR, do not rewrite history.
- Link related Architecture docs and Specs.
- Status values: Proposed | Accepted | Deprecated | Superseded

## Templates

Use `docs/templates/ADR_Template.md`.
