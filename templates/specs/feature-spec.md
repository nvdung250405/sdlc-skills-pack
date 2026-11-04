# Feature Specification: [FEATURE_NAME]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Feature Specification (Stories & Acceptance Criteria)  
> **Primary Owner Skill:** `spec-driven-development`, `pm-user-story`  
> **Canonical Destination Path:** `docs/features/<feature-id>/spec.md`  
> **Status:** `<Draft | In Review | Approved | Superseded>`  
> **Last updated:** `<YYYY-MM-DD>`  

- **Feature ID:** `FEAT-NNN`
- **Owner:** [Role / Team / Agent]
- **Related Epic(s):** [EPIC-...]
- **Related System Requirements:** [FR-..., NFR-...] (when applicable)

> This is the canonical feature artifact. Keep detailed User Stories and Acceptance Criteria here unless the project explicitly chooses another single authoritative location. Do not maintain duplicate Story/AC records across multiple files.

---

## 1. Problem and Objective (Required)
[Describe the problem, affected users, business justification, and expected value. Mark unvalidated assumptions explicitly.]

---

## 2. Scope (Required)
### In Scope
- [Capability 1]
- [Capability 2]

### Out of Scope
- [Explicitly excluded capabilities or deferred use cases]

---

## 3. Actors and Business Rules (Required)
- **Actors / Personas:** [Relevant user roles and systems]
- **Business Rules:** [Rules with explicit owners/sources, or `None identified`]
- **Constraints & Dependencies:** [System or environment constraints]

---

## 4. User Stories and Acceptance Criteria (Required)

### US-FEAT-NNN-001 — [Story Title]
- **Priority:** P1 | P2 | P3
- **Story:** As a [user/persona], I want [capability], so that [value/outcome].
- **Independent Test:** [How this story can be verified independently]
- **Dependencies:** [Other stories, APIs, or None]

#### Acceptance Criteria

**AC-FEAT-NNN-001 — [Happy Path Scenario Title]**
- **Given:** [Initial context/preconditions]
- **When:** [User action or system event]
- **Then:** [Observable and testable result]

**AC-FEAT-NNN-002 — [Error / Edge Scenario Title]**
- **Given:** [Relevant invalid, boundary or failure condition]
- **When:** [Action or event]
- **Then:** [Expected observable error handling or fallback behavior]

#### Story Notes
- **Edge Cases:** [Boundary values, empty states, duplicate inputs, concurrency]
- **Open Questions:** [Unresolved decisions; do not silently invent answers]

> Repeat the Story block for each independently valuable slice. Given/When/Then is the default for behavioral scenarios; do not force system constraints or non-functional requirements into artificial User Stories.

---

## 5. Functional Requirements (Optional / When Needed)
| ID | Requirement (Testable, single obligation) | Priority | Source | Acceptance / Verification |
|---|---|---|---|---|
| FR-FEAT-NNN-001 | The system MUST ... | Must | [Source] | [Observable result / Test] |

---

## 6. Non-Functional Requirements & Constraints (Optional / When Needed)
| ID | Quality Attribute | Measurable Requirement | Verification Method |
|---|---|---|---|
| NFR-FEAT-NNN-001 | Performance / Security / Availability | [Threshold or behavior] | [Command / Benchmark] |

---

## 7. Data and External Contracts (Required)
- **Entities & Data Ownership:** [Data models touched or created]
- **API / Events / Integrations:** [Contract endpoints or event schemas]
- **Authorization & Privacy:** [Access control rules and PII protections]
- **Compatibility & Migration:** [Backward compatibility impact]

---

## 8. Outcome / Success Criteria (Optional / When Applicable)
| ID | Outcome | Baseline | Target | How Measured |
|---|---|---|---|---|
| SC-001 | [User/business/system outcome] | [Baseline/unknown] | [Target] | [Telemetry metric] |

---

## 9. Assumptions and Open Questions (Required)
- **Assumptions:** [Mark validation status and owner]
- **Blocking Questions:** [Question, owner, needed-by date]

---

## 10. Verification and Approval Gate (Required)
- [ ] Problem, value, and scope are clear enough for this feature's risk level
- [ ] Stories represent user value and are split into independently verifiable slices
- [ ] Acceptance Criteria are observable, testable, and cover error/edge paths
- [ ] Requirement and contract references are traceable
- [ ] Security, privacy, compatibility, and migration impacts are addressed
- [ ] Open questions are resolved or explicitly accepted by the right owner
- **Reviewer Approval:** [Role / Decision / Date]
