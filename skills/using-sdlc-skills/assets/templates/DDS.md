# Detailed Design Specification (DDS / LLD): [FEATURE_NAME]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Detailed Design Specification (DDS / LLD)  
> **Primary Owner Skill:** `software-architecture`, `codebase-design`  
> **Canonical Destination Path:** `docs/features/<feature-id>/design.md`  
> **Status:** `<Draft | In Review | Approved>`  
> **Last updated:** `<YYYY-MM-DD>`  

---

## 1. Purpose, Scope & Boundaries (Required)
- **Feature ID:** `FEAT-NNN`
- **Related Requirements / Stories:** [FR-..., US-..., spec.md link]
- **Architecture Context:** [ADR links, component seam]
- **Included / Excluded Scope:** [Boundaries of this design]

---

## 2. Design Overview & Component Seams (Required)
[Component responsibilities and boundaries. Include Mermaid sequence or component diagrams illustrating request lifecycle.]

---

## 3. Interfaces & Public Contracts (Required)
For every public or cross-module interface, document endpoints, events, validation, authorizations, idempotency, and error handling.

| Contract | Method / Topic | Input Schema | Output Schema | Error Handling | AuthZ | Traceable Req ID |
|---|---|---|---|---|---|---|
| `CreateItem` | `POST /api/items` | `CreateItemRequest` | `ItemResponse` | 400 Validation, 409 Conflict | RBAC: `items:write` | `FR-001` |

---

## 4. Data Model & Persistence (Required)
- **Entities / Tables / Collections:** [Schema definitions, keys, and relations]
- **Indexes & Invariants:** [Unique constraints, compound indexes, TTL]
- **Transaction & Consistency Boundaries:** [ACID boundaries, locking]
- **Migration & Rollback:** [Zero-downtime expand/contract schema strategy]

---

## 5. Detailed Behavioral Flows (Required)
### 5.1 Main Happy Path
[Step-by-step execution flow]

### 5.2 Error & Boundary Flows
[Failure points, timeouts, retries, and fallback behaviors]

### 5.3 Concurrency & State Machine
[Race condition mitigation, idempotent keys, optimistic concurrency control]

---

## 6. Security & Privacy Controls (Required)
- **Trust Boundaries:** [Assets protected, ingress/egress validation]
- **Threat Mitigations:** [OWASP Top 10 defenses, rate limiting, SQLi/XSS prevention]
- **Sensitive Data & Secrets:** [Encryption at rest/in transit, zero secrets in code]

---

## 7. Reliability, Operations & Performance (Optional)
- **Timeouts, Retries & Circuit Breaking:** [Thresholds]
- **Expected Load & Latency Targets:** [e.g., p95 < 200ms at 500 RPS]
- **Telemetry:** [Metrics, alerts, structured logs, distributed trace IDs]
- **Feature Flags & Rollout Plan:** [Gradual percentage rollout strategy]

---

## 8. Test Design & Acceptance Strategy (Required)
| Requirement / AC | Test Level (Unit / Integration / E2E) | Scenario & Verification Command | Owner |
|---|---|---|---|
| `AC-001` | Integration | Test database transactional isolation | QA / Dev |

---

## 9. Implementation Tasks Reference (Required)
Link to `docs/features/<feature-id>/tasks.md`; do not embed a duplicate task list here.

---

## 10. Decisions & Open Questions (Required)
- **Accepted Decisions:** [ADR links]
- **Resolved Questions:** [Summary of technical alignments]
- **Unresolved / Blocking Questions:** [Question, owner, needed-by date]

---

## 11. Design Review & Approval Gate (Required)
- [ ] Every relevant requirement is addressed or explicitly documented as out of scope
- [ ] Interfaces, schemas, error codes, and failure modes are fully defined
- [ ] Data migrations guarantee backward compatibility (expand/contract)
- [ ] Security, privacy, and non-functional requirements have concrete mitigations
- [ ] Design fits the existing codebase architecture and deep module seams
- **Reviewer Approval:** [Tech Lead / Architect / Date]
