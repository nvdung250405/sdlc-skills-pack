# SDLC Stage → Output → Selected Skills

Bản đồ định tuyến kỹ năng thực tế theo **16 giai đoạn chuẩn hóa quốc tế** (ISO/IEC/IEEE 12207, SWEBOK v4, NIST SSDF, DORA, FinOps). Router duy nhất của pack là `using-sdlc-skills` lựa chọn luồng làm việc tinh gọn nhất (right-sized) và áp dụng cơ chế **Nạp kỹ năng theo nhu cầu (Demand-Driven Skill Loading)**.

Pack phân tầng kỹ năng thành 2 cấp độ:
- **Core (29 skills)**: Kỷ luật công kỹ nghệ nền tảng, độc lập công cụ, cài đặt mặc định cho mọi agent trong mọi dự án.
- **Extras (34 skills)**: Năng lực chuyên sâu, nạp theo nhu cầu thực tế của ngữ cảnh dự án, stack công nghệ, vai trò chuyên môn hoặc hạ tầng.

---

## 1. Bảng điều hướng 16 Giai đoạn SDLC

| Stage (Giai đoạn) | Expected outputs (Tạo phẩm tinh gọn) | Core skills (Mặc định cài đặt) | Extras / Triggers (Nạp theo nhu cầu) |
|---|---|---|---|
| **Discovery** | • Opportunity brief (problem framing, target users, validation findings)<br>• Customer & market research synthesis<br>• Hypothesis validation records (khi theo dõi qua các vòng lặp) | `interview-me`<br>`idea-refine` | `customer-research` (khi cần nghiên cứu sâu insight người dùng, chân dung khách hàng, benchmark đối thủ) |
| **Requirements** | • Product Requirements Document (PRD)<br>• Feature specifications (User Stories & Acceptance Criteria)<br>• Requirements traceability & compliance records (theo ngữ cảnh dự án) | `requirements-engineering`<br>`spec-driven-development`<br>`pm-user-story`<br>`pm-product-spec`<br>`pm-spec-quality-audit` | *(Tất cả kỹ năng đặc tả yêu cầu cốt lõi đã thuộc Core)* |
| **Architecture & System Design** | • System architecture overview (components, boundaries, C4 models)<br>• Architecture Decision Records (ADRs)<br>• Interface & data contracts (OpenAPI, schemas, data models)<br>• UI component specifications & design system tokens | `software-architecture`<br>`api-and-interface-design`<br>`database-design`<br>`documentation-and-adrs` | `codebase-design` (khi thiết kế deep modules theo phong cách Matt Pocock)<br>`domain-modeling` (khi xây dựng glossary và domain model)<br>`frontend-design` (khi định hình phong cách thị giác và design tokens) |
| **Planning & Task Breakdown** | • Technical implementation plan & task breakdown (kèm DoD và ràng buộc kỹ thuật)<br>• Task handoff & context notes (khi cần bàn giao phiên) | `planning-and-task-breakdown`<br>`task-handoff` | `to-tickets` (khi bẻ khóa plan thành các ticket tracer-bullet dạng issue độc lập) |
| **Implementation & Construction** | • Mã nguồn ứng dụng & lịch sử commit nguyên tử có kiểm soát<br>• Automated unit & component test suites<br>• Database migrations & integration adapters<br>• Feature flags & cấu hình môi trường | `incremental-implementation`<br>`test-driven-development`<br>`source-driven-development`<br>`git-workflow-and-versioning`<br>`using-git-worktrees` | `subagent-driven-development` (khi điều phối song song qua subagents chuyên biệt)<br>`frontend-ui-engineering` (khi xây dựng giao diện người dùng web/di động phức tạp)<br>`vercel-react-best-practices` (khi tối ưu hóa ứng dụng React/Next.js theo chuẩn Vercel) |
| **Testing & Verification** | • Automated test suites (integration, E2E, contract)<br>• Kết quả thực thi test & chẩn đoán lỗi (trong CI hoặc test runner)<br>• Kết quả benchmark hiệu năng, tải và accessibility (khi đánh giá) | `verification-before-completion` | `webapp-testing` (khi kiểm thử E2E giao diện web bằng Playwright)<br>`browser-testing-with-devtools` (khi inspect DOM, console, network qua Chrome DevTools MCP)<br>`api-contract-testing` (khi kiểm thử tương thích hợp đồng API consumer/provider)<br>`k6-load-testing` (khi kiểm thử tải, stress test và đo ngưỡng SLA)<br>`screen-reader-testing` (khi kiểm toán trợ năng ARIA và screen reader) |
| **Review & Acceptance** | • Pull request review comments & merge approvals<br>• Acceptance verification (khi độc lập cổng nghiệm thu)<br>• Design & guideline conformance reviews | `code-review-and-quality`<br>`receiving-code-review` | `web-design-guidelines` (khi rà soát tuân thủ quy chuẩn thiết kế web và typography hiện đại) |
| **Release & Deployment** | • Versioned build artifacts và images (có ký số khi bắt buộc)<br>• Deployment automation (CI/CD pipelines, GitOps sync manifests)<br>• Release notes, changelog & rollback / contingency instructions | `ci-cd-and-automation`<br>`shipping-and-launch` | `docker-expert` (khi tối ưu hóa container, multi-stage build và Docker security)<br>`terraform-specialist` (khi triển khai hạ tầng dưới dạng mã IaC Terraform/OpenTofu)<br>`kubernetes-architect` (khi triển khai cụm K8s, GitOps ArgoCD/Flux và container orchestration) |
| **Operations & Incident Response** | • Observability configurations (dashboards, alert rules, SLOs)<br>• Operational runbooks & triage playbooks<br>• Incident records & postmortems (khi xảy ra sự cố) | `observability-and-instrumentation`<br>`systematic-debugging` | `service-mesh-observability` (khi quản trị distributed tracing và metrics qua Service Mesh Istio/Linkerd) |
| **Maintenance & Evolution** | • Technical debt & dependency upgrade backlog<br>• Điều tra và xử lý suy giảm hiệu năng (khi cần)<br>• Schema evolution scripts & deprecation notices | `code-simplification` | `improve-codebase-architecture` (khi quét tìm cơ hội tái cấu trúc kiến trúc mã nguồn)<br>`performance-optimization` (khi profiling và tối ưu hóa runtime/database bottleneck)<br>`deprecation-and-migration` (khi lập kế hoạch loại bỏ hệ thống cũ hoặc migration zero-downtime) |
| **Product Learning & Measurement** | • Product telemetry specification & event tracking taxonomy<br>• Báo cáo kết quả phễu chuyển đổi, cohort & thử nghiệm<br>• Tổng hợp phản hồi định tính & mức độ tiếp nhận tính năng | *(Không có kỹ năng Core bắt buộc; nạp theo nhu cầu sản phẩm)* | `analytics` (khi thiết kế taxonomy sự kiện và phân tích phễu hành vi)<br>`ab-testing` (khi thiết kế, chạy và đo lường thử nghiệm A/B) |
| **Security & Privacy (cross-cutting)** | • Threat models & abuse cases (STRIDE)<br>• Kết quả quét lỗ hổng & biên bản khắc phục<br>• Access control policies & cấu hình secrets<br>• Đánh giá tuân thủ quyền riêng tư dữ liệu (khi xử lý PII) | `security-and-hardening` | `threat-model-analyst` (khi phân tích mối đe dọa bảo mật theo khung STRIDE)<br>`secrets-management` (khi quản lý mật khẩu, khóa bí mật qua HashiCorp Vault/AWS Secrets Manager)<br>`auth-implementation-patterns` (khi thiết kế kiến trúc xác thực OAuth2, OIDC, JWT, RBAC/ABAC) |
| **Platform & Developer Experience (cross-cutting)** | • Cấu hình môi trường phát triển (devcontainers, pre-commit hooks)<br>• Golden-path templates & định nghĩa quy trình tái sử dụng<br>• Platform service & tool catalog (khi quản lý nền tảng dùng chung) | *(Không có kỹ năng Core bắt buộc; nạp theo hạ tầng DevEx)* | `setup-pre-commit` (khi tự động hóa kiểm tra mã nguồn trước khi commit qua pre-commit hooks)<br>`git-guardrails-claude-code` (khi thiết lập hàng rào an toàn cho tương tác Git tự động của agent) |
| **AI Governance & Agent Operations (cross-cutting)** | • Chính sách agent & cấu hình runtime (system prompt, tool permissions)<br>• Tập dữ liệu đánh giá & kết quả benchmark mô hình<br>• Model cards & nhật ký kiểm toán thực thi của agent | `using-sdlc-skills`<br>`context-engineering` | `skill-authoring` (khi phát triển hoặc kiểm toán kỹ năng agent mới trong pack)<br>`writing-for-agents` (khi soạn thảo prompt và tài liệu hướng dẫn tối ưu cho LLM)<br>`mcp-builder` (khi xây dựng server Model Context Protocol để mở rộng công cụ) |
| **Documentation & Knowledge (cross-cutting)** | • Hướng dẫn người dùng & tài liệu lập trình viên (onboarding, contributor guide)<br>• Hướng dẫn sử dụng API & tích hợp hệ thống<br>• Tài liệu tra cứu khắc phục sự cố vận hành | *(Không có kỹ năng Core bắt buộc; nạp theo loại tài liệu)* | `doc-coauthoring` (khi hỗ trợ đồng tác giả viết tài liệu kỹ thuật dài hơi)<br>`writing-guidelines` (khi biên tập tài liệu kỹ thuật ngắn gọn, súc tích theo quy chuẩn) |
| **Cost & Financial Governance (cross-cutting)** | • Báo cáo phân bổ chi phí hạ tầng và mô hình AI<br>• Ngân sách đám mây, cảnh báo chi tiêu & hạn mức tài nguyên | *(Không có kỹ năng Core bắt buộc; nạp theo nhu cầu FinOps)* | `cost-optimization` (khi tối ưu hóa hóa đơn đám mây đa nền tảng AWS, Azure, GCP, FinOps tagging) |

