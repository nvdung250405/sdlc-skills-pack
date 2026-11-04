# Tasks: [FEATURE_NAME]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Authoritative Task Breakdown  
> **Primary Owner Skill:** `planning-and-task-breakdown`  
> **Canonical Destination Path:** `docs/features/<feature-id>/tasks.md`  
> **Status:** `<Draft | In Progress | Completed>`  
> **Last updated:** `<YYYY-MM-DD>`  

- **Feature ID:** `FEAT-NNN`
- **Inputs:** `docs/features/<feature-id>/spec.md`, `plan.md`, `design.md`

---

## 1. Task List (Required)

Format: `T-NNN [P?] [FR/Story] Task summary` where `P` marks safe independent parallelism. Every task MUST specify target files, dependencies, acceptance condition, and exact verification command.

- [ ] `T-001` [US-FEAT-NNN-001] [Task verb + concrete outcome]
  - **Depends on:** None
  - **Target Files:** `src/feature/domain.ts`, `tests/feature/domain.spec.ts`
  - **Acceptance:** [Observable behavior]
  - **Verify Command:** `npm test -- tests/feature/domain.spec.ts` (Exit 0)
  - **Risk / Rollback:** [Low / Revert commit]

- [ ] `T-002` [US-FEAT-NNN-001] [Next task verb + outcome]
  - **Depends on:** `T-001`
  - **Target Files:** `src/feature/api.ts`, `tests/feature/api.spec.ts`
  - **Acceptance:** [Observable behavior]
  - **Verify Command:** `npm test -- tests/feature/api.spec.ts` (Exit 0)
  - **Risk / Rollback:** [Low]

---

## 2. Execution Contract (Required)
- Execute tasks in strict dependency order; do not start dependent tasks before prerequisites are verified.
- Keep one coherent vertical slice at a time. Write/update tests with behavioral code.
- Do not silently alter the spec, API contract, database schema or quality gate; propose an explicit amendment.
- Mark complete `[x]` ONLY after executing the verification command and recording real evidence.

---

## 3. Final Verification & Completion Gate (Required)
- [ ] All tasks are complete or explicitly deferred with documented reason
- [ ] Automated test suites, linters, and type-checks pass cleanly
- [ ] Acceptance criteria and requirement IDs are fully covered
- [ ] Verification evidence recorded in `acceptance-report.md`
- **Task Lead Sign-off:** [Role / Date]
