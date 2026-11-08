# SDLC Stage → Output → Selected Skills

Bản đồ định tuyến kỹ năng thực tế theo **16 giai đoạn chuẩn hóa quốc tế** (ISO/IEC/IEEE 12207, SWEBOK v4, NIST SSDF, DORA, FinOps). Router duy nhất của pack là `using-sdlc-skills` lựa chọn luồng làm việc tinh gọn nhất (right-sized) và áp dụng cơ chế **Nạp kỹ năng theo nhu cầu (Demand-Driven Skill Loading)**.

Pack quy chuẩn thành:
- **33 Universal SDLC skills**: Kỷ luật công kỹ nghệ nền tảng, độc lập công cụ, cài đặt mặc định cho mọi agent trong mọi dự án.

---

## 1. Bảng điều hướng 16 Giai đoạn SDLC

| Stage (Giai đoạn) | Expected outputs (Tạo phẩm tinh gọn) | Universal skills (Mặc định cài đặt) | Triggers / Ghi chú |
|---|---|---|---|
| **Discovery** | • Opportunity brief (problem framing, target users, validation findings)<br>• Customer & market research synthesis<br>• Hypothesis validation records (khi theo dõi qua các vòng lặp) | `interview-me`<br>`idea-refine`<br>`analytics` | Khảo sát vấn đề kinh doanh, phỏng vấn nhu cầu và dữ liệu hành vi người dùng |
| **Requirements** | • Product Requirements Document (PRD)<br>• Feature specifications (User Stories & Acceptance Criteria)<br>• Requirements traceability & compliance records (theo ngữ cảnh dự án) | `spec-driven-development`<br>`pm-user-story` | Soạn thảo PRD/spec, User Stories BDD và ma trận truy vết yêu cầu |
| **Architecture & System Design** | • System architecture overview (components, boundaries, C4 models)<br>• Architecture Decision Records (ADRs)<br>• Interface & data contracts (OpenAPI, schemas, data models)<br>• UI component specifications & design system tokens | `software-architecture`<br>`api-and-interface-design`<br>`database-design`<br>`documentation-and-adrs` | Thiết kế ranh giới hệ thống, hợp đồng API, mô hình dữ liệu và ghi nhận ADR |
| **Planning & Task Breakdown** | • Technical implementation plan & task breakdown (kèm DoD và ràng buộc kỹ thuật)<br>• Task handoff & context notes (khi cần bàn giao phiên) | `planning-and-task-breakdown`<br>`task-handoff` | Bẻ khóa công việc thành các task nguyên tử độc lập và quản lý phiên làm việc |
| **Implementation & Construction** | • Mã nguồn ứng dụng & lịch sử commit nguyên tử có kiểm soát<br>• Automated unit & component test suites<br>• Database migrations & integration adapters<br>• Feature flags & cấu hình môi trường | `incremental-implementation`<br>`test-driven-development`<br>`source-driven-development`<br>`git-workflow-and-versioning`<br>`frontend-ui-engineering` | Xây dựng theo lát cắt dọc mỏng, Red-Green-Refactor, tuân thủ tài liệu chuẩn và kỷ luật Git |
| **Testing & Verification** | • Automated test suites (integration, E2E, contract)<br>• Kết quả thực thi test & chẩn đoán lỗi (trong CI hoặc test runner)<br>• Kết quả benchmark hiệu năng, tải và accessibility (khi đánh giá) | `verification-before-completion`<br>`webapp-testing`<br>`api-contract-testing`<br>`k6-load-testing` | Kiểm thử Playwright E2E, kiểm thử hợp đồng API, đo tải k6 và đối soát bằng chứng trước khi kết thúc |
| **Review & Acceptance** | • Pull request review comments & merge approvals<br>• Acceptance verification (khi độc lập cổng nghiệm thu)<br>• Design & guideline conformance reviews | `code-review-and-quality` | Rà soát đa chiều logic, bảo mật, chất lượng mã nguồn và tiêu chí nghiệm thu |
| **Release & Deployment** | • Versioned build artifacts và images (có ký số khi bắt buộc)<br>• Deployment automation (CI/CD pipelines, GitOps sync manifests)<br>• Release notes, changelog & rollback / contingency instructions | `ci-cd-and-automation`<br>`shipping-and-launch`<br>`docker-expert` | Tự động hóa pipeline CI/CD, đóng gói container Docker tối ưu và checklist phát hành an toàn |
| **Operations & Incident Response** | • Observability configurations (dashboards, alert rules, SLOs)<br>• Operational runbooks & triage playbooks<br>• Incident records & postmortems (khi xảy ra sự cố) | `observability-and-instrumentation`<br>`systematic-debugging` | Thiết lập alert/SLO Prometheus, quy trình runbook và chẩn đoán gốc rễ sự cố |
| **Maintenance & Evolution** | • Technical debt & dependency upgrade backlog<br>• Điều tra và xử lý suy giảm hiệu năng (khi cần)<br>• Schema evolution scripts & deprecation notices | `code-simplification`<br>`performance-optimization`<br>`deprecation-and-migration` | Tinh giản mã phức tạp, xử lý bottleneck hiệu năng và di chuyển dữ liệu zero-downtime |
| **Product Learning & Measurement** | • Product telemetry specification & event tracking taxonomy<br>• Báo cáo kết quả phễu chuyển đổi, cohort & thử nghiệm<br>• Tổng hợp phản hồi định tính & mức độ tiếp nhận tính năng | `analytics` | Thiết kế taxonomy sự kiện telemetry, theo dõi phễu chuyển đổi và phân tích thử nghiệm |
| **Security & Privacy (cross-cutting)** | • Threat models & abuse cases (STRIDE)<br>• Kết quả quét lỗ hổng & biên bản khắc phục<br>• Access control policies & cấu hình secrets<br>• Đánh giá tuân thủ quyền riêng tư dữ liệu (khi xử lý PII) | `security-and-hardening`<br>`auth-implementation-patterns` | Đánh giá an ninh STRIDE, kiểm toán lỗ hổng, quản lý xác thực và phân quyền RBAC/ABAC |
| **Platform & Developer Experience (cross-cutting)** | • Cấu hình môi trường phát triển (devcontainers, pre-commit hooks)<br>• Golden-path templates & định nghĩa quy trình tái sử dụng<br>• Platform service & tool catalog (khi quản lý nền tảng dùng chung) | `ci-cd-and-automation`<br>`docker-expert` | Thiết lập môi trường tự động hóa, container chuẩn hóa và quy trình dev lặp lại |
| **AI Governance & Agent Operations (cross-cutting)** | • Chính sách agent & cấu hình runtime (system prompt, tool permissions)<br>• Tập dữ liệu đánh giá & kết quả benchmark mô hình<br>• Model cards & nhật ký kiểm toán thực thi của agent | `using-sdlc-skills`<br>`task-handoff` | Điều hướng quy trình SDLC thống nhất, điều phối subagents và quản lý ngữ cảnh |
| **Documentation & Knowledge (cross-cutting)** | • Hướng dẫn người dùng & tài liệu lập trình viên (onboarding, contributor guide)<br>• Hướng dẫn sử dụng API & tích hợp hệ thống<br>• Tài liệu tra cứu khắc phục sự cố vận hành | `documentation-and-adrs`<br>`source-driven-development` | Tài liệu hóa kiến trúc, quyết định kỹ thuật và hướng dẫn tích hợp |
| **Cost & Financial Governance (cross-cutting)** | • Báo cáo phân bổ chi phí hạ tầng và mô hình AI<br>• Ngân sách đám mây, cảnh báo chi tiêu & hạn mức tài nguyên | `software-architecture`<br>`performance-optimization` | Đánh giá sizing hạ tầng, tối ưu hóa tài nguyên và chi phí vận hành |

