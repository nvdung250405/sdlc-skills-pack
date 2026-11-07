# Full SDLC workflow (System & Initiative Lifecycle)

> **Document type:** Standardized Workflow Definition  
> **Workflow:** `full-sdlc`  
> **Scenario Group:** Construction  
> **Trigger / Input:** Complex initiatives, greenfield projects, system establishment, multi-team features  
> **Primary Stages:** Discovery → Requirements → Architecture → Planning → Implementation → Testing → Review → Release → Operations  
> **Key Output:** Full feature release, system architecture overview, validated production deliverables  
> **Verification / Exit Gate:** Full test suite passing, empirical acceptance report, release checklist approved  

---


Use for new systems, major capabilities, complex integrations, or material-risk initiatives. This workflow coordinates foundational system establishment, enforces cross-cutting stage-gate reviews at every hand-off, delegates individual capabilities to `workflows/feature-loop.md`, and governs system-level release, observability, and operations.

Activities are iterative, overlapping, and non-linear. Skip artifacts that add no value and record why.

---

## Phase 1: Foundation, Product Scope & Centralized Architecture

### Discovery
1. Read repository context, architectural constraints, and constitution (`AGENTS.md` / `constitution.md`).
2. Run `interview-me` and `idea-refine` when problem framing or target users are ambiguous; use `analytics` for quantitative data if available.
3. Scaffold `docs/discovery/[initiative]/opportunity-brief.md` (from `templates/specs/opportunity-brief.md`) to capture problem framing, target persona, and initial hypotheses.
4. **Stage-Gate Review (Discovery Hand-off):** Verify problem clarity and evidence validity. If the problem framing remains speculative or ungrounded, pause and revisit `interview-me` before authoring product requirements.

### Requirements
5. Author or update `docs/prd.md` (from `templates/specs/PRD.md`) with `spec-driven-development` (evidence, measurable outcomes, epic breakdowns, non-goals, and identified risks). Run formal requirements specification (`docs/specs/SRS.md`, `docs/specs/RTM.md`) only when regulatory traceability is mandatory.
6. **Stage-Gate Review (Requirements Hand-off via Cross-Cutting Audit):**
   - Review `docs/prd.md` with `spec-driven-development` to identify build-damaging ambiguities, missing alternative flows, hidden assumptions, or unmeasurable acceptance criteria.
   - Ensure requirements are clear, concise, and unambiguous for autonomous agents.
   - **Gate Decision:** If *Critical* or *High-severity* gaps are uncovered, do not proceed to Architecture. Return to Step 5 to resolve requirements deficiencies first.

### Architecture & System Design
7. Establish component boundaries, C4 models, subsystem responsibilities, and data ownership in `docs/architecture.md` (from `templates/specs/architecture-overview.md`) using `software-architecture`.
8. **Establish Centralized System Contracts (Contract-First):**
   - Use `api-and-interface-design` to define top-level inter-service contracts, public API gateway specifications (OpenAPI/REST, GraphQL, gRPC `.proto`), and shared asynchronous event schemas before designing internal storage.
   - Ensure clear domain boundaries and deep module seams across subsystems.
   - Apply `api-contract-testing` to generate wire-level compatibility fixtures and provider-consumer contract tests based on these centralized specifications.
9. Define persistence architecture with `database-design`: select database engines (relational/document/time-series), ORM/data access layers, replication, connection pooling, and data partitioning strategies. Align persistence schemas and indexing models to support the established system contracts. Record architectural decisions and trade-offs in `docs/adr/ADR-NNN-[slug].md` (from `templates/specs/ADR.md`) using `documentation-and-adrs`.
10. **Stage-Gate Review (Architecture Hand-off via Security & Resources):**
    - Apply `security-and-hardening` to produce a STRIDE-A threat model and verify trust boundaries in `docs/security/threat-model-[system].md` (from `templates/governance/threat-model.md`).
    - Evaluate infrastructure sizing and resource allocations.
    - **Gate Decision:** If unmitigated critical security risks or unsustainable cost projections exist, halt progression. Revise architecture and ADRs in Step 7–9 before delegating construction.

