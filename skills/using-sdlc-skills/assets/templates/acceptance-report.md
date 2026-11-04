# Acceptance Report: [FEATURE_NAME]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Acceptance and Verification Report  
> **Primary Owner Skill:** `verification-before-completion`  
> **Canonical Destination Path:** `docs/features/<feature-id>/acceptance-report.md`  
> **Status:** `<Draft | Verified | Partial | Failed | Blocked>`  
> **Last updated:** `<YYYY-MM-DD>`  

---

## 1. Executive Verdict & Deliverables (Required)
- **Feature ID:** `FEAT-NNN`
- **Spec / Design Versions:** [Paths / Git commit hashes]
- **Verifier:** [Role / Agent / Name]
- **Verification Date:** [YYYY-MM-DD]
- **Overall Verdict:** `Verified` | `Partial` | `Failed` | `Blocked`

### Produced Deliverables
| Deliverable | Canonical Path | Git Commit / Checksum | Status |
|---|---|---|---|
| Application Code | `path/to/code` | `abc1234` | Complete |
| Test Suites | `path/to/tests` | `abc1234` | Passing |

---

## 2. Requirement & Acceptance Criteria Checks (Required)
| Requirement / AC ID | Scenario Summary | Verification Command / Observation | Actual Result | Verdict | Evidence Reference |
|---|---|---|---|---|---|
| `US-FEAT-NNN-001` | Story verification | `npm test -- test/feature.spec.ts` | 5 passed, 0 failed | Passed | See §3 log below |
| `AC-FEAT-NNN-001` | Happy path scenario | Browser automation / API call | HTTP 200, valid body | Passed | Screenshot / raw log |

---

## 3. Empirical Test & Build Evidence (Required)
| Check | Exact Command & Environment | Exit Code / Result | Notes & Observations |
|---|---|---|---|
| Unit / Component Tests | `npm test` / `pytest` | Exit 0 | All unit assertions green |
| Integration Tests | `npm run test:integration` | Exit 0 | Database transactions verified |
| Lint & Static Analysis | `npm run lint` / `flake8` | Exit 0 | 0 warnings, 0 errors |

### Raw Terminal Output Evidence
```text
[Paste relevant raw terminal execution snippet proving clean execution here]
```

---

## 4. Findings, Gaps & Residual Limitations (Required)
- **Unverified Items:** [List any requirement not covered or skipped with reason]
- **Environment Limitations:** [e.g., Staging sandbox mocked external payment gateway]
- **Residual Risks & Tech Debt:** [Known minor caveats or follow-up items]

---

## 5. Traceability & RTM Updates (Optional)
- **RTM Rows / Columns Updated:** [Link to `docs/specs/RTM.md` if applicable]
- **Requirements Lacking Automated Tests:** [Mark any requirement needing manual drill]

---

## 6. Independent Sign-off Gate (Required)
- [ ] Acceptance scenarios verified independently of implementation self-report
- [ ] All verification commands were executed freshly and outputs inspected
- [ ] Failures, skipped checks, and mocks are explicitly disclosed
- [ ] No test threshold, linter rule, or quality gate was weakened to achieve verdict
- **Approver / Verifier Signature:** [Role / Name / Date]
