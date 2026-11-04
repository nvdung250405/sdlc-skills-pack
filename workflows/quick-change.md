# Quick-change workflow

> **Document type:** Standardized Workflow Definition  
> **Workflow:** `quick-change`  
> **Scenario Group:** Construction  
> **Trigger / Input:** Minor tweak, copy update, isolated bug, clear low-risk change  
> **Primary Stages:** Context & Intake → Acceptance Condition → Atomic TDD Edit → Targeted Verification → Safety Review  
> **Key Output:** Atomic commit, targeted test case  
> **Verification / Exit Gate:** Targeted tests passing, `verification-before-completion` evidence captured  

---

## 1. Prerequisites & Scoping
Use only when scope is unambiguous, risk is low, and the change does not affect public contracts, data migrations, security boundaries, or production state. If complexity expands, escalate immediately to `workflows/feature-loop.md`.

## 2. Execution Steps
1. **Context & Scoping:** Read the relevant code, repository guidance, and existing tests. Use `spec-driven-development` only if an existing feature spec needs clarification or behavior is ambiguous.
2. **Define Acceptance Condition:** State a concise, verifiable acceptance condition before editing.
3. **Atomic Implementation:** Make the smallest surgical change using `incremental-implementation`. Add or update regression/unit tests using `test-driven-development` when behavior changes.
4. **Targeted Verification:** Run focused tests, linters, and project quality checks.
5. **Verification Gate:** Run `verification-before-completion` to capture fresh terminal output confirming all checks passed and zero unexpected regressions exist.
6. **Diff & Safety Review:** Review `git diff` using `code-review-and-quality` for unintended side-effects, formatting noise, or security risks.
7. **Honest Reporting:** Report exact command execution evidence and remaining uncertainty in the completion response.
