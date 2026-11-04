# Starter Artifact Templates Catalog

Thư mục `templates/` chứa **41 khuôn mẫu khởi tạo chuẩn hóa (Canonical Starter Templates & Blueprints)** tương ứng trực tiếp 1:1 với các tạo phẩm thực tế trong 16 giai đoạn của vòng đời phát triển phần mềm ([docs/sdlc-practical-matrix.md](../docs/sdlc-practical-matrix.md)).

---

## 1. Nguyên tắc Khế ước Tạo phẩm (Artifact Contract Principles)

- **Định dạng gốc chuẩn hóa (Native Canonical Formats):** Mỗi tạo phẩm được định hình bằng định dạng chuẩn của nó (không ép mọi thứ thành Markdown):
  - *Quản trị & Báo cáo:* Markdown (`.md`)
  - *Hợp đồng API & Dịch vụ:* OpenAPI 3.1 (`.yaml`), AsyncAPI 3.0 (`.yaml`), STOMP 1.2 (`.yaml`), Protobuf (`.proto`), GraphQL (`.graphql`), JSON Schema (`.json`), SQL DDL (`.sql`).
  - *Cấu hình & Vận hành:* YAML (`.yaml`), JSON (`.json`).
- **Khởi tạo trực tiếp trên đĩa (Disk Scaffolding):** Khi bắt đầu một giai đoạn, sử dụng `python scripts/scaffold.py <alias>` để sinh file mẫu trực tiếp ra đường dẫn chuẩn (*canonical destination path*) trong dự án thay vì dán nội dung vào cửa sổ chat.
- **Single Source of Truth:** Tuyệt đối không chỉnh sửa trực tiếp các tệp trong `templates/` cho một feature cụ thể; luôn làm việc trên file tại canonical path của dự án.

---

## 2. Bảng Danh mục 41 Canonical Templates theo 16 Giai đoạn SDLC

