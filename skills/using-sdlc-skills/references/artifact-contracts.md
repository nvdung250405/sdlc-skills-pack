# Canonical Artifact & Template Contracts

This reference document defines the complete mapping and ownership rules for the pack's **32 lean canonical artifact templates** across all 16 SDLC stages.

---

## 1. Principles of Lean Artifact Ownership

1. **Starter Template vs. Canonical Artifact:**
   - Files in `templates/` (and router assets `assets/templates/`) are **starter templates / blueprints**.
   - They provide an initial skeleton with pre-defined sections, quality prompts, and required fields.
   - When initiating work, the agent or engineer copies or scaffolds the template to the **Canonical Destination Path** on disk and populates it with real project context.
   - **Never maintain duplicate files** (e.g., do not create both `feature-spec.md` and `spec.md` for the same feature).
2. **Native Canonical Formats (Contract-First):**
   - Technical interfaces use their native machine-executable format: REST APIs use OpenAPI 3.1 (`.yaml`), messaging events use AsyncAPI (`.yaml`), realtime channels use STOMP (`.yaml`), RPCs use Protobuf (`.proto`), queries use GraphQL (`.graphql`), and schemas use JSON Schema / SQL DDL.
3. **No Stack-Dependent Template Bloat:**
   - Repository-specific environments (`devcontainer.json`, `ci.yaml`, `.env.example`) are generated dynamically by specialist skills (`docker-expert`, `ci-cd-and-automation`, `incremental-implementation`) tailored to the project's real language and tooling.
4. **Consolidated Verification Evidence:**
   - `delivery/acceptance-report.md` serves as the single source of truth for all pre-completion evidence: automated tests, contract validation, security scans, and performance SLAs.

---

## 2. Complete Artifact & Template Mapping Table (32 Lean Canonical Artifacts)

