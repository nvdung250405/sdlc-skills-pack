---
name: using-sdlc-skills
description: Routes a software task through the selected portable SDLC workflows and skills. Use at the start of a non-trivial feature, bug fix, refactor, requirements/design task, release, incident, handoff, or when selecting the next skill.
---

# Using the SDLC skill pack

This is the **only default pack-level router**. Classify the task, select the smallest adequate workflow, call only the skills needed, and ensure each stage hands off its output through the canonical artifact contract. Do not duplicate detailed procedures already owned by selected skills.

## Demand-Driven Skill Loading

The pack separates installation from active prompt loading. With **26 Core skills** (default engineering discipline) and **37 Extras skills** (specialized domain/stack capabilities), agents follow a 5-step demand-driven lifecycle:

```
Task Intake ──► Discover & Select ──► Load & Scaffold ──► Execute Work ──► Verify & Handoff
      │                 │                     │                   │                 │
  Classify       Workflow + Skills       Read Workflow &      Domain Work      Evidence-backed
   Stage          + Template             Scaffold Template   (Code/Spec/Design)   Check
```

1. **Task Intake & Stage Classification**: Analyze user request context and map it to the corresponding SDLC Stage (Discovery, Requirements, Architecture, Planning, Implementation, Testing, Review, Release, Operations, Maintenance, Learning, Security, Platform, Governance, Docs, Cost).
2. **Discover & Select (The SDLC Triad: Workflow, Skills, Artifact)**:
   - **Target Workflow:** Resolve the procedural workflow governing the task (e.g. `full-sdlc.md`, `feature-loop.md`, `bug-fix.md`, `quick-change.md`, `incident-response.md`, `experimentation-loop.md`, `deprecation-and-migration.md`, `agent-handoff-contract.md`). Read from `workflows/<name>.md` or router assets `assets/workflows/<name>.md`.
   - **Target Skills:** Select the Smallest Sufficient Set. Core skills are always **installed** (available on disk) but not all loaded into context simultaneously — load only the skills actually needed for this task step. Add Extras specialist skills based on tech stack, cloud, or domain when they supply distinct required capability.
   - **Artifact & Starter Template Resolution:** Determine if the task produces a canonical artifact. If yes, select the matching starter template (e.g., `feature-spec.md`, `ADR.md`, `architecture-overview.md`, `tasks.md`, `incident-postmortem.md`, `threat-model.md`).
3. **Load Workflow & Scaffold Template**:
   - Load the procedural steps from the resolved workflow into active context.
   - Retrieve the starter template from `templates/<name>.md` (workspace) or `assets/templates/<name>.md` (router bundled assets).
   - Scaffold the skeleton into the project's **Canonical Destination Path** (e.g. `docs/features/<feature-id>/spec.md`, `docs/architecture.md`, `docs/adr/ADR-NNN-[slug].md`) before filling domain content.
4. **Execute with Selected Skills**: Follow the loaded workflow sequence and apply domain skills to populate the scaffold with real business logic, BDD Given/When/Then acceptance criteria, architecture models, or implementation code.
5. **Verify Output Contract & Handoff**: Prove completion with fresh empirical evidence (`verification-before-completion`), record session handoff in `.agent/tasks/<task-id>.md` (`task-handoff`), and unload transient context.

## Choose a workflow

