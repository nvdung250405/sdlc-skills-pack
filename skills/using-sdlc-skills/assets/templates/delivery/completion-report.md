# Completion Report: [TASK_OR_FEATURE_NAME]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Minimum Completion Report  
> **Primary Owner Skill:** `verification-before-completion`, `task-handoff`  
> **Canonical Destination Path:** `docs/features/<feature-id>/completion-report.md` (hoặc trực tiếp trong báo cáo kết thúc turn)  
> **Status:** `<Completed | Partially Completed | Blocked | Failed>`  
> **Last updated:** `<YYYY-MM-DD>`  

---

## 1. Status (Required)
- **Final Verdict:** `Completed` | `Partially Completed` | `Blocked` | `Failed`
- **Feature / Task ID:** `FEAT-NNN`
- **Completed By:** [Role / Agent / Engineer]
- **Completion Timestamp:** [YYYY-MM-DD HH:MM:SS UTC]

---

## 2. Deliverables (Required)
All modified, created, or deprecated files with exact relative paths and commit hashes:

| Deliverable Type | Exact File Path | Git Commit SHA / Checksum | State |
|---|---|---|---|
| Application Code | `src/...` | `abc1234` | Modified |
| Automated Tests | `tests/...` | `abc1234` | Added |
| Executable Contract | `contracts/openapi.yaml` | `abc1234` | Validated |
| Feature Specification | `docs/features/<id>/spec.md` | `abc1234` | Approved |

---

## 3. Verification Evidence (Required)
Commands actually executed, exit codes observed, and empirical proof (Evidence-Before-Assertion):

| Verification Check | Exact Command Run | Exit Code | Result Summary |
|---|---|---|---|
| Unit & Component Tests | `python scripts/bounded_run.py npm test` | `0` | 24 passed, 0 failed |
| Contract Schema Lint | `python scripts/verify_contracts.py` | `0` | 100% schema conformance |
| Code Quality / Linter | `npm run lint` | `0` | 0 warnings, 0 errors |

### Raw Log Reference
- Full terminal log persisted at: `.agent/logs/YYYYMMDD_HHMMSS_test.log`

---

## 4. Limitations & Residual Risks (Required)
- **Unverified Assumptions:** [None | List any boundary condition not tested]
- **Environment Caveats:** [e.g., Run on mock payment gateway in staging]
- **Technical Debt & Follow-up Items:** [List any deferred cleanups or future optimizations]

