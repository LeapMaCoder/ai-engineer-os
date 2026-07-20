# 08_Testing

## Purpose

Define how we prove Code matches Specifications.

In the Source of Truth chain, Test is the last verification layer:

Vision → Product → Specification → Architecture → Code → **Test**

## Contains

- Test strategy
- Quality gates
- Coverage expectations (once stack exists)
- Bug triage conventions

## Rules

- Acceptance criteria come from Specifications, not from tickets alone.
- Flaky tests are treated as defects.
- Do not choose test frameworks here without Architecture / ADR.

## Related

Cross-cutting suites live in `/tests`. Unit tests live next to code.