| User intent / change type | Route |
|---|---|
| Idea unclear or business problem unknown | `interview-me` → `idea-refine`; use `customer-research` for user insight synthesis and `pm-product-spec` once problem/assumptions are grounded. |
| New product or major initiative | Follow `workflows/full-sdlc.md`: `interview-me` / `idea-refine` as needed → `pm-product-spec` → optional `pm-spec-quality-audit` → formal `requirements-engineering` only when SRS/FR/NFR/UC/RTM are justified → `software-architecture` when system boundaries or material quality attributes need design. |
| New user-facing feature | Follow `workflows/feature-loop.md`: `pm-product-spec` if product intent/scope is not already defined → `pm-user-story` to author Story and Given/When/Then AC in the canonical feature spec → `pm-spec-quality-audit` for significant/ambiguous/high-risk specs → `spec-driven-development` to structure spec/plan/tasks when useful → architecture/API/UI skills only when the change warrants them → `planning-and-task-breakdown` → implementation and verification. |
| Small, clear feature/change | Follow `workflows/quick-change.md`: Read repository guidance/context → `spec-driven-development` only if a feature spec is missing or behavior is ambiguous → `incremental-implementation` and `test-driven-development` when behavior changes → `verification-before-completion` → `code-review-and-quality` as risk warrants. |
| Bug or unexpected behavior | Follow `workflows/bug-fix.md`: `systematic-debugging` → reproduce and isolate the root cause → regression test/TDD where practical → smallest fix → project verification → `verification-before-completion` and review. |
| Refactor / Code simplification | Follow `workflows/refactoring.md`: establish characterization tests → `improve-codebase-architecture` and `codebase-design` for deep modules → `code-simplification` micro-steps → regression verification. |
| Architecture review & deep modules | `software-architecture` for component boundaries and C4 models → `codebase-design` for deep module design → `domain-modeling` for ubiquitous language and glossaries → `documentation-and-adrs` for decisions with trade-offs. |
| Codebase architecture improvement | `improve-codebase-architecture` to scan for shallow modules, leaky abstractions, or architectural drift → propose incremental remedies. |
| Tracer-bullet ticket breakdown | `to-tickets` to convert plans or specifications into self-contained tracer-bullet task tickets declaring explicit dependency edges. |
| API/schema/integration change | `api-and-interface-design` plus `software-architecture` when system boundaries or major data ownership change. **Contract-First Rule:** Always scaffold executable contracts (`contracts/openapi.yaml`, `contracts/asyncapi.yaml`, `contracts/stomp-websocket.yaml`, `contracts/service.proto`, `contracts/schema.graphql`, `contracts/data-contract.json`); **never** generate unstructured prose markdown such as `api.md` → `api-contract-testing` for wire-level consumer-provider compatibility and regression fixtures → ADR only for meaningful trade-offs → plan and implementation. |
| System / schema / API migration | Follow `workflows/deprecation-and-migration.md`: use `deprecation-and-migration` and `database-design` for 4-phase Expand/Contract zero-downtime transition; coordinate with `code-simplification`. |
| Database schema / persistence design | `database-design` to select database/ORM, design normalized tables, indexing strategy and safe migrations; coordinate with `software-architecture`. |
| React / Next.js web application | `vercel-react-best-practices` for eliminating waterfalls, optimizing RSC boundaries, bundle size, and rendering performance; coordinate with `frontend-ui-engineering` and `frontend-design`. |
| Multi-agent / subagent orchestration | `subagent-driven-development` to orchestrate parallel implementation streams with isolated subagents and independent review gates. |
| Authentication / authorization flow | `auth-implementation-patterns` for session/token lifecycles, OAuth2/OIDC boundaries and RBAC policy enforcement; coordinate with `security-and-hardening`. |
| Threat modeling & security analysis | `threat-model-analyst` for STRIDE threat modeling, data-flow diagrams, and abuse cases; coordinate with `security-and-hardening`. |
| Secrets & CI credential handling | `secrets-management` for secret stores, workload identity and credential rotation; coordinate with `ci-cd-and-automation`. |
| Performance profiling & optimization | Follow `workflows/performance-tuning.md`: baseline benchmark with `k6-load-testing` / DevTools → bottleneck profiling (`database-design`, profilers) → surgical fix with `performance-optimization` → comparative before/after verification. |
| Dependency / library / CVE upgrade | Follow `workflows/dependency-upgrade.md`: audit changelogs / CVEs with `security-and-hardening` → isolated workspace via `using-git-worktrees` → update manifests & lockfiles → fix breaking changes → verify regressions. |
| Container / platform orchestration | `docker-expert` for container optimization/hardening; `kubernetes-architect` for cluster orchestration and GitOps; `terraform-specialist` for IaC module design and state. |
| Service mesh & distributed tracing | `service-mesh-observability` for Istio/Linkerd telemetry, distributed tracing, envoy metrics, and communication SLOs. |
| Cloud cost governance & FinOps | `cost-optimization` for resource rightsizing, spend anomaly detection, tagging enforcement, and multi-cloud cost reduction. |
| Accessibility / screen-reader audit | `screen-reader-testing` for screen-reader and ARIA accessibility verification; coordinate with `webapp-testing`. |
| Visual & web design review | `web-design-guidelines` for typography, spacing, responsive layout, and modern CSS guidelines; `frontend-design` for visual aesthetic direction. |
| Product analytics & experimentation | Follow `workflows/experimentation-loop.md`: `analytics` for event tracking taxonomy and funnel metrics; `ab-testing` for hypothesis formulation, variant split, and statistical significance. |
| Pre-commit hooks & agent guardrails | `setup-pre-commit` for pre-commit hook automation; `git-guardrails-claude-code` for safe autonomous git operations. |
| AI prompt & MCP server authoring | `writing-for-agents` for crafting high-leverage LLM instructions; `mcp-builder` for constructing Model Context Protocol tools; `skill-authoring` for pack maintenance. |
| Technical document authoring | `doc-coauthoring` for collaborative technical writing; `writing-guidelines` for concise editorial standards; `documentation-and-adrs` for architecture records. |
| Formal requirements or compliance-heavy system | `requirements-engineering` owns SRS/FR/NFR/use cases/RTM as appropriate; then architecture and feature spec. Never force this flow on a simple bug or small feature. |
| Spec/PRD/Story audit | `pm-spec-quality-audit`; for technical cross-document consistency manually follow the canonical links and requirement IDs. Do not change code unless asked. |
| Security-sensitive change | Pull security considerations into requirements/design, then `security-and-hardening` during implementation/review; record unmitigated risks and require appropriate approval. |
| Web UI runtime verification | Choose `webapp-testing` for Playwright automation or `browser-testing-with-devtools` for DevTools/MCP inspection. Use both only when they supply distinct needed evidence. |
| Release / deployment | `verification-before-completion` → `code-review-and-quality` and `security-and-hardening` as applicable → `ci-cd-and-automation` → `shipping-and-launch` → `observability-and-instrumentation`; production/destructive operations require approval. |
| Production incident | Follow `workflows/incident-response.md` first to mitigate/restore; only then use `systematic-debugging` for root cause and regression work. |
| Transfer between sessions/agents | Follow `workflows/agent-handoff-contract.md`: `task-handoff` first; use `using-git-worktrees` when an isolated workspace is appropriate; read linked authoritative files, not copied summaries alone. |
| Finish a development branch | `verification-before-completion` → `code-review-and-quality` → `git-workflow-and-versioning`; follow repository merge/PR policy. |

