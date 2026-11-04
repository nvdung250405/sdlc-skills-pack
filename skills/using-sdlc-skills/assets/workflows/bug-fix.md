# Bug-fix workflow

> **Document type:** Standardized Workflow Definition  
> **Workflow:** `bug-fix`  
> **Scenario Group:** Defect Resolution  
> **Trigger / Input:** Defect ticket, failing test, bug report, unexpected runtime behavior  
> **Primary Stages:** Reproduce (Red) → Isolate Root Cause → Fix (Green) → Refactor → Verify  
> **Key Output:** Bug fix commit, automated regression test guard  
> **Verification / Exit Gate:** Regression test passing, zero side regressions, `verification-before-completion`  

---

## 1. Context & Intake
1. Capture the observed symptom, expected behavior, execution environment, and reproduction steps.
2. Verify if the expected behavior is documented in an existing specification (`docs/features/<feature-id>/spec.md`). Never invent business logic without grounding.

## 2. Systematic Root Cause Isolation
3. Use `systematic-debugging` before editing implementation code:
   - Reproduce the failure consistently.
   - Isolate the defect to a specific subsystem or function.
   - Formulate a falsifiable hypothesis and test it with telemetry or logs.
   - Identify the exact root cause.

## 3. TDD Fix & Regression Guard
4. Author an automated regression test reproducing the defect (Red state) before touching production code.
5. Apply the smallest surgical fix using `test-driven-development` to turn the test green.
6. Clean up code with `code-simplification` while preserving functional behavior.

## 4. Review & Verification Gate
7. Run the project's full test suite, linting, and type checking to ensure zero regressions.
8. Use `security-and-hardening` when trust boundaries, permissions, credentials, or sensitive data are touched.
9. Execute `verification-before-completion` to capture fresh terminal output and evidence before reporting the fix as complete.
