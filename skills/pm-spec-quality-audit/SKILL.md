---
name: pm-spec-quality-audit
description: Audit a PRD, feature specification, User Story, or requirements document for build-damaging gaps. Use when reviewing specs before coding to identify untestable requirements, missing flows, scope ambiguity, hidden assumptions, and traceability gaps.
license: MIT
---

# Specification Quality Audit (pack adaptation)

Adapted for the Universal SDLC Agent Skills Pack from Uxcel Product Skills, `pm/audits/spec-quality/SKILL.md` (MIT). Findings and severity categories are retained conceptually; the audit is not a verbatim copy.

## Audit method

1. Identify document type (PRD, functional spec, technical spec, Story/AC), intended audience and lifecycle stage. Evaluate it against its actual purpose.
2. Check the problem/outcome anchor: can every major requirement be linked to a user or business need? Flag solution-first specifications where the problem is unknown.
3. Check layer separation: distinguish product/business outcome, observable functional behavior and technical implementation. Flag architecture details embedded in a product requirement unless they are real constraints.
4. Test every requirement: could an engineer/QA write a pass/fail test without asking what a vague adjective means? Look for measurable thresholds when the outcome demands them.
5. Look for absences, not only bad wording: out-of-scope boundaries, error and alternate flows, empty states, permissions, dependencies, constraints, assumptions and acceptance criteria.
6. Check traceability and consistency: duplicate/conflicting requirements, stories with no user value, ACs that don't test the stated behavior, orphaned constraints, unsupported claims and missing owners.
7. Classify findings by likely build damage: **Critical** (teams may build different/wrong things), **Major** (delivery likely to drift or break), **Minor** (trust/maintenance degradation), **Cosmetic** (wording only).
8. For each finding, state the violated principle, evidence/location, impact and a concrete repair. Do not rewrite stakeholder intent by guessing. Separate blockers from suggested improvements.

## Output format

```markdown
## Specification Quality Audit — <document>
Context: <document type, audience, lifecycle stage>

### Critical
- [Location] Finding → impact → concrete repair
### Major
- ...
### Minor
- ...
### Cosmetic
- ...
### Working well
- ...

Top priorities: <ordered actions>
Open questions / assumptions requiring owner decision: <list>
```

If a category has no findings, say so. Do not manufacture findings to fill the table.

## Gate guidance

Do not use an arbitrary numeric score as the release criterion. Do not proceed with unresolved Critical findings. Major findings must be fixed or explicitly accepted by the appropriate owner with rationale. Minor/Cosmetic findings may be deferred when the risk and schedule justify it. This audit checks document quality; it does not prove the implementation works, replace code review, or replace runtime acceptance testing.
