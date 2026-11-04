# Canonical Artifact & Template Contracts

This reference document defines the complete mapping and ownership rules for the pack's **41 canonical artifact templates** across all 16 SDLC stages.

---

## 1. Principles of Artifact Ownership

1. **Starter Template vs. Canonical Artifact:**
   - Files in `templates/` (and router assets `assets/templates/`) are **starter templates / blueprints**.
   - They provide an initial skeleton with pre-defined sections, quality prompts, and required fields.
   - When initiating work, the agent or engineer copies or scaffolds the template to the **Canonical Destination Path** on disk and populates it with real project context.
   - **Never maintain duplicate files** (e.g., do not create both `feature-spec.md` and `spec.md` for the same feature).
2. **Native Canonical Formats (Contract-First):**
   - Do not force non-prose technical interfaces into Markdown. REST APIs use OpenAPI 3.1 (`.yaml`), messaging events use AsyncAPI (`.yaml`), realtime channels use STOMP (`.yaml`), RPCs use Protobuf (`.proto`), queries use GraphQL (`.graphql`), and schemas use JSON Schema / SQL DDL.
3. **One Artifact, One Owner:**
   - Every artifact type has exactly one authoritative owner skill that governs its creation, structure, and amendments.
4. **Evidence Before Assertions:**
   - A written test plan or design checklist is not evidence. Artifacts recording verification (`acceptance-report.md`, `pull-request.md`, `benchmark-report.md`) must contain real terminal output and observed check results.

---

## 2. Complete Artifact & Template Mapping Table (41 Canonical Artifacts)