---

## 2. Nguyên tắc Sở hữu Tạo phẩm và Ánh xạ Template (Artifact & Template Contracts)

Mỗi tạo phẩm chuẩn hóa (canonical artifact) chỉ do một kỹ năng chịu trách nhiệm chính sở hữu, ngăn chặn mâu thuẫn giữa các luồng:

- **Opportunity Brief (`docs/discovery/[initiative]/opportunity-brief.md`)**: Do `interview-me` / `idea-refine` khởi tạo, `customer-research` cung cấp bằng chứng người dùng.
- **Product Requirements Document (`docs/prd.md`)**: Do `pm-product-spec` sở hữu.
- **Feature Specification (`docs/features/<feature-id>/spec.md`)**: Do `pm-user-story` sở hữu nội dung Story/AC BDD; `spec-driven-development` sở hữu cấu trúc tổng quan.
- **Formal System Requirements (`docs/srs.md`, `docs/rtm.md`)**: Do `requirements-engineering` sở hữu (chỉ tạo khi có yêu cầu tuân thủ chính thức).
- **Architecture Overview (`docs/architecture.md`)**: Do `software-architecture` sở hữu ranh giới thành phần và phân rã hệ thống.
- **Architecture Decisions (`docs/adr/ADR-NNN-*.md`)**: Do `documentation-and-adrs` sở hữu các quyết định kỹ thuật có đánh đổi.
- **Final Technical Task List (`docs/features/<feature-id>/tasks.md`)**: Do `planning-and-task-breakdown` là **chủ thể duy nhất** sở hữu danh sách task thực thi cuối cùng.
- **Task Session & Handoff (`.agent/tasks/<task-id>.md`)**: Do `task-handoff` sở hữu trạng thái phiên và nhật ký bàn giao.
- **Empirical Evidence & Acceptance (`docs/features/<feature-id>/acceptance-report.md`)**: Do `verification-before-completion` yêu cầu bằng chứng tươi thực tế trước khi hoàn tất.
- **Incident Postmortem (`docs/incidents/<id>/postmortem.md`)**: Do `observability-and-instrumentation` sở hữu điều tra nguyên nhân gốc rễ và hành động khắc phục.
- **Operational Runbook (`docs/runbooks/<service>.md`)**: Do `observability-and-instrumentation` / `service-mesh-observability` sở hữu quy trình xử lý sự cố và vận hành.
- **Threat Model (`docs/security/threat-model-<system>.md`)**: Do `threat-model-analyst` sở hữu phân tích STRIDE-A và ranh giới tin cậy.
- **Phân định Code Review vs. Spec Audit**: `code-review-and-quality` rà soát mã nguồn triển khai; `pm-spec-quality-audit` rà soát ngữ nghĩa tài liệu spec/PRD (hai năng lực bổ trợ, không thay thế nhau).