| Stage (Giai đoạn) | Starter Template | Định dạng chuẩn | Canonical Destination Path | Companion Skills |
| :--- | :--- | :--- | :--- | :--- |
| **1. Discovery** | [`opportunity-brief.md`](opportunity-brief.md)<br>[`research-synthesis.md`](research-synthesis.md)<br>[`experiment-brief.md`](experiment-brief.md) | `.md`<br>`.md`<br>`.md` | `docs/discovery/[initiative]/opportunity-brief.md`<br>`docs/discovery/[initiative]/research-synthesis.md`<br>`docs/experiments/[exp-id].md` | `interview-me`, `idea-refine`<br>`customer-research`<br>`ab-testing` |
| **2. Requirements** | [`PRD.md`](PRD.md)<br>[`feature-spec.md`](feature-spec.md)<br>[`SRS.md`](SRS.md)<br>[`RTM.md`](RTM.md) | `.md`<br>`.md`<br>`.md`<br>`.md` | `docs/prd.md`<br>`docs/features/[feature-id]/spec.md`<br>`docs/specs/SRS.md`<br>`docs/specs/RTM.md` | `pm-product-spec`<br>`pm-user-story`, `spec-driven-development`<br>`requirements-engineering`<br>`requirements-engineering` |
| **3. Architecture & Design** | [`architecture-overview.md`](architecture-overview.md)<br>[`ADR.md`](ADR.md)<br>[`DDS.md`](DDS.md)<br>[`openapi.yaml`](openapi.yaml)<br>[`asyncapi.yaml`](asyncapi.yaml)<br>[`stomp-websocket.yaml`](stomp-websocket.yaml)<br>[`service.proto`](service.proto)<br>[`schema.graphql`](schema.graphql)<br>[`data-contract.json`](data-contract.json)<br>[`design-tokens.json`](design-tokens.json) | `.md`<br>`.md`<br>`.md`<br>`.yaml`<br>`.yaml`<br>`.yaml`<br>`.proto`<br>`.graphql`<br>`.json`<br>`.json` | `docs/architecture.md`<br>`docs/adr/ADR-NNN-[slug].md`<br>`docs/features/[feature-id]/design.md`<br>`contracts/openapi.yaml`<br>`contracts/asyncapi.yaml`<br>`contracts/stomp-websocket.yaml`<br>`contracts/service.proto`<br>`contracts/schema.graphql`<br>`contracts/data-contract.json`<br>`design/tokens.json` | `software-architecture`<br>`documentation-and-adrs`<br>`codebase-design`<br>`api-and-interface-design`<br>`api-and-interface-design`<br>`api-and-interface-design`<br>`api-and-interface-design`<br>`api-and-interface-design`<br>`domain-modeling`, `database-design`<br>`frontend-design` |
| **4. Planning & Breakdown** | [`plan.md`](plan.md)<br>[`tasks.md`](tasks.md)<br>[`task-handoff.md`](task-handoff.md) | `.md`<br>`.md`<br>`.md` | `docs/features/[feature-id]/plan.md`<br>`docs/features/[feature-id]/tasks.md`<br>`.agent/tasks/[task-id].md` | `planning-and-task-breakdown`<br>`planning-and-task-breakdown`<br>`task-handoff` |
| **5. Implementation** | [`migration.sql`](migration.sql)<br>[`env.example`](env.example) | `.sql`<br>`dotenv` | `migrations/[timestamp]_[id].sql`<br>`.env.example` | `database-design`<br>`incremental-implementation`, `secrets-management` |
| **6. Testing & Verification** | [`acceptance-report.md`](acceptance-report.md)<br>[`benchmark-report.md`](benchmark-report.md) | `.md`<br>`.md` | `docs/features/[feature-id]/acceptance-report.md`<br>`docs/features/[feature-id]/benchmark-report.md` | `verification-before-completion`<br>`k6-load-testing`, `screen-reader-testing` |
| **7. Review & Acceptance** | [`pull-request.md`](pull-request.md)<br>[`acceptance-report.md`](acceptance-report.md) | `.md`<br>`.md` | `.github/pull_request_template.md`<br>`docs/features/[feature-id]/acceptance-report.md` | `code-review-and-quality`, `receiving-code-review`<br>`verification-before-completion` |
| **8. Release & Deployment** | [`release-notes.md`](release-notes.md)<br>[`release-checklist.md`](release-checklist.md)<br>[`ci-pipeline.yaml`](ci-pipeline.yaml) | `.md`<br>`.md`<br>`.yaml` | `docs/releases/v[X.Y.Z].md`<br>`docs/releases/release-checklist.md`<br>`.github/workflows/ci.yaml` | `shipping-and-launch`<br>`shipping-and-launch`<br>`ci-cd-and-automation` |
| **9. Operations & Incidents** | [`incident-postmortem.md`](incident-postmortem.md)<br>[`runbook.md`](runbook.md)<br>[`alert-rules.yaml`](alert-rules.yaml) | `.md`<br>`.md`<br>`.yaml` | `docs/incidents/[YYYYMMDD-slug]/postmortem.md`<br>`docs/runbooks/[service-name].md`<br>`deploy/alerts/[service]-rules.yaml` | `observability-and-instrumentation`<br>`observability-and-instrumentation`<br>`service-mesh-observability` |
| **10. Maintenance & Evolution** | [`deprecation-notice.md`](deprecation-notice.md)<br>[`migration.sql`](migration.sql) | `.md`<br>`.sql` | `docs/migrations/[slug]-deprecation.md`<br>`migrations/[timestamp]_[slug].sql` | `deprecation-and-migration`<br>`code-simplification` |
| **11. Product Learning** | [`experiment-brief.md`](experiment-brief.md)<br>[`tracking-plan.md`](tracking-plan.md)<br>[`event-schema.json`](event-schema.json) | `.md`<br>`.md`<br>`.json` | `docs/experiments/[exp-id].md`<br>`docs/analytics/tracking-plan.md`<br>`analytics/schemas/[event].json` | `ab-testing`<br>`analytics`<br>`analytics` |
| **12. Security & Privacy** | [`threat-model.md`](threat-model.md)<br>[`security-assessment.md`](security-assessment.md) | `.md`<br>`.md` | `docs/security/threat-model-[system].md`<br>`docs/security/security-assessment-[id].md` | `threat-model-analyst`<br>`security-and-hardening`, `secrets-management` |
| **13. Platform & DevEx** | [`devcontainer.json`](devcontainer.json)<br>[`pre-commit-config.yaml`](pre-commit-config.yaml) | `.json`<br>`.yaml` | `.devcontainer/devcontainer.json`<br>`.pre-commit-config.yaml` | `setup-pre-commit`<br>`git-guardrails-claude-code` |
| **14. AI Governance** | [`constitution.md`](constitution.md)<br>[`model-card.md`](model-card.md) | `.md`<br>`.md` | `AGENTS.md` / `CLAUDE.md`<br>`docs/ai/model-card-[id].md` | `using-sdlc-skills`, `writing-for-agents`<br>`context-engineering` |
| **15. Documentation** | [`README.md`](README.md)<br>[`runbook.md`](runbook.md)<br>[`architecture-overview.md`](architecture-overview.md) | `.md`<br>`.md`<br>`.md` | `README.md`<br>`docs/runbooks/[service].md`<br>`docs/architecture.md` | `doc-coauthoring`<br>`writing-guidelines` |
| **16. Cost Governance** | [`cost-attribution-report.md`](cost-attribution-report.md) | `.md` | `docs/finops/cost-report-[period].md` | `cost-optimization` |
