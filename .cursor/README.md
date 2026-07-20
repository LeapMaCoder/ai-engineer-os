# .cursor/

Cursor project configuration for LeapMa.

## Purpose

Encode AI-native engineering constraints so agents follow SDD by default.

## Layout

```text
.cursor/
└── rules/
    ├── global/         # Project-wide principles
    ├── product/        # Requirements & user value (no premature code)
    ├── architecture/   # Design & ADR discipline
    ├── backend/        # Services implementation constraints
    ├── frontend/       # Apps implementation constraints
    ├── ai/             # AI agent / mentor system constraints
    ├── testing/        # Quality & verification
    └── review/         # Review gates & rejection criteria
```

See `rules/README.md` for rule responsibilities.