---

## 2. Nguyên tắc Sở hữu Tạo phẩm và Ánh xạ Template (Artifact & Template Contracts)

Mỗi tạo phẩm chuẩn hóa (canonical artifact) chỉ do một kỹ năng chịu trách nhiệm chính sở hữu, ngăn chặn mâu thuẫn giữa các luồng:

- **Opportunity Brief (`docs/discovery/[initiative]/opportunity-brief.md`)**: Do `interview-me` / `idea-refine` khởi tạo, `analytics` cung cấp dữ liệu định lượng.
- **Product Requirements Document (`docs/prd.md`)**: Do `spec-driven-development` sở hữu.
- **Feature Specification (`docs/features/<feature-id>/spec.md`)**: Do `pm-user-story` sở hữu nội dung Story/AC BDD; `spec-driven-development` sở hữu cấu trúc tổng quan.
- **Formal System Requirements (`docs/specs/SRS.md`, `docs/specs/RTM.md`)**: Do `spec-driven-development` sở hữu (khi có yêu cầu tuân thủ chính thức).
- **Architecture Overview (`docs/architecture.md`)**: Do `software-architecture` sở hữu ranh giới thành phần và phân rã hệ thống.
- **Architecture Decisions (`docs/adr/ADR-NNN-*.md`)**: Do `documentation-and-adrs` sở hữu các quyết định kỹ thuật có đánh đổi.
- **Final Technical Task List (`docs/features/<feature-id>/tasks.md`)**: Do `planning-and-task-breakdown` là **chủ thể duy nhất** sở hữu danh sách task thực thi cuối cùng.
- **Task Session & Handoff (`.agent/tasks/<task-id>.md`)**: Do `task-handoff` sở hữu trạng thái phiên và nhật ký bàn giao.
- **Empirical Evidence & Acceptance (`docs/features/<feature-id>/acceptance-report.md`)**: Do `verification-before-completion` yêu cầu bằng chứng tươi thực tế trước khi hoàn tất.
- **Incident Postmortem (`docs/incidents/[YYYYMMDD-slug]/postmortem.md`)**: Do `observability-and-instrumentation` sở hữu điều tra nguyên nhân gốc rễ và hành động khắc phục.
- **Operational Runbook (`docs/runbooks/[service-name].md`)**: Do `observability-and-instrumentation` sở hữu quy trình xử lý sự cố và vận hành.
- **Threat Model (`docs/security/threat-model-[system].md`)**: Do `security-and-hardening` sở hữu phân tích STRIDE-A và ranh giới tin cậy.
- **Phân định Code Review vs. Spec Audit**: `code-review-and-quality` rà soát mã nguồn triển khai; `spec-driven-development` rà soát ngữ nghĩa tài liệu spec/PRD (hai năng lực bổ trợ, không thay thế nhau).