### Bảng Ánh xạ Khế ước Tạo phẩm Tinh gọn (31 Lean Canonical Artifacts)

| Stage | Expected Artifact | Starter Template | Native Format | Canonical Destination Path | Primary Owner Skill |
|---|---|---|---|---|---|
| **Discovery** | Opportunity brief & VoC evidence | `templates/specs/opportunity-brief.md` | `.md` | `docs/discovery/[initiative]/opportunity-brief.md` | `interview-me`, `idea-refine`, `customer-research` |
| **Requirements** | Product Requirements Document | `templates/specs/PRD.md` | `.md` | `docs/prd.md` | `pm-product-spec` |
| **Requirements** | Feature Specification (Stories & AC) | `templates/specs/feature-spec.md` | `.md` | `docs/features/<feature-id>/spec.md` | `spec-driven-development`, `pm-user-story` |
| **Requirements** | Formal System Requirements (SRS) | `templates/specs/SRS.md` | `.md` | `docs/specs/SRS.md` | `requirements-engineering` |
| **Requirements** | Requirements Traceability Matrix (RTM) | `templates/specs/RTM.md` | `.md` | `docs/specs/RTM.md` | `requirements-engineering` |
| **Architecture** | System Architecture Overview | `templates/specs/architecture-overview.md` | `.md` | `docs/architecture.md` | `software-architecture` |
| **Architecture** | Architecture Decision Record | `templates/specs/ADR.md` | `.md` | `docs/adr/ADR-NNN-[slug].md` | `documentation-and-adrs` |
| **Architecture** | Detailed Design Specification | `templates/specs/DDS.md` | `.md` | `docs/features/<feature-id>/design.md` | `software-architecture`, `codebase-design` |
| **Architecture** | REST API Executable Contract | `templates/contracts/openapi.yaml` | `.yaml` | `contracts/openapi.yaml` | `api-and-interface-design` |
| **Architecture** | Event-Driven Messaging Contract | `templates/contracts/asyncapi.yaml` | `.yaml` | `contracts/asyncapi.yaml` | `api-and-interface-design` |
| **Architecture** | Realtime & WebSocket Protocol Contract | `templates/contracts/stomp-websocket.yaml` | `.yaml` | `contracts/stomp-websocket.yaml` | `api-and-interface-design` |
| **Architecture** | Microservices RPC Interface Contract | `templates/contracts/service.proto` | `.proto` | `contracts/service.proto` | `api-and-interface-design` |
| **Architecture** | Query Interface Contract (GraphQL) | `templates/contracts/schema.graphql` | `.graphql` | `contracts/schema.graphql` | `api-and-interface-design` |
| **Architecture** | Domain Data Model Contract (JSON Schema) | `templates/contracts/data-contract.json` | `.json` | `contracts/data-contract.json` | `domain-modeling`, `database-design` |
| **Architecture** | Database Migration DDL | `templates/contracts/migration.sql` | `.sql` | `migrations/[timestamp]_[id].sql` | `database-design` |
| **Planning** | Technical Plan & Strategy | `templates/delivery/plan.md` | `.md` | `docs/features/<feature-id>/plan.md` | `spec-driven-development` |
| **Planning** | Authoritative Task Breakdown | `templates/delivery/tasks.md` | `.md` | `docs/features/<feature-id>/tasks.md` | `planning-and-task-breakdown` |
| **Planning** | Task Session & Role Handoff | `templates/delivery/task-handoff.md` | `.md` | `.agent/tasks/<task-id>.md` | `task-handoff` |
| **Verification** | Consolidated Acceptance & Verification | `templates/delivery/acceptance-report.md` | `.md` | `docs/features/<feature-id>/acceptance-report.md` | `verification-before-completion` |
| **Review** | Pull Request Description & Review | `templates/delivery/pull-request.md` | `.md` | `.github/pull_request_template.md` (hoặc PR body) | `code-review-and-quality` |
| **Release** | Release Notes & Changelog | `templates/delivery/release-notes.md` | `.md` | `docs/releases/v[X.Y.Z].md` | `shipping-and-launch` |
| **Release** | Release Readiness Gate | `templates/delivery/release-checklist.md` | `.md` | `docs/releases/release-checklist.md` | `shipping-and-launch` |
| **Operations** | Incident Postmortem | `templates/platform/incident-postmortem.md` | `.md` | `docs/incidents/[YYYYMMDD-slug]/postmortem.md` | `observability-and-instrumentation` |
| **Operations** | Operational Runbook | `templates/platform/runbook.md` | `.md` | `docs/runbooks/[service-name].md` | `observability-and-instrumentation` |
| **Operations** | Observability Alert Rules & SLOs | `templates/platform/alert-rules.yaml` | `.yaml` | `deploy/alerts/[service]-rules.yaml` | `observability-and-instrumentation`, `service-mesh-observability` |
| **Evolution** | Deprecation Notice & Migration | `templates/delivery/deprecation-notice.md` | `.md` | `docs/migrations/[slug]-deprecation.md` | `deprecation-and-migration` |
| **Learning** | Growth Experiment Brief | `templates/governance/experiment-brief.md` | `.md` | `docs/experiments/[exp-id]-[slug].md` | `ab-testing` |
| **Learning** | Event Tracking Plan & Schemas | `templates/governance/tracking-plan.md` | `.md` | `docs/analytics/tracking-plan.md` | `analytics` |
| **Learning** | Product Telemetry Event Schema | `templates/governance/event-schema.json` | `.json` | `analytics/schemas/[event].json` | `analytics` |
| **Security** | STRIDE-A Threat Model | `templates/governance/threat-model.md` | `.md` | `docs/security/threat-model-[system].md` | `threat-model-analyst` |
| **Governance** | Engineering Constitution & Rules | `templates/governance/constitution.md` | `.md` | `AGENTS.md` / `CLAUDE.md` / `.agent/constitution.md` | `writing-for-agents`, `context-engineering` |

