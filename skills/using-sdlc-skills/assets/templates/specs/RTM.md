# Requirements Traceability Matrix (RTM)

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Requirements Traceability Matrix (RTM)  
> **Primary Owner Skill:** `requirements-engineering`  
> **Canonical Destination Path:** `docs/specs/RTM.md`  
> **Status:** `<Draft | Baseline | Verified>`  
> **Last updated:** `<YYYY-MM-DD>`  

This matrix maintains bidirectional traceability from stakeholder needs through requirements, architecture design, implementation tasks, and verification test cases.

---

## 1. Traceability Ledger (Required)

| Requirement ID | Requirement Summary | Category | Architecture / Design Seam | Implementation Task | Verification Test Case | Status |
|---|---|---|---|---|---|---|
| `FR-AUTH-001` | OAuth2 Login flow | Functional | `docs/architecture.md#auth` | `T-001` (`tasks.md`) | `test_oauth_flow.py` | Verified |
| `NFR-SEC-001` | Encrypted JWT tokens | Security | `ADR-003` | `T-002` (`tasks.md`) | `test_jwt_encryption.py` | Verified |

---

## 2. Verification Status & Evidence Rules (Required)
- An item is marked `Verified` only when accompanied by passing automated test execution evidence or an approved acceptance report.
- `Pending`: Implementation or test authoring underway.
- `Blocked`: Prerequisite task or external dependency failing.

---

## 3. Verification & Traceability Sign-off (Required)
- [ ] Every in-scope requirement maps to at least one test case or verification command
- [ ] No orphan design elements or unverified requirements exist
- [ ] Verification evidence links resolve to valid artifacts or CI test logs
- **Audited by:** [QA Lead / Requirements Engineer / Date]
