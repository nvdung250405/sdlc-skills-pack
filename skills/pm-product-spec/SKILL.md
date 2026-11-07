---
name: pm-product-spec
description: Use when drafting PRDs, scoping business requirements, or defining measurable product outcomes.
license: MIT
---

# Product Specification / PRD (pack adaptation)

Adapted for the Universal SDLC Agent Skills Pack from Uxcel Product Skills, `pm/deliverables/product-spec/SKILL.md` (MIT). This is a curated adaptation; consult `manifests/skill-provenance.json` before refreshing it from upstream.

## Responsibility

Own product intent and the product-level PRD. Do not duplicate the feature's canonical Story/AC artifact. A PRD may summarize representative stories, but detailed Stories and their Acceptance Criteria live in `docs/features/<feature-id>/spec.md` and are owned by `pm-user-story`.

## Inputs

- Raw idea or feature request.
- Available user/customer evidence, business goals and constraints.
- Existing product vision, scope, metrics, architecture constraints and repository conventions when available.

## Procedure

1. **Choose the artifact.** Use a PRD when the problem, desired outcome or product scope is still being decided. Use a feature specification when scope is agreed and detailed observable behavior is needed. Do not blend product intent with implementation design.
2. **Anchor on the problem.** State the current/desired state gap, who is affected, consequences, and target outcome. Link evidence where supplied. If evidence is missing, mark the claim as an assumption and state how it could be validated; never invent research, metrics or customer quotes.
3. **Define the target user and value.** Use supplied personas/research. If not available, label the persona as provisional instead of fabricating a research-grounded persona.
4. **Set measurable goals.** Separate outcomes from outputs. Include baseline, target, measurement method and time horizon where known. Leave unknown targets as open questions rather than inventing numbers.
5. **Set boundaries.** Explicitly state in-scope and out-of-scope behavior. Capture constraints, dependencies, assumptions, risks and owners where known.
6. **Record candidate capabilities.** Organize outcomes into epics/features and propose priority with rationale. Detailed Story decomposition belongs to `pm-user-story`.
7. **Self-review.** Check every requirement for observable/testable wording, traceability to the problem, coherent scope and explicit uncertainty.

## Output contract

Default path: `docs/prd.md`, unless the repository already has a canonical location.

Include, as appropriate:

- Summary and problem/evidence.
- Target users and needs.
- Goals, success metrics and non-goals.
- Scope and candidate epics/features.
- Constraints, dependencies, assumptions and risks.
- Open questions and validation plan.

## Quality gate

The PRD is ready when the problem and target users are clear enough for the next decision; goals and boundaries are explicit; success can be evaluated; material assumptions are labeled; and downstream feature detail is not confused with product-level intent. For significant work, request `pm-spec-quality-audit` before the PRD is treated as build-ready.

## Environment Integration

> [!TIP]
> On completion: finish with `verification-before-completion` to confirm any generated artifacts meet acceptance criteria, then `task-handoff` to persist state across sessions.