### Bảng Ánh xạ Khế ước Tạo phẩm Tinh gọn (32 Lean Canonical Artifacts)

| Stage | Expected Artifact | Starter Template | Native Format | Canonical Destination Path | Primary Owner Skill |
|---|---|---|---|---|---|
| **Discovery** | Opportunity brief & VoC evidence | `templates/specs/opportunity-brief.md` | `.md` | `docs/discovery/[initiative]/opportunity-brief.md` | `interview-me`, `idea-refine` |
| **Requirements** | Product Requirements Document | `templates/specs/PRD.md` | `.md` | `docs/prd.md` | `spec-driven-development` |
| **Requirements** | Feature Specification (Stories & AC) | `templates/specs/feature-spec.md` | `.md` | `docs/features/<feature-id>/spec.md` | `spec-driven-development`, `pm-user-story` |
| **Requirements** | Formal System Requirements (SRS) | `templates/specs/SRS.md` | `.md` | `docs/specs/SRS.md` | `spec-driven-development` |
| **Requirements** | Requirements Traceability Matrix (RTM) | `templates/specs/RTM.md` | `.md` | `docs/specs/RTM.md` | `spec-driven-development` |
| **Architecture** | System Architecture Overview | `templates/specs/architecture-overview.md` | `.md` | `docs/architecture.md` | `software-architecture` |
| **Architecture** | Architecture Decision Record | `templates/specs/ADR.md` | `.md` | `docs/adr/ADR-NNN-[slug].md` | `documentation-and-adrs` |
| **Architecture** | Detailed Design Specification | `templates/specs/DDS.md` | `.md` | `docs/features/<feature-id>/design.md` | `software-architecture` |
| **Architecture** | REST API Executable Contract | `templates/contracts/openapi.yaml` | `.yaml` | `contracts/openapi.yaml` | `api-and-interface-design` |
| **Architecture** | Event-Driven Messaging Contract | `templates/contracts/asyncapi.yaml` | `.yaml` | `contracts/asyncapi.yaml` | `api-and-interface-design` |
| **Architecture** | Realtime & WebSocket Protocol Contract | `templates/contracts/stomp-websocket.yaml` | `.yaml` | `contracts/stomp-websocket.yaml` | `api-and-interface-design` |
| **Architecture** | Microservices RPC Interface Contract | `templates/contracts/service.proto` | `.proto` | `contracts/service.proto` | `api-and-interface-design` |
| **Architecture** | Query Interface Contract (GraphQL) | `templates/contracts/schema.graphql` | `.graphql` | `contracts/schema.graphql` | `api-and-interface-design` |
| **Architecture** | Domain Data Model Contract (JSON Schema) | `templates/contracts/data-contract.json` | `.json` | `contracts/data-contract.json` | `database-design` |
| **Architecture** | Database Migration DDL | `templates/contracts/migration.sql` | `.sql` | `migrations/[timestamp]_[id].sql` | `database-design` |
| **Planning** | Technical Plan & Strategy | `templates/delivery/plan.md` | `.md` | `docs/features/<feature-id>/plan.md` | `spec-driven-development` |
| **Planning** | Authoritative Task Breakdown | `templates/delivery/tasks.md` | `.md` | `docs/features/<feature-id>/tasks.md` | `planning-and-task-breakdown` |
| **Planning** | Task Session & Role Handoff | `templates/delivery/task-handoff.md` | `.md` | `.agent/tasks/<task-id>.md` | `task-handoff` |
| **Delivery** | Task Completion Report | `templates/delivery/completion-report.md` | `.md` | `docs/features/<feature-id>/completion-report.md` | `verification-before-completion`, `task-handoff` |
| **Verification** | Consolidated Acceptance & Verification | `templates/delivery/acceptance-report.md` | `.md` | `docs/features/<feature-id>/acceptance-report.md` | `verification-before-completion` |
| **Review** | Pull Request Description & Review | `templates/delivery/pull-request.md` | `.md` | `.github/pull_request_template.md` (hoặc PR body) | `code-review-and-quality` |
| **Release** | Release Notes & Changelog | `templates/delivery/release-notes.md` | `.md` | `docs/releases/v[X.Y.Z].md` | `shipping-and-launch` |
| **Release** | Release Readiness Gate | `templates/delivery/release-checklist.md` | `.md` | `docs/releases/release-checklist.md` | `shipping-and-launch` |
| **Operations** | Incident Postmortem | `templates/platform/incident-postmortem.md` | `.md` | `docs/incidents/[YYYYMMDD-slug]/postmortem.md` | `observability-and-instrumentation` |
| **Operations** | Operational Runbook | `templates/platform/runbook.md` | `.md` | `docs/runbooks/[service-name].md` | `observability-and-instrumentation` |
| **Operations** | Observability Alert Rules & SLOs | `templates/platform/alert-rules.yaml` | `.yaml` | `deploy/alerts/[service]-rules.yaml` | `observability-and-instrumentation` |
| **Evolution** | Deprecation Notice & Migration | `templates/delivery/deprecation-notice.md` | `.md` | `docs/migrations/[slug]-deprecation.md` | `deprecation-and-migration` |
| **Learning** | Growth Experiment Brief | `templates/governance/experiment-brief.md` | `.md` | `docs/experiments/[exp-id]-[slug].md` | `analytics` |
| **Learning** | Event Tracking Plan & Schemas | `templates/governance/tracking-plan.md` | `.md` | `docs/analytics/tracking-plan.md` | `analytics` |
| **Learning** | Product Telemetry Event Schema | `templates/governance/event-schema.json` | `.json` | `analytics/schemas/[event].json` | `analytics` |
| **Security** | STRIDE-A Threat Model | `templates/governance/threat-model.md` | `.md` | `docs/security/threat-model-[system].md` | `security-and-hardening` |
| **Governance** | Engineering Constitution & Rules | `templates/governance/constitution.md` | `.md` | `AGENTS.md` / `CLAUDE.md` / `.agent/constitution.md` | `using-sdlc-skills` |

