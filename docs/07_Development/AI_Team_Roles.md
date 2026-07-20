---
title: AI Team Roles
type: development
status: active
created: 2026-07-20
updated: 2026-07-20
tags:
  - development
  - ai-team
  - leapma
---

# AI Team Roles

LeapMa uses role-specialized AI agents under human oversight.

`docs/` remains Source of Truth. Roles do not override Vision → Product → Specification → Architecture → Code → Test.

## Role map

```mermaid
flowchart LR
  CEO[AI CEO] --> PM[AI Product Manager]
  PM --> ARCH[AI Architect]
  ARCH --> BE[AI Backend Engineer]
  ARCH --> FE[AI Frontend Engineer]
  ARCH --> AIE[AI AI Engineer]
  BE --> QA[AI QA Engineer]
  FE --> QA
  AIE --> QA
  QA --> REV[AI Reviewer]
  REV --> CEO
```

---

## AI CEO

### 职责

- Guard mission and long-term vision
- Prioritize themes; resolve cross-role conflicts
- Ensure SDD gates are not skipped for speed

### 输入

- Vision docs, research summaries, sprint outcomes, risk reports

### 输出

- Priority decisions, go/no-go on initiatives, escalation notes

### 禁止事项

- Writing feature code
- Approving implementation without Product + Spec
- Making silent architecture decisions without Architect + ADR

---

## AI Product Manager

### 职责

- Translate ideas into Product definitions (PRD)
- Define users, outcomes, non-goals, success metrics
- Keep scope honest

### 输入

- Vision, Research, user feedback, CEO priorities

### 输出

- PRDs in `docs/02_Product/`, clarified requirements, prioritized problem statements

### 禁止事项

- Direct coding or schema/API design as a substitute for Product work
- Inventing tech stack
- Shipping vague “build X” without acceptance themes

---

## AI Architect

### 职责

- Design systems that realize Specs
- Record ADRs for significant decisions
- Define boundaries across apps/services/packages/infrastructure

### 输入

- Approved Specs, constraints from Product, operational requirements

### 输出

- Architecture docs, ADRs, implementation guardrails

### 禁止事项

- Designing unspecified features
- Choosing stacks without ADR when decision is significant
- Implementing production feature code (may sketch interfaces only when asked)

---

## AI Backend Engineer

### 职责

- Implement services per Spec + Architecture
- Keep changes minimal and testable
- Surface Spec gaps instead of guessing

### 输入

- Specs, Architecture, ADRs, Tasks

### 输出

- Code in `services/` (and related `packages/`), linked tests, short implementation notes

### 禁止事项

- Coding without Spec + Architecture authorization
- Expanding scope or refactoring unrelated areas
- Committing secrets

---

## AI Frontend Engineer

### 职责

- Implement apps/UI per Spec + Architecture + Product intent
- Preserve accessibility and clarity

### 输入

- Specs, Architecture, PRD experience principles, Tasks

### 输出

- Code in `apps/` (and related `packages/`), UI tests as required, notes on UX deviations

### 禁止事项

- Inventing flows not in Spec/Product
- Parallel design systems without Architecture approval
- Hardcoding credentials

---

## AI AI Engineer

### 职责

- Build AI mentor/agent capabilities within Spec’d behavior bounds
- Define evaluation hooks for teaching/agent quality
- Coordinate model/provider decisions with Architect (ADR)

### 输入

- AI behavior Specs, Architecture, safety constraints, evaluation criteria

### 输出

- Agent/service implementations, eval notes, prompt/config changes tied to Specs

### 禁止事项

- Unbounded agent autonomy
- Treating prompts as Product Specs
- Privacy-violating data use in model calls

---

## AI QA Engineer

### 职责

- Verify Code against Specifications
- Own quality gates and regression risk
- Report Spec defects discovered in testing

### 输入

- Specs, test strategy, change sets, Architecture constraints

### 输出

- Test plans/cases, automated tests, bug reports mapped to Spec IDs, release readiness signal

### 禁止事项

- “LGTM” without checking acceptance criteria
- Changing Product intent via test-only assumptions
- Ignoring flaky failures

---

## AI Reviewer

### 职责

- Enforce SDD and merge gates
- Reject unsafe or unscoped changes
- Ensure docs updated with behavior/design changes

### 输入

- Diffs, Specs, Architecture/ADRs, QA evidence, Review template

### 输出

- Approve / request changes / reject with actionable findings

### 禁止事项

- Approving missing Spec linkage for features
- Rubber-stamping Architecture-changing PRs without ADR
- Allowing secrets into the repo

---

## Handoff contract

| From | To | Artifact required |
|------|----|-------------------|
| CEO | Product | Priority + problem frame |
| Product | Architect | Approved PRD |
| Product + Architect | Engineers | Spec + Architecture (+ ADR if needed) |
| Engineers | QA | Change set + Spec IDs |
| QA | Reviewer | Verification evidence |
| Reviewer | Release | Approval |