| Stage | Starter Template | Native Format | Canonical Destination Path | Primary Owner Skill | Purpose / Description |
|---|---|---|---|---|---|
| **1. Discovery** | `templates/specs/opportunity-brief.md` | `.md` | `docs/discovery/[initiative]/opportunity-brief.md` | `interview-me`, `idea-refine`, `customer-research` | Problem framing, target users, research evidence, VoC, and initial hypotheses. |
| **2. Requirements** | `templates/specs/PRD.md` | `.md` | `docs/prd.md` | `pm-product-spec` | Product intent, user problems, measurable outcomes, epics, non-goals, and risks. |
| **2. Requirements** | `templates/specs/feature-spec.md` | `.md` | `docs/features/<feature-id>/spec.md` | `spec-driven-development`, `pm-user-story` | Canonical feature specification containing User Stories and BDD Given/When/Then AC. |
| **2. Requirements** | `templates/specs/SRS.md` | `.md` | `docs/specs/SRS.md` *(or `docs/srs.md`)* | `requirements-engineering` | Formal Software Requirements Specification for compliance-heavy or high-complexity projects. |
| **2. Requirements** | `templates/specs/RTM.md` | `.md` | `docs/specs/RTM.md` *(or `docs/rtm.md`)* | `requirements-engineering` | Requirements Traceability Matrix linking requirements to designs, tasks, and tests. |
| **3. Architecture** | `templates/specs/architecture-overview.md` | `.md` | `docs/architecture.md` | `software-architecture` | System boundaries, C4 models, component breakdown, and data ownership. |
| **3. Architecture** | `templates/specs/ADR.md` | `.md` | `docs/adr/ADR-NNN-[slug].md` | `documentation-and-adrs` | Architectural Decision Record capturing context, options considered, trade-offs, and cost. |
| **3. Architecture** | `templates/specs/DDS.md` | `.md` | `docs/features/<feature-id>/design.md` | `software-architecture`, `codebase-design` | Detailed Design Specification (LLD) for complex subsystem or data model changes. |
| **3. Architecture** | `templates/contracts/openapi.yaml` | `.yaml` | `contracts/openapi.yaml` | `api-and-interface-design` | Machine-executable REST API contract (OpenAPI 3.1) with consistent error semantics. |
| **3. Architecture** | `templates/contracts/asyncapi.yaml` | `.yaml` | `contracts/asyncapi.yaml` | `api-and-interface-design` | Event-driven messaging contract (AsyncAPI 3.0 / CloudEvents) for Kafka/RabbitMQ. |
| **3. Architecture** | `templates/contracts/stomp-websocket.yaml` | `.yaml` | `contracts/stomp-websocket.yaml` | `api-and-interface-design` | STOMP 1.2 protocol & WebSocket frames contract for real-time messaging. |
| **3. Architecture** | `templates/contracts/service.proto` | `.proto` | `contracts/service.proto` | `api-and-interface-design` | Protocol Buffers v3 RPC interface contract for gRPC / internal microservices. |
| **3. Architecture** | `templates/contracts/schema.graphql` | `.graphql` | `contracts/schema.graphql` | `api-and-interface-design` | GraphQL SDL schema contract defining Queries, Mutations, and Subscriptions. |
| **3. Architecture** | `templates/contracts/data-contract.json` | `.json` | `contracts/data-contract.json` | `domain-modeling`, `database-design` | Canonical JSON Schema Draft 2020-12 data contract for domain entity models. |
| **3. Architecture** | `templates/contracts/migration.sql` | `.sql` | `migrations/[timestamp]_[id].sql` | `database-design` | Reversible, transactional SQL schema migration with expand/contract support. |
| **4. Planning** | `templates/delivery/plan.md` | `.md` | `docs/features/<feature-id>/plan.md` | `spec-driven-development` | Implementation strategy, technical context, and governance checks. |
| **4. Planning** | `templates/delivery/tasks.md` | `.md` | `docs/features/<feature-id>/tasks.md` | `planning-and-task-breakdown` | Single authoritative task list with dependency edges, files, and verification commands. |
| **4. Planning** | `templates/delivery/task-handoff.md` | `.md` | `.agent/tasks/<task-id>.md` | `task-handoff` | Active session state, progress log, and cross-agent / cross-session handoff notes. |
| **6. Verification** | `templates/delivery/acceptance-report.md` | `.md` | `docs/features/<feature-id>/acceptance-report.md` | `verification-before-completion` | Consolidated empirical verification: tests, contract lint, security scans & SLAs. |
| **6. Verification** | `templates/delivery/completion-report.md` | `.md` | `docs/features/<feature-id>/completion-report.md` | `verification-before-completion`, `task-handoff` | Minimum Completion Report: Status, Deliverables, Verification commands/evidence, Limitations. |
| **7. Review** | `templates/delivery/pull-request.md` | `.md` | `.github/pull_request_template.md` *(or PR body)* | `code-review-and-quality` | PR description, change motivation, test evidence, and reviewer checklist. |
| **8. Release** | `templates/delivery/release-notes.md` | `.md` | `docs/releases/v[X.Y.Z].md` | `shipping-and-launch` | Release highlights, detailed changelog, breaking changes, and deployment procedures. |
| **8. Release** | `templates/delivery/release-checklist.md` | `.md` | `docs/releases/release-checklist.md` | `shipping-and-launch` | Pre-deployment quality, security, operations, and rollback readiness gates. |
| **9. Operations** | `templates/platform/incident-postmortem.md` | `.md` | `docs/incidents/[YYYYMMDD-slug]/postmortem.md` | `observability-and-instrumentation` | Root cause analysis (5 Whys), outage timeline, impact metrics, and action items. |
| **9. Operations** | `templates/platform/runbook.md` | `.md` | `docs/runbooks/[service-name].md` | `observability-and-instrumentation` | Operational triage, service health SLOs, diagnostic commands, and recovery runbooks. |
| **9. Operations** | `templates/platform/alert-rules.yaml` | `.yaml` | `deploy/alerts/[service]-rules.yaml` | `observability-and-instrumentation`, `service-mesh-observability` | Prometheus alert definitions, latency/error rate thresholds, and runbook links. |
| **10. Evolution** | `templates/delivery/deprecation-notice.md` | `.md` | `docs/migrations/[slug]-deprecation.md` | `deprecation-and-migration` | Sunset timeline, breaking change warnings, and 4-phase Expand/Contract zero-downtime guides. |
| **11. Learning** | `templates/governance/tracking-plan.md` | `.md` | `docs/analytics/tracking-plan.md` | `analytics` | Event tracking taxonomy, trigger conditions, property schemas, and privacy guardrails. |
| **11. Learning** | `templates/governance/event-schema.json` | `.json` | `analytics/schemas/[event].json` | `analytics` | JSON Schema validating product telemetry tracking payloads before ingestion. |
| **11. Learning** | `templates/governance/experiment-brief.md` | `.md` | `docs/experiments/[exp-id]-[slug].md` | `ab-testing` | A/B testing design, falsifiable hypothesis, sample sizing, variants, and statistical results. |
| **12. Security** | `templates/governance/threat-model.md` | `.md` | `docs/security/threat-model-[system].md` | `threat-model-analyst` | STRIDE-A threat analysis, data flow diagrams (DFD), trust boundaries, and mitigations. |
| **14. Governance** | `templates/governance/constitution.md` | `.md` | `AGENTS.md` / `docs/constitution.md` | `context-engineering`, `writing-for-agents` | Project constitution, agent guardrails, coding conventions, and architectural invariants. |

---

## 3. Scaffolding Automation

To scaffold any canonical artifact instantly, use the CLI tool:
```bash
python scripts/scaffold.py <alias> [--id <id>] [--title <title>]
```

Supported aliases (32 aliases across 5 groups):
- **Specs (`specs/`):** `brief`, `prd`, `spec`, `srs`, `rtm`, `arch`, `adr`, `design`
- **Contracts (`contracts/`):** `openapi`, `asyncapi`, `stomp`, `proto`, `graphql`, `data-contract`, `migration`
- **Delivery (`delivery/`):** `plan`, `tasks`, `handoff`, `acceptance`, `completion`, `pr`, `release`, `checklist`, `deprecation`
- **Platform (`platform/`):** `alert-rules`, `runbook`, `postmortem`
- **Governance (`governance/`):** `constitution`, `threat-model`, `tracking`, `event-schema`, `experiment`
