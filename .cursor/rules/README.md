# Cursor Rules — LeapMa

Rules guide Cursor agents. They do **not** replace `docs/` Source of Truth.

## Rule domains

| Domain | Responsibility |
|--------|----------------|
| `global/` | SDD principles, monorepo boundaries, collaboration defaults |
| `product/` | Demand clarity & user value; forbid jumping to code |
| `architecture/` | Design integrity, ADR requirement, no silent stack choices |
| `backend/` | Service implementation constraints (when coding is authorized) |
| `frontend/` | App/UI implementation constraints (when coding is authorized) |
| `ai/` | AI mentor/agent behavior and safety constraints |
| `testing/` | Spec-linked quality gates |
| `review/` | What to check before merge |

## Activation model

- Prefer narrow rules for scoped work.
- Global rules always apply.
- Product/Architecture rules apply before any implementation rule.

## Authority

If a rule conflicts with an accepted doc in `docs/`, **update the rule** — docs remain Source of Truth.
