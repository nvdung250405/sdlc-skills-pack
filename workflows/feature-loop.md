# Feature development loop

> **Document type:** Standardized Workflow Definition  
> **Workflow:** `feature-loop`  
> **Scenario Group:** Construction  
> **Trigger / Input:** Standard feature request, user story in existing codebase  
> **Primary Stages:** Spec & Stories → Contract-First Architecture → Planning → Construction (TDD) → Verification & Acceptance  
> **Key Output:** Working feature slice, automated unit/integration tests, canonical feature spec  
> **Verification / Exit Gate:** All AC tests green, DoD satisfied, `verification-before-completion` evidence recorded  

---


Use for implementing a feature in an existing codebase. Read existing repository context and guidance first. Do not fork a second artifact system.

---

## 1. Specification & Quality Gate
1. Identify feature scope and canonical spec path: `docs/features/<feature-id>/spec.md` (scaffold from `templates/specs/feature-spec.md` if not present).
2. If product intent is unsettled, consult or update `docs/prd.md` with `pm-product-spec`.
3. Use `pm-user-story` to add/refine user-facing stories and Given/When/Then Acceptance Criteria directly inside `docs/features/<feature-id>/spec.md`. For purely technical changes, use a technical spec or ADR instead of fabricating stories.
4. Run `pm-spec-quality-audit` if the specification is complex, ambiguous, or needs a pre-build quality gate.

## 2. Contract-First Architecture & Design Seams
5. Follow **Contract-First** design: establish observable interfaces and boundaries before internal persistence implementation:
   - **Interface & Wire Contracts (Contract-First):** Use `api-and-interface-design` and `api-contract-testing` to define REST/gRPC/GraphQL schemas, request/response models, and compatibility fixtures before modifying persistence layers.
   - **Persistence & Migration (Persistence Second):** Once interface contracts are defined, invoke `database-design` to design normalized tables, indexing strategy, and zero-downtime database migrations required to satisfy the contract.
   - **Component Boundaries & Models:** Use `software-architecture` when feature logic alters module seams, C4 diagrams, or domain ownership.
   - **Design Trade-offs:** Use `documentation-and-adrs` to record meaningful architectural decisions in `docs/adr/ADR-NNN-[slug].md` (from `templates/specs/ADR.md`).
   - **Security & Threat Surface:** Use `threat-model-analyst` and `security-and-hardening` if the feature crosses trust boundaries, handles credentials, or processes sensitive data.
   - **UI Styling & Tokens:** Use `frontend-design` and `frontend-ui-engineering` for design tokens and layout composition.

## 3. Planning & Task Breakdown
6. Use `planning-and-task-breakdown` as the **sole author** of the final `docs/features/<feature-id>/tasks.md` (from `templates/delivery/tasks.md`). Every task must specify target file paths, dependencies, acceptance conditions, and exact verification commands.

## 4. Construction & TDD Loop
7. Implement in thin, verifiable slices using `incremental-implementation`.
8. Write tests before code with `test-driven-development` where behavioral tests can drive the implementation. Ground unfamiliar APIs with `source-driven-development`.
9. For unexpected test failures or regressions, invoke `systematic-debugging`: reproduce, isolate root cause, state hypothesis, and add regression guard.

## 5. Review, Verification & Acceptance
10. Run relevant unit, integration, contract, and browser tests (webapp-testing or rowser-testing-with-devtools).
11. Conduct code review using code-review-and-quality; prepare PR description using 	emplates/delivery/pull-request.md.
12. Execute erification-before-completion to record fresh empirical evidence in docs/features/<feature-id>/acceptance-report.md (from 	emplates/delivery/acceptance-report.md) or completion-report.md.
13. Update session handoff log in .agent/tasks/<task-id>.md using 	ask-handoff.

---

> [!TIP]
> **Graceful Fallback for Extras Skills:**
> When specialist Extras skills are not installed on disk:
> - For API wire contracts without pi-contract-testing: validate syntax with scripts/verify_contracts.py and run project integration test fixtures.
> - For UI/Browser testing without webapp-testing or rowser-testing-with-devtools: execute standard project headless test runners (
pm test, pytest).
> - For threat modeling without 	hreat-model-analyst: rely on core security-and-hardening checks consolidated in cceptance-report.md.

> [!NOTE]
> If implementation uncovers an unexpected architecture, data migration, or security risk larger than initially estimated, pause and route back to the owning design/spec stage before continuing.