## Canonical artifact contract

Use repository-native conventions if equivalent artifacts already exist. Otherwise prefer:

- `docs/discovery/[initiative]/opportunity-brief.md`: problem framing, target users, validation findings and initial hypothesis (seeded from `templates/opportunity-brief.md`).
- `docs/constitution.md` (or `AGENTS.md`): context, constraints, engineering policies and Definition of Done (seeded from `templates/constitution.md`).
- `docs/prd.md`: product intent, problem/evidence, goals/metrics, non-goals, epics, risks and assumptions; optional for small changes (seeded from `templates/PRD.md`).
- `docs/features/<feature-id>/spec.md`: canonical feature specification, containing User Stories, stable `US-*` IDs, `AC-*` Given/When/Then scenarios where appropriate, rules, edge cases, dependencies and open questions (seeded from `templates/feature-spec.md`).
- `docs/specs/SRS.md` (or `docs/srs.md`): optional formal system requirements for complex or compliance-heavy work (seeded from `templates/SRS.md`).
- `docs/specs/RTM.md` (or `docs/rtm.md`): optional requirement-to-design/task/test traceability ledger for projects that need it (seeded from `templates/RTM.md`).
- `docs/architecture.md`: system architecture overview, boundaries, C4 models, and data ownership (seeded from `templates/architecture-overview.md`).
- `docs/adr/ADR-NNN-[slug].md`: architecture decision records with trade-offs and options considered (seeded from `templates/ADR.md`).
- `docs/features/<feature-id>/design.md` (or `technical-design.md`): detailed design specification only when needed (seeded from `templates/DDS.md`).
- `docs/features/<feature-id>/plan.md`: implementation plan and execution strategy (seeded from `templates/plan.md`).
- `docs/features/<feature-id>/tasks.md`: the single authoritative final task list for that feature (seeded from `templates/tasks.md`).
- `.agent/tasks/<task-id>.md`: active task session state, progress, and role handoffs (seeded from `templates/task-handoff.md`).
- `docs/features/<feature-id>/acceptance-report.md`: verification evidence for non-trivial features/releases (seeded from `templates/acceptance-report.md`).
- `.github/pull_request_template.md` (or PR body): pull request description, motivation, and verification evidence (seeded from `templates/pull-request.md`).
- `docs/releases/v[X.Y.Z].md`: release notes, changelog, and migration procedures (seeded from `templates/release-notes.md`).
- `docs/releases/release-checklist.md`: pre-deployment quality, security, and rollback readiness gates (seeded from `templates/release-checklist.md`).
- `docs/incidents/[YYYYMMDD-slug]/postmortem.md`: root cause investigations and corrective actions (seeded from `templates/incident-postmortem.md`).
- `docs/runbooks/[service-name].md`: operational runbooks, triage procedures, and health metrics (seeded from `templates/runbook.md`).
- `docs/migrations/[slug]-deprecation.md`: deprecation notices and 4-phase Expand/Contract zero-downtime guides (seeded from `templates/deprecation-notice.md`).
- `docs/experiments/[exp-id]-[slug].md`: growth experimentation briefs and hypothesis metrics (seeded from `templates/experiment-brief.md`).
- `docs/analytics/tracking-plan.md`: telemetry event tracking taxonomy and schemas (seeded from `templates/tracking-plan.md`).
- `docs/security/threat-model-[system].md`: STRIDE-A threat modeling and risk mitigations (seeded from `templates/threat-model.md`).