---

## 3. Cơ chế Nạp Kỹ năng theo Nhu cầu & Chống Quá tải Ngữ cảnh (Demand-Driven Loading & Anti-Overload)

Quá trình thực thi tác vụ của agent tuân thủ vòng đời 5 bước theo thiết kế kiến trúc (xem sơ đồ và định nghĩa chuẩn tại [`docs/architecture.md` Section 4.3](architecture.md) và router [`skills/using-sdlc-skills/SKILL.md`](../skills/using-sdlc-skills/SKILL.md)), đảm bảo **nạp đúng theo bối cảnh (context-driven)** và **tuyệt đối không làm quá tải ngữ cảnh (anti-overload)**.

> **Nguyên tắc cốt lõi — Installation ≠ Selection ≠ Context Loading:** 33 Universal skills **được cài đặt** (installed) để luôn có mặt trên disk, nhưng không có nghĩa là tất cả đều được nạp vào cửa sổ ngữ cảnh cùng lúc. Mỗi task chỉ nạp file SKILL.md của các skill thực sự cần dùng cho bước công việc đó. Xem định nghĩa chuẩn "Task Active Skills" tại `architecture.md`.

1. **Tiếp nhận tác vụ (Task Intake)**: Phân loại mục tiêu công việc theo 1 trong 16 Stages SDLC.
2. **Khám phá & Tuyển chọn (Discover & Select — The SDLC Triad)**:
   - **Chọn Workflow:** Xác định kịch bản điều phối phù hợp (`full-sdlc.md`, `feature-loop.md`, `bug-fix.md`, `quick-change.md`, `incident-response.md`, `experimentation-loop.md`, `deprecation-and-migration.md`, `agent-handoff-contract.md`).
   - **Chọn Kỹ năng:** Xác định *Tập nhỏ nhất đủ dùng (Smallest Sufficient Set)*: 33 Universal skills **được cài đặt sẵn** (installed) không có nghĩa là tất cả đều được nạp vào ngữ cảnh cùng lúc — chỉ nạp các skill thực sự cần cho bước công việc hiện tại (thường là 1–2 skills).
   - **Chọn Template:** Tra cứu bảng khế ước tạo phẩm để xác định file starter template tương ứng.
