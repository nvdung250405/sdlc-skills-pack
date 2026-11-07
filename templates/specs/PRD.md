# Product Requirements Document (PRD): [PRODUCT_OR_INITIATIVE_NAME]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Product Requirements Document (PRD)  
> **Primary Owner Skill:** `spec-driven-development`  
> **Canonical Destination Path:** `docs/prd.md`  
> **Status:** `<Draft | In Review | Approved | Superseded>`  
> **Last updated:** `<YYYY-MM-DD>`  

---


> Purpose: describe the problem, intended outcomes, scope, and product-level requirements. Tailor this document to the initiative's size and risk. Keep unsupported details explicit as assumptions or open questions; do not invent user research, market data, baselines, or targets.

## Document control

- PRD ID: `PRD-NNN` (optional for small initiatives)
- Status: Draft | In Review | Approved | Superseded
- Product / initiative: [name]
- Owner: [Product Manager / Business Analyst / responsible role]
- Contributors / reviewers: [roles or names]
- Last updated: [YYYY-MM-DD]
- Related documents: [vision, project context, architecture, existing requirements, links]

## 1. Executive summary

[In a few sentences, describe who has a problem, what outcome is needed, and why this initiative matters now. Avoid prescribing implementation detail unless it is a genuine constraint.]

## 2. Problem statement and evidence

### Problem

[Describe the user/business problem, affected workflow, and consequences of leaving it unresolved.]

### Evidence

| Evidence ID | Observation or source | Date / context | Confidence | Implication |
|---|---|---|---|---|
| EVD-001 | [Interview, analytics, support ticket, operational data, stakeholder input, etc.] | [context] | High / Medium / Low | [what this evidence supports] |

Distinguish observed facts from interpretation. If evidence is unavailable, state that explicitly and identify how it should be gathered.

## 3. Target users and context

Include only the level of segmentation useful for this initiative.

| User / stakeholder segment | Need or job to be done | Current pain point | Desired outcome |
|---|---|---|---|
| [segment] | [need] | [pain] | [outcome] |

Optional supporting artifacts: personas, user journeys, service blueprints, workflow diagrams, accessibility needs, and research notes.

## 4. Goals and success measures

### Goals

- [G-001] [Outcome we want to achieve]

### Success metrics

| Metric ID | Metric and definition | Baseline | Target / threshold | Measurement source and window | Owner |
|---|---|---|---|---|---|
| MET-001 | [Define calculation and population] | [value, unknown, or not applicable] | [target or TBD with rationale] | [instrumentation, survey, operational report; time window] | [role] |

Do not fabricate a baseline or target. When a target is unknown, record who will establish it, by when, and what decision depends on it.

## 5. Non-goals

Explicitly list outcomes or capabilities that this initiative will not address.

- [NG-001] [Out of scope and, where useful, why]

## 6. Scope and candidate capabilities

### In scope

- [CAP-001] [Capability or outcome]

### Out of scope

- [OOS-001] [Excluded capability]

### Epic breakdown

Create epics when they help organize independently valuable capabilities. Small changes may omit epics and proceed directly to a feature or story.

| Epic ID | Epic / capability | User or business outcome | Priority | Dependencies / notes |
|---|---|---|---|---|
| `EPIC-001` | [title] | [outcome] | Must / Should / Could / Later | [dependencies or TBD] |

Epic IDs should remain stable once referenced by downstream stories, tasks, tests, or release evidence.

## 7. High-level requirements and experience

Summarize only the product behavior needed to align stakeholders. Detailed feature behavior belongs in feature specifications and User Stories/Acceptance Criteria; system-level requirements may be managed separately in an SRS or requirements register.

- Primary user journeys / workflows: [brief outline or link]
- Key capabilities and business rules: [brief outline or link]
- External systems, data, and integrations: [known systems or link]
- Accessibility, localization, privacy, security, legal, and regulatory considerations: [applicable concerns or TBD]
- Known system-level quality attributes (performance, availability, recovery, auditability, etc.): [measurable constraint or reference, if known]

## 8. Constraints, assumptions, dependencies, and risks

### Constraints

| ID | Constraint | Source / rationale | Impact |
|---|---|---|---|
| CON-001 | [technical, legal, budget, schedule, platform, policy, or organizational constraint] | [source] | [impact] |

### Assumptions

| ID | Assumption | Confidence | Validation method / owner | Due date or decision point |
|---|---|---|---|---|
| ASM-001 | [unverified statement] | High / Medium / Low | [how and by whom it will be checked] | [date / milestone / TBD] |

### Dependencies and risks

| ID | Type | Description | Likelihood / impact | Mitigation or next action | Owner |
|---|---|---|---|---|---|
| RSK-001 | Risk / Dependency | [description] | [assessment] | [action] | [role] |

## 9. Rollout and operational considerations

Include when relevant to launch or ongoing operation.

- Rollout / migration / feature-flag approach: [plan or TBD]
- Adoption, training, support, and communications: [plan or not applicable]
- Instrumentation, monitoring, and feedback signals: [signals and owners]
- Rollback, roll-forward, or service-continuity constraints: [plan or link]

## 10. Open questions and decisions

| ID | Question / decision | Why it matters | Owner | Needed by | Status |
|---|---|---|---|---|---|
| OQ-001 | [question not yet resolved] | [impact if unresolved] | [role] | [date / milestone] | Open |

Do not represent an unresolved question as an approved requirement. Record the answer and its rationale when resolved.

## 11. Readiness / approval gate

Tailor these checks to the scale and risk of the initiative; mark N/A with a reason rather than forcing irrelevant artifacts.

- [ ] Problem and target users are clear, with evidence or explicitly recorded uncertainty.
- [ ] Goals and success measures are measurable, or the plan to establish missing baselines/targets is recorded.
- [ ] In-scope and out-of-scope boundaries are explicit.
- [ ] Candidate epics/capabilities are identified where useful and have stable IDs.
- [ ] Important assumptions, dependencies, risks, and open questions have owners or next actions.
- [ ] Relevant privacy, security, accessibility, legal, and operational concerns are considered.
- [ ] Downstream specification and validation approach is clear enough to proceed.

Decision: Proceed | Proceed with recorded follow-ups | Rework | Rejected

- Reviewer / role: [role]
- Date: [YYYY-MM-DD]
- Rationale / conditions: [notes]