---

## 3. Cơ chế Nạp Kỹ năng theo Nhu cầu & Chống Quá tải Ngữ cảnh (Demand-Driven Loading & Anti-Overload)

Quá trình thực thi tác vụ của agent tuân thủ vòng đời 5 bước theo thiết kế kiến trúc (xem sơ đồ và định nghĩa chuẩn tại [`docs/architecture.md` Section 4.3](architecture.md) và router [`skills/using-sdlc-skills/SKILL.md`](../skills/using-sdlc-skills/SKILL.md)), đảm bảo **nạp đúng theo bối cảnh (context-driven)** và **tuyệt đối không làm quá tải ngữ cảnh (anti-overload)**.

> **Nguyên tắc cốt lõi — Installation ≠ Selection ≠ Context Loading:** 29 Core skills **được cài đặt** (installed) để luôn có mặt trên disk, nhưng không có nghĩa là tất cả đều được nạp vào cửa sổ ngữ cảnh cùng lúc. Mỗi task chỉ nạp file SKILL.md của các skill thực sự cần dùng cho bước công việc đó. Xem định nghĩa chuẩn "Task Active Skills" tại `architecture.md`.

1. **Tiếp nhận tác vụ (Task Intake)**: Phân loại mục tiêu công việc theo 1 trong 16 Stages SDLC.
2. **Khám phá & Tuyển chọn (Discover & Select — The SDLC Triad)**:
   - **Chọn Workflow:** Xác định kịch bản điều phối phù hợp (`full-sdlc.md`, `feature-loop.md`, `bug-fix.md`, `quick-change.md`, `incident-response.md`, `experimentation-loop.md`, `deprecation-and-migration.md`, `agent-handoff-contract.md`).
   - **Chọn Kỹ năng:** Xác định *Tập nhỏ nhất đủ dùng (Smallest Sufficient Set)*: 29 Core skills **được cài đặt sẵn** (installed) không có nghĩa là tất cả đều được nạp vào ngữ cảnh cùng lúc — chỉ nạp các skill thực sự cần cho bước công việc hiện tại. Chỉ nạp thêm 1–2 Extras skills khi tech stack hoặc domain thực sự yêu cầu và skill đó cung cấp năng lực riêng biệt.
   - **Chọn Template:** Tra cứu bảng khế ước tạo phẩm để xác định file starter template tương ứng.
