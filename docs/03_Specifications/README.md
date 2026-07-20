# 03_Specifications

## Purpose

Specify **exact behavior** that engineering will implement and QA will verify.

Specifications are the contract between Product and Code:

Vision → Product → **Specification** → Architecture → Code → Test

## Contains

- Functional specifications
- Non-functional requirements (performance, security, reliability)
- AI behavior specs (prompts/policies at product-behavior level)
- Edge cases and acceptance criteria

## Rules

- Specs must be testable.
- Specs must reference a Product doc.
- Ambiguity is a defect in the spec, not something to “figure out in code”.
- Changing behavior requires updating the spec first (SDD).

## Templates

Use `docs/templates/Specification_Template.md`.