### Platform & Developer Experience (cross-cutting setup)
11. Configure automated quality gates, linting, and commit-time formatting using `ci-cd-and-automation` and `git-workflow-and-versioning`.
12. Establish base containerization or build environments using `docker-expert` or platform templates when containerized delivery is needed.

---

## Phase 2: Incremental Capability Delivery (Feature Loop Delegation)

### Planning & Task Breakdown
13. Prioritize epics from `docs/prd.md`. Use `planning-and-task-breakdown` to sequence independent capabilities and identify blocking dependency edges.

### Implementation & Construction
14. For each epic or capability defined in `docs/prd.md`, delegate to `workflows/feature-loop.md`:
    - Author canonical feature specification in `docs/features/<feature-id>/spec.md` with `pm-user-story` (Stories & BDD Given/When/Then AC).
    - Plan tasks in `docs/features/<feature-id>/tasks.md` with `planning-and-task-breakdown`.
    - Execute the TDD construction loop (`incremental-implementation`, `test-driven-development`).
    - Use the Subagent Dispatch Protocol (`workflows/agent-handoff-contract.md`) when orchestrating independent feature loops in parallel across isolated subagent workspaces (binding `test-driven-development` to Implementers and `code-review-and-quality` to Reviewers).
    - Maintain active progress and role hand-offs using `task-handoff` (`.agent/tasks/<task-id>.md`).
    - Collect empirical verification evidence for each capability before completing its slice.

---

## Phase 3: System Integration, Release & Operations

### Testing & Verification (System-Level)
15. Verify cross-service integration contracts and wire compatibility using `api-contract-testing`.
16. Execute end-to-end automated flows with `webapp-testing` (Playwright).
17. Run load, stress, and scalability benchmarks with `k6-load-testing` when throughput or latency SLAs are critical; audit frontend accessibility with `frontend-ui-engineering`.

### Review & Acceptance
18. Conduct multi-axis code review with `code-review-and-quality` when processing review feedback.
19. Generate the pull request description from `templates/delivery/pull-request.md` with explicit summary, motivation, and commands run.
20. **Stage-Gate Review (Acceptance Gate):**
    - Run `verification-before-completion` to gather fresh, empirical test evidence across the whole system.
    - Record overall acceptance verification in `docs/features/<feature-id>/acceptance-report.md` (from `templates/delivery/acceptance-report.md`).
    - **Gate Decision:** If any required check fails, regressions appear, or test evidence is missing, do not proceed to release. Loop back to Implementation or Testing to resolve issues.

### Release & Deployment
21. Prepare release notes and changelog in `docs/releases/v[X.Y.Z].md` (from `templates/delivery/release-notes.md`) using `git-workflow-and-versioning` for semantic tagging.
22. Validate deployment safety, migration readiness, and rollback procedures against `templates/delivery/release-checklist.md` with `shipping-and-launch` and `ci-cd-and-automation`.
23. Audit cloud resource allocation and configuration before production rollout.
24. Production deployments and destructive actions require explicit human authorization.

### Operations & Incident Response
25. Configure dashboards, error alert thresholds, and SLO tracking with `observability-and-instrumentation`.
26. Publish operational runbook in `docs/runbooks/[service-name].md` (from `templates/platform/runbook.md`).
27. For production anomalies or outages, transition immediately to `workflows/incident-response.md`.

### Product Learning & Measurement
28. Define product telemetry taxonomy in `docs/analytics/tracking-plan.md` using `analytics` to measure funnel metrics and adoption.
29. Design and evaluate continuous experiments using `analytics` in `docs/experiments/[id].md` (via `workflows/experimentation-loop.md`).

---

## Control Rules
- **Stage-Gate Quality Invariant:** Hand-offs between stages require explicit cross-cutting review. If gate criteria are not satisfied, loop back to the deficient stage rather than advancing.
- **Non-Linear Execution:** Stage titles define capability domains matching the Master Matrix, not rigid sequential waterfall gates. Return to earlier stages whenever new evidence or risks emerge.
- **Single Source of Truth:** One canonical artifact per scope; do not create duplicate PRDs, feature specs, or competing task lists.
- **Evidence Before Claims:** A planned test is not evidence; always report exact commands run and real terminal output.
- **Zero Fabricated Requirements:** If requirements are contradictory or missing, amend the owning spec instead of inventing behavior in code.