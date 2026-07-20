# LeapMa

AI-native programmer growth platform.

LeapMa is **not** a traditional course marketplace. It helps programmers grow continuously through:

- AI mentors
- Dynamic learning paths
- Knowledge graphs
- Gamified progression

Inspired by the best traits of Boot.dev, Duolingo, Codecademy, LeetCode, DataCamp, and Mimo — rebuilt around long-term skill growth.

## Current stage

**Phase 0 — Project initialization & engineering system**

This repository currently contains:

- Monorepo skeleton
- Documentation system (`docs/` as Source of Truth)
- SDD templates
- Cursor rules
- AI team roles & development workflow

There is **no product feature code** yet.

## Development method

LeapMa uses **Specification Driven Development (SDD)**.

Source of Truth chain:

```text
Vision → Product → Specification → Architecture → Code → Test
```

Process:

```text
Idea → Research → Product → Spec → Architecture → Tasks
  → Implementation → Review → Testing → Release → Retro
```

See:

- [`docs/README.md`](docs/README.md)
- [`docs/07_Development/Development_Workflow.md`](docs/07_Development/Development_Workflow.md)
- [`docs/07_Development/AI_Team_Roles.md`](docs/07_Development/AI_Team_Roles.md)

## Repository layout

```text
LeapMa/
├── docs/              # Source of Truth (product + engineering docs)
├── apps/              # User-facing applications (future)
├── services/          # Backend & AI services (future)
├── packages/          # Shared libraries (future)
├── infrastructure/    # Docker / deploy / cloud (future)
├── tests/             # Cross-cutting tests (future)
├── scripts/           # Repo-level scripts (future)
├── .cursor/           # Cursor rules for AI-native development
├── .github/           # GitHub collaboration / CI (future)
├── .env.example       # Env var template (no secrets)
├── CHANGELOG.md
└── README.md
```

## Docs map (quick)

| Path | Role |
|------|------|
| `docs/00_Vision` | Why LeapMa exists |
| `docs/01_Research` | Evidence & competitor learning |
| `docs/02_Product` | PRDs / user value |
| `docs/03_Specifications` | Testable behavior contracts |
| `docs/04_Architecture` | System design |
| `docs/05_ADR` | Architecture decisions |
| `docs/06_Sprint` | Sprint planning |
| `docs/07_Development` | Workflow & AI roles |
| `docs/08_Testing` | Quality strategy |
| `docs/09_Release` | Shipping |
| `docs/10_Operations` | Run / operate |
| `docs/templates` | SDD templates (Obsidian-friendly) |

## Roadmap (high level)

1. **Phase 0 (now):** engineering system & docs foundation
2. **Phase 1:** Vision + Research + core Product definition
3. **Phase 2:** Foundational Specifications & Architecture (with ADRs)
4. **Phase 3:** First vertical slice implementation (mentor / path / progress — TBD by Specs)
5. **Phase 4+:** Expand graph, gamification, multi-surface clients, operations maturity

## Contributing (process)

1. Do not start with code.
2. Use templates under `docs/templates/`.
3. Link upstream docs.
4. Follow Cursor rules under `.cursor/rules/`.
5. Record significant decisions as ADRs.

## License

TBD
