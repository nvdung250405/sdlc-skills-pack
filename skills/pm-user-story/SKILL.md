---
name: pm-user-story
description: Write, split, or critique value-focused User Stories and Acceptance Criteria for a feature. Use when an epic or product requirement must become testable feature-level behavior; avoid manufacturing stories for pure technical work that is clearer as a technical spec or ADR.
license: MIT
---

# User Story Authoring (pack adaptation)

Adapted for the Universal SDLC Agent Skills Pack from Uxcel Product Skills, `pm/foundations/user-story/SKILL.md` (MIT). The Given/When/Then output contract is aligned with GitHub Spec Kit's public specification pattern. This is not a verbatim copy; consult provenance before refresh.

## Responsibility

Own the detailed Story/Acceptance Criteria content for a user-facing feature. The canonical location is `docs/features/<feature-id>/spec.md`, or the repository's existing feature-spec file. Do not create a second user-story file when the canonical spec already contains Story/AC.

## Inputs

- Approved or draft PRD, epic or feature intent.
- Relevant persona/journey or evidence (if present).
- Existing business rules, system constraints, contracts and repository conventions.

## Procedure

1. Establish whose need the story represents, what outcome they want and why it matters. If the persona/need is inferred rather than evidenced, label it as an assumption.
2. Decide whether a User Story improves clarity. For infrastructure, refactoring, pure maintenance or system-level NFR, a technical change record, requirement or ADR may be more appropriate than a fictional user story.
3. Write a concise value statement: `As a <persona>, I want <capability>, so that <outcome>.` Keep implementation tasks out of the story sentence.
4. Apply INVEST as a heuristic. Split stories that bundle distinct outcomes, multiple personas or multiple independently testable workflows. Do not split so aggressively that a slice loses user value.
5. Write Acceptance Criteria for observable behavior. Prefer Given/When/Then scenarios when behavior can be expressed that way. Cover the important happy path, validation/error paths, permissions, boundary cases and alternate flows that matter to the feature. Do not invent business rules to fill gaps.
6. Capture business rules, dependencies, relevant NFRs, edge cases and open questions separately from the narrative story.
7. Map each scenario to an independent test idea or verification mechanism. A test idea is not evidence that the test has passed.
8. Review the story for duplicated scope, unclear actors, untestable phrases and conflicts with the PRD/spec.

## Output contract

Update the canonical feature spec; do not create a second source of truth. Each story should contain:

- Stable `US-###` identifier and title.
- Epic/feature reference when available.
- Story statement (or a clear free-form alternative when the strict formula is unsuitable).
- Priority and rationale where known.
- Acceptance Criteria with stable `AC-###` identifiers and Given/When/Then scenarios where appropriate.
- Business rules, edge cases, dependencies, constraints and open questions as applicable.
- Independent test/verification notes.

## Quality gate

Ready for planning when the need and value are understandable; story scope is reasonably independent; ACs are observable and testable; material error/alternate paths are addressed; assumptions are visible; and there are no unresolved contradictions. Use `pm-spec-quality-audit` for non-trivial or high-risk specs.