3. **Nạp Quy trình & Dựng khung Tạo phẩm (Load Workflow & Scaffold Template)**:
   - Nạp các bước của workflow đã chọn vào ngữ cảnh hoạt động.
   - Đọc template từ assets đi kèm router và khởi tạo (scaffold) ra file trên đĩa tại **Canonical Destination Path** của dự án (thay vì paste cả template dài vào cửa sổ chat).
4. **Thi công có kỷ luật (Execute Work with Selected Skills)**: Thực thi công việc theo trình tự của workflow và vận dụng kỹ năng chuyên sâu để điền nội dung thực tế (BDD stories, code TDD, architecture C4, threat mitigations). Nếu phát sinh rủi ro vượt ranh giới, mới nạp thêm kỹ năng chuyên môn tương ứng.
5. **Xác minh hợp đồng & Bàn giao (Verify Output Contract & Handoff)**: Kiểm định bằng chứng thực tế (`verification-before-completion`), bàn giao phiên gọn gàng vào `.agent/tasks/<task-id>.md` (chỉ truyền file paths, không paste lại nội dung tài liệu), và giải phóng ngữ cảnh tạm thời.

---

## 4. Ghi chú về Nguồn gốc và Quản trị

Pack kết hợp **63 kỹ năng tuyển chọn và chuẩn hóa** từ các nguồn uy tín:
- **Upstream đồng bộ có ghim SHA**: Addy Osmani (21 skills), Superpowers (5 skills), Anthropic Skills (4 skills), Matt Pocock (7 skills), Corey Haines (3 skills), Vercel Labs (3 skills), GitHub Awesome Copilot (1 skill).
- **Adapted phái sinh cục bộ có kiểm toán**: Uxcel Product Skills (3 skills), Agentic SDLC Kit (2 skills), wshobson/agents (5 skills), sickn33/agentic-awesome-skills (5 skills), api-contract-testing (1 skill).
- **Pack-owned cốt lõi**: `using-sdlc-skills`, `task-handoff`, `skill-authoring`.

Chi tiết giấy phép, commit lock và hàm băm bảo toàn nội dung xem tại `manifests/skill-provenance.json` và `THIRD_PARTY_NOTICES.md`.