3. **Nạp Quy trình & Dựng khung Tạo phẩm (Load Workflow & Scaffold Template)**:
   - Nạp các bước của workflow đã chọn vào ngữ cảnh hoạt động.
   - Đọc template từ assets đi kèm router và khởi tạo (scaffold) ra file trên đĩa tại **Canonical Destination Path** của dự án (thay vì paste cả template dài vào cửa sổ chat).
4. **Thi công có kỷ luật (Execute Work with Selected Skills)**: Thực thi công việc theo trình tự của workflow và vận dụng kỹ năng chuyên sâu để điền nội dung thực tế (BDD stories, code TDD, architecture C4, threat mitigations).
5. **Xác minh hợp đồng & Bàn giao (Verify Output Contract & Handoff)**: Kiểm định bằng chứng thực tế (`verification-before-completion`), bàn giao phiên gọn gàng vào `.agent/tasks/<task-id>.md` (chỉ truyền file paths, không paste lại nội dung tài liệu), và giải phóng ngữ cảnh tạm thời.

---

## 4. Ghi chú về Nguồn gốc và Quản trị

Pack kết hợp **33 Universal SDLC skills tuyển chọn và chuẩn hóa** từ các nguồn uy tín:
- **Upstream đồng bộ có ghim SHA**: Addy Osmani (19 skills), Superpowers (2 skills), Anthropic Skills (1 skill), Corey Haines (1 skill).
- **Adapted phái sinh cục bộ có kiểm toán**: Uxcel Product Skills (1 skill), Agentic SDLC Kit (1 skill), wshobson/agents (1 skill), sickn33/agentic-awesome-skills (3 skills), api-contract-testing (1 skill).
- **Pack-owned cốt lõi**: `using-sdlc-skills`, `task-handoff`, `api-contract-testing`.

Chi tiết giấy phép, commit lock và hàm băm bảo toàn nội dung xem tại `manifests/skill-provenance.json` và `THIRD_PARTY_NOTICES.md`.
