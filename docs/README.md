# docs/ — LeapMa Source of Truth

`docs/` is the **Source of Truth** for LeapMa.

Code does not define product intent. Documents do.

## Authority chain

```text
Vision
  → Product
    → Specification
      → Architecture
        → Code
          → Test
```

| Layer | Meaning | Directory |
|------|---------|-----------|
| Vision | Why LeapMa exists; long-term north star | `00_Vision/` |
| Product | Who we serve; problems & outcomes | `02_Product/` (informed by `01_Research/`) |
| Specification | Exact behavior to build & verify | `03_Specifications/` |
| Architecture | How the system realizes the specs | `04_Architecture/` + `05_ADR/` |
| Code | Implementation of approved specs/architecture | `apps/`, `services/`, `packages/` |
| Test | Proof that code matches specs | `tests/` + `08_Testing/` |

### Non-negotiable rules

1. **No feature code** without a corresponding Product definition and Specification.
2. **No architecture change** without updating Architecture docs; significant choices need an ADR.
3. **Tests assert Specifications**, not implementation whims.
4. If code and docs disagree, **docs win until intentionally revised** via SDD process.
5. Research informs Product; it does not authorize implementation by itself.

## Directory map

| Folder | Role |
|--------|------|
| `00_Vision` | Mission, principles, north-star outcomes |
| `01_Research` | Market, competitor, user, tech research |
| `02_Product` | PRDs, personas, journeys, success metrics |
| `03_Specifications` | Functional / non-functional / AI behavior specs |
| `04_Architecture` | System design, boundaries, data & AI design |
| `05_ADR` | Architecture Decision Records |
| `06_Sprint` | Sprint goals, plans, notes |
| `07_Development` | Workflow, AI roles, engineering practices |
| `08_Testing` | Test strategy, plans, quality gates |
| `09_Release` | Release notes, checklists, rollout |
| `10_Operations` | Runbooks, monitoring, incident process |
| `Archive` | Superseded docs (keep history, do not delete casually) |
| `templates/` | Obsidian-friendly SDD templates |

## How to add work

1. Copy a template from `templates/`.
2. Place it in the correct numbered folder.
3. Link upstream docs (Vision → Product → Spec → Architecture).
4. Only then open implementation tasks.
