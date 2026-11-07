---
name: requirements-engineering
description: Use when formalizing functional/non-functional requirements, use cases, and maintaining requirements traceability (RTM).
license: Apache-2.0
---

# Requirements Engineering (pack adaptation)

Adapted for this pack from Agentic SDLC Kit's `skills/requirements-engineering/SKILL.md` (Apache-2.0). It is a compact, portable adaptation of the SRS/traceability workflow, not a verbatim upstream snapshot. See `manifests/skill-provenance.json` before updating.

## When to use

Use for a new system, complex domain, regulated/contract-heavy delivery, multiple integrations, substantial NFRs, or when requirement traceability is required. For a small feature, use `pm-user-story` and `spec-driven-development` without creating a formal SRS unnecessarily.

## Ownership and inputs

Own system-level requirement statements, use cases when useful, stable requirement IDs and the initial RTM rows. Consume stakeholder intent, product scope, constraints, known existing behavior and applicable policy. Existing approved IDs and documents are authoritative until formally amended.

## Procedure

1. Establish scope, stakeholders, external systems, user classes, business rules and key constraints. Ask focused questions; do not expand into exhaustive catalogues unless system risk warrants it.
2. Separate confirmed requirements from assumptions, options and unresolved questions. Flag assumptions with an owner and validation approach.
3. Identify functional requirements and important quality attributes (security, privacy, performance, reliability, accessibility, operability, maintainability, compatibility). Make NFRs measurable where the stakeholders or system context provides a basis. Never invent thresholds and present them as approved.
4. Assign stable IDs: `FR-<AREA>-NNN`, `NFR-<AREA>-NNN`; use `UC-NNN` for use cases where they add value. Do not recycle IDs. Mark removed items retired/deprecated rather than renumbering.
5. Express functional requirements as one testable obligation each. Use EARS or clear “shall/must” wording when formal requirements benefit from it. Capture preconditions, main flow, alternative/error flows and postconditions for complex use cases.
6. Create/update the RTM only when traceability is needed. Record source, requirement, planned verification, and later design/test references. Downstream owners append their references; they must not overwrite the requirement definition.
7. Check duplicates, contradictions, feasibility, verifiability, scope and unresolved decision points. Consult `pm-spec-quality-audit` for a product/functional document or use the repository's requirements checklist.

## Output contract

When formalization is justified, default to:

- `docs/srs.md` — scope, context, functional requirements, NFRs, constraints, assumptions and change history.
- `docs/use-cases.md` — only for workflows whose interaction complexity benefits from use-case descriptions.
- `docs/rtm.md` — only when traceability is warranted; initial requirements/verification rows, with later stages appending owned references.

Use project conventions where present. Do not create an SRS merely because this skill exists.

## Quality gate

Each accepted requirement has a clear source/owner, is unambiguous and verifiable, and does not conflict with another accepted requirement. NFR targets have a justified basis or remain open questions. Stable IDs and traceability state are preserved. This skill defines requirements; it does not design the architecture or declare implementation acceptance.

## Environment Integration

> [!TIP]
> On completion: finish with `verification-before-completion` to confirm any generated artifacts meet acceptance criteria, then `task-handoff` to persist state across sessions.
