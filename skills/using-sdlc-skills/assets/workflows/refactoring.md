# Code refactoring & architectural deepening workflow

> **Document type:** Standardized Workflow Definition  
> **Workflow:** `refactoring`  
> **Scenario Group:** Maintenance & Optimization  
> **Trigger / Input:** Technical debt, code smell, module deepening, shallow abstractions  
> **Primary Stages:** Scope & Invariants → Characterization Tests → Deep Module Seams → Micro-Steps → Regression Verification  
> **Key Output:** Refactored clean code, deep module seams, architectural ADR if seams change  
> **Verification / Exit Gate:** 100% behavioral preservation, full test suite passing, zero regression  

---


Use this workflow for technical debt reduction, module deepening, code simplification, or architectural cleanup where observable behavior must remain 100% unchanged. Do not manufacture User Stories for purely technical refactoring.

---

## 1. Scope & Invariants Definition
1. **Define Behavioral Invariants**: Explicitly state the public interfaces, contracts, return values, and side-effects that must not change.
2. **Consult Architectural Context**: Review existing architecture in `docs/architecture.md` and relevant ADRs. If breaking public interfaces or data schemas is unavoidable, escalate to `workflows/deprecation-and-migration.md` instead.

## 2. Characterization Safety Harness
3. **Audit Existing Test Coverage**: Ensure comprehensive test coverage exists for the target code paths.
4. **Write Characterization / Golden Tests**: If test coverage is insufficient or brittle, write behavioral characterization tests using `test-driven-development` to pin down current behavior *before* modifying any implementation code. Confirm all tests pass green.

## 3. Deep Module Design (Design-It-Twice)
5. **Scan for Architectural Drift**: Use `improve-codebase-architecture` to identify shallow modules, leaky abstractions, or temporal coupling.
6. **Design Deeper Interfaces**: Apply `codebase-design` to create deep modules: simple, narrow interfaces that hide substantial internal complexity. Sketch at least two alternative seam locations before committing.
7. **Record Material Decisions**: Use `documentation-and-adrs` to log architectural trade-offs in `docs/adr/ADR-NNN-[slug].md` if public seams or structural patterns change.

## 4. Incremental Surgical Execution
8. **Plan Small Slices**: Use `planning-and-task-breakdown` if the refactor spans multiple subsystems.
9. **Refactor in Micro-Steps**: Apply `code-simplification` and `incremental-implementation`. Make one isolated change at a time (e.g. extract method, encapsulate field, replace conditional with polymorphism).
10. **Continuous Regression Check**: Run the test suite after each micro-step. Never accumulate unverified changes. If tests fail, use `systematic-debugging` to isolate the divergence immediately.

## 5. Review & Verification Gate
11. **Verify Behavior Preservation**: Run the full project test suite, typecheck, and strict linters.
12. **Collect Evidence**: Execute `verification-before-completion` to capture fresh terminal output proving zero behavioral regressions.
13. **Diff Review**: Inspect `git diff` using `code-review-and-quality` to confirm that no accidental side-effects, unwanted formatting noise, or commented-out code remain.