| Stage | Starter Template | Native Format | Canonical Destination Path | Primary Owner Skill | Purpose / Description |
|---|---|---|---|---|---|
| **1. Discovery** | `templates/opportunity-brief.md` | `.md` | `docs/discovery/[initiative]/opportunity-brief.md` | `interview-me`, `idea-refine` | Problem framing, target users, research evidence, and initial hypotheses. |
| **1. Discovery** | `templates/research-synthesis.md` | `.md` | `docs/discovery/[initiative]/research-synthesis.md` | `customer-research` | Voice of Customer (VoC), customer interviews, and market benchmarks. |
| **1. Discovery** | `templates/experiment-brief.md` | `.md` | `docs/experiments/[exp-id].md` | `ab-testing` | Hypothesis validation records and growth experiment briefs. |
| **2. Requirements** | `templates/PRD.md` | `.md` | `docs/prd.md` | `pm-product-spec` | Product intent, user problems, measurable outcomes, epics, non-goals, and risks. |
| **2. Requirements** | `templates/feature-spec.md` | `.md` | `docs/features/<feature-id>/spec.md` | `spec-driven-development`, `pm-user-story` | Canonical feature specification containing User Stories and BDD Given/When/Then AC. |
| **2. Requirements** | `templates/SRS.md` | `.md` | `docs/specs/SRS.md` *(or `docs/srs.md`)* | `requirements-engineering` | Formal Software Requirements Specification for compliance-heavy or high-complexity projects. |
| **2. Requirements** | `templates/RTM.md` | `.md` | `docs/specs/RTM.md` *(or `docs/rtm.md`)* | `requirements-engineering` | Requirements Traceability Matrix linking requirements to designs, tasks, and tests. |
| **3. Architecture** | `templates/architecture-overview.md` | `.md` | `docs/architecture.md` | `software-architecture` | System boundaries, C4 models, component breakdown, and data ownership. |
| **3. Architecture** | `templates/ADR.md` | `.md` | `docs/adr/ADR-NNN-[slug].md` | `documentation-and-adrs` | Architectural Decision Record capturing context, options considered, and trade-offs. |
| **3. Architecture** | `templates/DDS.md` | `.md` | `docs/features/<feature-id>/design.md` | `software-architecture`, `codebase-design` | Detailed Design Specification (LLD) for complex subsystem or data model changes. |
| **3. Architecture** | `templates/openapi.yaml` | `.yaml` | `contracts/openapi.yaml` | `api-and-interface-design` | Machine-executable REST API contract (OpenAPI 3.1) with consistent error semantics. |
| **3. Architecture** | `templates/asyncapi.yaml` | `.yaml` | `contracts/asyncapi.yaml` | `api-and-interface-design` | Event-driven messaging contract (AsyncAPI 3.0 / CloudEvents) for Kafka/RabbitMQ. |
| **3. Architecture** | `templates/stomp-websocket.yaml` | `.yaml` | `contracts/stomp-websocket.yaml` | `api-and-interface-design` | STOMP 1.2 protocol & WebSocket frames contract for real-time messaging. |
| **3. Architecture** | `templates/service.proto` | `.proto` | `contracts/service.proto` | `api-and-interface-design` | Protocol Buffers v3 RPC interface contract for gRPC / internal microservices. |
| **3. Architecture** | `templates/schema.graphql` | `.graphql` | `contracts/schema.graphql` | `api-and-interface-design` | GraphQL SDL schema contract defining Queries, Mutations, and Subscriptions. |
| **3. Architecture** | `templates/data-contract.json` | `.json` | `contracts/data-contract.json` | `domain-modeling`, `database-design` | Canonical JSON Schema Draft 2020-12 data contract for domain entity models. |
| **3. Architecture** | `templates/design-tokens.json` | `.json` | `design/tokens.json` | `frontend-design` | Design Tokens Community Group (W3C) UI design tokens specification. |
| **4. Planning** | `templates/plan.md` | `.md` | `docs/features/<feature-id>/plan.md` | `spec-driven-development` | Implementation strategy, technical context, and governance checks. |
| **4. Planning** | `templates/tasks.md` | `.md` | `docs/features/<feature-id>/tasks.md` | `planning-and-task-breakdown` | Single authoritative task list with dependency edges, files, and verification commands. |
| **4. Planning** | `templates/task-handoff.md` | `.md` | `.agent/tasks/<task-id>.md` | `task-handoff` | Active session state, progress log, and cross-agent / cross-session handoff notes. |
| **5. Implementation**| `templates/migration.sql` | `.sql` | `migrations/[timestamp]_[id].sql` | `database-design` | Reversible, transactional SQL schema migration with expand/contract support. |
| **5. Implementation**| `templates/env.example` | `dotenv` | `.env.example` | `incremental-implementation`, `secrets-management` | Environment boundary & feature flag configuration committed without secrets. |
| **6. Verification** | `templates/acceptance-report.md` | `.md` | `docs/features/<feature-id>/acceptance-report.md` | `verification-before-completion` | Empirical test evidence, build logs, and acceptance verification before completion. |
| **6. Verification** | `templates/benchmark-report.md` | `.md` | `docs/features/<feature-id>/benchmark-report.md` | `k6-load-testing`, `screen-reader-testing` | Performance, load (k6), and accessibility (WCAG) benchmark report. |
| **7. Review** | `templates/pull-request.md` | `.md` | `.github/pull_request_template.md` *(or PR body)* | `code-review-and-quality` | PR description, change motivation, test evidence, and reviewer checklist. |
| **8. Release** | `templates/release-notes.md` | `.md` | `docs/releases/v[X.Y.Z].md` | `shipping-and-launch` | Release highlights, detailed changelog, breaking changes, and deployment procedures. |
| **8. Release** | `templates/release-checklist.md` | `.md` | `docs/releases/release-checklist.md` | `shipping-and-launch` | Pre-deployment quality, security, operations, and rollback readiness gates. |
| **8. Release** | `templates/ci-pipeline.yaml` | `.yaml` | `.github/workflows/ci.yaml` | `ci-cd-and-automation` | CI/CD pipeline automation enforcing multi-tier quality gates. |
| **9. Operations** | `templates/incident-postmortem.md` | `.md` | `docs/incidents/[YYYYMMDD-slug]/postmortem.md` | `observability-and-instrumentation` | Root cause analysis (5 Whys), outage timeline, impact metrics, and action items. |
| **9. Operations** | `templates/runbook.md` | `.md` | `docs/runbooks/[service-name].md` | `observability-and-instrumentation` | Operational triage, service health SLOs, diagnostic commands, and recovery runbooks. |
| **9. Operations** | `templates/alert-rules.yaml` | `.yaml` | `deploy/alerts/[service]-rules.yaml` | `observability-and-instrumentation`, `service-mesh-observability` | Prometheus alert definitions, latency/error rate thresholds, and runbook links. |
| **10. Evolution** | `templates/deprecation-notice.md` | `.md` | `docs/migrations/[slug]-deprecation.md` | `deprecation-and-migration` | Sunset timeline, breaking change warnings, and 4-phase Expand/Contract zero-downtime guides. |
| **11. Learning** | `templates/tracking-plan.md` | `.md` | `docs/analytics/tracking-plan.md` | `analytics` | Event tracking taxonomy, trigger conditions, property schemas, and privacy guardrails. |
| **11. Learning** | `templates/event-schema.json` | `.json` | `analytics/schemas/[event].json` | `analytics` | JSON Schema validating product telemetry tracking payloads before ingestion. |
| **12. Security** | `templates/threat-model.md` | `.md` | `docs/security/threat-model-[system].md` | `threat-model-analyst` | STRIDE-A threat analysis, data flow diagrams (DFD), trust boundaries, and mitigations. |
| **12. Security** | `templates/security-assessment.md` | `.md` | `docs/security/security-assessment-[id].md` | `security-and-hardening`, `secrets-management` | Vulnerability scan results, dependency audit records, and privacy compliance checks. |
| **13. Platform** | `templates/devcontainer.json` | `.json` | `.devcontainer/devcontainer.json` | `setup-pre-commit` | Declarative developer container environment configuration. |
| **13. Platform** | `templates/pre-commit-config.yaml` | `.yaml` | `.pre-commit-config.yaml` | `setup-pre-commit`, `git-guardrails-claude-code` | Git pre-commit hooks enforcing whitespace, json/yaml syntax, and secrets scanning. |
| **14. Governance** | `templates/constitution.md` | `.md` | `AGENTS.md` / `docs/constitution.md` | `context-engineering`, `writing-for-agents` | Project constitution, agent guardrails, coding conventions, and architectural invariants. |
| **14. Governance** | `templates/model-card.md` | `.md` | `docs/ai/model-card-[id].md` | `using-sdlc-skills`, `context-engineering` | AI Model Card documenting intended use, safety guardrails, and benchmark results. |
| **16. Cost** | `templates/cost-attribution-report.md` | `.md` | `docs/finops/cost-report-[period].md` | `cost-optimization` | Infrastructure cloud spend, AI token budgeting, rightsizing, and FinOps metrics. |

---

## 3. Scaffolding Automation

To scaffold any canonical artifact instantly, use the CLI tool:
```bash
python scripts/scaffold.py <alias> [--id <id>] [--title <title>]
```

Supported aliases (41 aliases):
- **Discovery & Requirements:** `brief`, `research`, `experiment`, `prd`, `spec`, `srs`, `rtm`
- **Architecture & Contracts:** `arch`, `adr`, `design`, `openapi`, `asyncapi`, `stomp`, `proto`, `graphql`, `data-contract`, `tokens`
- **Planning & Construction:** `plan`, `tasks`, `handoff`, `migration`, `env`
- **Verification & Review:** `acceptance`, `benchmark`, `pr`, `release`, `checklist`, `ci`
- **Operations & Incidents:** `postmortem`, `runbook`, `alert-rules`, `deprecation`
- **Telemetry & Learning:** `tracking`, `event-schema`
- **Security & Platform:** `threat-model`, `security`, `devcontainer`, `pre-commit`
- **Governance & Cost:** `constitution`, `model-card`, `cost`