For the complete 22-row contract mapping table and CLI scaffolding aliases, see [references/artifact-contracts.md](references/artifact-contracts.md) or `templates/README.md`.

Templates in `templates/` (and router assets `assets/templates/`) are starters, not required extra documents. Do not create both `feature-spec.md` and `spec.md` for the same feature; copy the selected template into the canonical path instead of maintaining two authoritative files.

## Cross-skill invariants

1. **One artifact, one owner.** Product PRD is owned by `pm-product-spec`; detailed Story/AC by `pm-user-story`; formal system requirements and initial RTM rows by `requirements-engineering`; architecture by `software-architecture`; ADR rationale by `documentation-and-adrs`; final tasks by `planning-and-task-breakdown`.
2. **No duplicate routers.** This skill chooses the pack workflow. Skills such as `spec-driven-development` own a local procedure, not pack-level routing.
3. **Stable IDs.** Never invent references to absent documents, recycle IDs, or renumber downstream references. Retire removed IDs when traceability is in use.
4. **No fabricated facts.** Separate evidence, approved decisions, assumptions, unknown targets and proposed defaults.
5. **Specification precedes implementation when scope/behavior warrants it.** If reality contradicts an approved spec, propose an amendment and preserve the decision trail instead of silently rewriting the spec to justify code.
6. **Evidence before completion claims.** Use `verification-before-completion`; report exact commands/observations and their results. A written test plan is not test evidence.
7. **Tailor by risk.** Do not force PRD/SRS/DDS/RTM/ADR/Story onto every change. Do not force TDD on work where it does not fit, but require an explicit verification method.
8. **Fallback honestly.** If subagents, browser automation, MCP or a required command are unavailable, use a sequential/manual fallback and state that limitation.
9. **Approval boundaries.** Do not make production/destructive changes, change business scope, weaken release/security gates or accept material residual risk without the appropriate approval.
10. **Context discipline & anti-overload.** Never load all skills or full templates into the active prompt simultaneously. Load strictly on demand: 1 procedural workflow, the smallest sufficient set of skills (typically 1-2 Core + 0-1 Extras per step), and read/scaffold artifacts directly to disk. Pass file paths, never pasted document excerpts. Delegate sprawling explorations to subagents.

## Handoff

For multi-step work, maintain `.agent/tasks/<task-id>.md` with goal, artifacts read, decisions, changed files, tests/commands actually run, open risks and the next action. Re-read authoritative files at each handoff; avoid copying large excerpts.
