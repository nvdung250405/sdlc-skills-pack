# Starter Artifact Templates Catalog

Thư mục `templates/` chứa **31 khuôn mẫu khởi tạo chuẩn hóa tinh gọn (Lean Canonical Artifact Templates & Blueprints)** được tuyển chọn kỹ lưỡng, tương ứng trực tiếp với các tạo phẩm thực tế trong 16 giai đoạn của vòng đời phát triển phần mềm ([docs/sdlc-practical-matrix.md](../docs/sdlc-practical-matrix.md)).

Bộ template được thiết kế theo nguyên lý **Lean & Contract-First**:
- **Không nhồi nhét cấu hình phụ thuộc stack:** Các file như `devcontainer.json`, `ci.yaml`, `.env.example` được để cho các kỹ năng chuyên môn (`docker-expert`, `ci-cd-and-automation`, `incremental-implementation`) tự động sinh trực tiếp theo tech stack thực tế của dự án.
- **Tích hợp kiểm định toàn diện:** Báo cáo nghiệm thu [`delivery/acceptance-report.md`](delivery/acceptance-report.md) hợp nhất toàn bộ bằng chứng kiểm thử (Unit/Integration, Contract Lint, Security Scan và Performance SLA) vào một nơi duy nhất.
- **Tập trung vào Khế ước thực thi:** Cung cấp đầy đủ 7 khế ước máy đọc được (`openapi.yaml`, `asyncapi.yaml`, `stomp-websocket.yaml`, `service.proto`, `schema.graphql`, `data-contract.json`, `migration.sql`) để chấm dứt tình trạng Agent tạo văn xuôi `api.md`.

---

## 1. Nhóm Khế ước Kỹ thuật Thực thi (`contracts/` — 7 items)

Hợp đồng giao tiếp dịch vụ và dữ liệu ở định dạng chuẩn hóa, máy đọc và kiểm thử tự động được.

| Starter Template | Định dạng | Mục đích sử dụng | Primary Owner Skill |
|---|---|---|---|
| [`contracts/openapi.yaml`](contracts/openapi.yaml) | `.yaml` | REST API contract chuẩn OpenAPI 3.1 (paths, schemas, error envelope, bearer auth) | `api-and-interface-design` |
| [`contracts/asyncapi.yaml`](contracts/asyncapi.yaml) | `.yaml` | Event-driven messaging contract (AsyncAPI 3.0 / CloudEvents) cho Kafka/RabbitMQ | `api-and-interface-design` |
| [`contracts/stomp-websocket.yaml`](contracts/stomp-websocket.yaml) | `.yaml` | STOMP 1.2 protocol & WebSocket message frames cho giao tiếp thời gian thực | `api-and-interface-design` |
| [`contracts/service.proto`](contracts/service.proto) | `.proto` | Protocol Buffers v3 RPC interface contract cho gRPC / microservices nội bộ | `api-and-interface-design` |
| [`contracts/schema.graphql`](contracts/schema.graphql) | `.graphql` | GraphQL SDL schema contract (Queries, Mutations, Subscriptions, Errors) | `api-and-interface-design` |
| [`contracts/data-contract.json`](contracts/data-contract.json) | `.json` | JSON Schema Draft 2020-12 data contract cho domain entity models | `domain-modeling`, `database-design` |
| [`contracts/migration.sql`](contracts/migration.sql) | `.sql` | Reversible, transactional SQL schema migration DDL (Up/Down) | `database-design` |

---

## 2. Nhóm Đặc tả Nghiệp vụ & Thiết kế Kiến trúc (`specs/` — 8 items)

Tài liệu đặc tả yêu cầu, câu chuyện người dùng, thiết kế kiến trúc và quyết định kỹ thuật.

| Starter Template | Định dạng | Mục đích sử dụng | Primary Owner Skill |
|---|---|---|---|
| [`specs/opportunity-brief.md`](specs/opportunity-brief.md) | `.md` | Khảo sát cơ hội, định hình vấn đề, bằng chứng người dùng (VoC) & giả thuyết | `interview-me`, `idea-refine`, `customer-research` |
| [`specs/PRD.md`](specs/PRD.md) | `.md` | Product Requirements Document (mục tiêu, outcomes, epics, non-goals) | `pm-product-spec` |
| [`specs/feature-spec.md`](specs/feature-spec.md) | `.md` | Đặc tả tính năng chuẩn hóa (User Stories, BDD Given/When/Then AC) | `spec-driven-development`, `pm-user-story` |
| [`specs/SRS.md`](specs/SRS.md) | `.md` | Formal System Requirements Specification cho dự án phức tạp/tuân thủ | `requirements-engineering` |
| [`specs/RTM.md`](specs/RTM.md) | `.md` | Requirements Traceability Matrix liên kết requirements với code/test | `requirements-engineering` |
| [`specs/architecture-overview.md`](specs/architecture-overview.md) | `.md` | Tổng quan kiến trúc hệ thống, ranh giới thành phần và mô hình C4 | `software-architecture` |
| [`specs/ADR.md`](specs/ADR.md) | `.md` | Architecture Decision Record ghi nhận quyết định kỹ thuật, đánh đổi & chi phí | `documentation-and-adrs` |
| [`specs/DDS.md`](specs/DDS.md) | `.md` | Detailed Design Specification cho các subsystem hoặc thuật toán sâu | `software-architecture`, `codebase-design` |

---

## 3. Nhóm Kế hoạch, Thi công & Bàn giao (`delivery/` — 8 items)

Kế hoạch chia nhỏ công việc, quản lý phiên làm việc, nghiệm thu toàn diện và phát hành phiên bản.

| Starter Template | Định dạng | Mục đích sử dụng | Primary Owner Skill |
|---|---|---|---|
| [`delivery/plan.md`](delivery/plan.md) | `.md` | Kế hoạch triển khai kỹ thuật và chiến lược kiểm thử | `spec-driven-development`, `planning-and-task-breakdown` |
| [`delivery/tasks.md`](delivery/tasks.md) | `.md` | Danh sách task nguyên tử cuối cùng kèm dependency edges và verification | `planning-and-task-breakdown` |
| [`delivery/task-handoff.md`](delivery/task-handoff.md) | `.md` | Nhật ký phiên làm việc, trạng thái hiện tại và bàn giao giữa các agent | `task-handoff` |
| [`delivery/acceptance-report.md`](delivery/acceptance-report.md) | `.md` | Báo cáo nghiệm thu hợp nhất: Test, Lint, Security Scan & Performance SLA | `verification-before-completion` |
| [`delivery/pull-request.md`](delivery/pull-request.md) | `.md` | Biểu mẫu Pull Request, động lực thay đổi và checklist người review | `code-review-and-quality` |
| [`delivery/release-notes.md`](delivery/release-notes.md) | `.md` | Changelog và ghi chú phát hành theo phiên bản SemVer | `shipping-and-launch` |
| [`delivery/release-checklist.md`](delivery/release-checklist.md) | `.md` | Cổng kiểm soát sẵn sàng phát hành, rà soát an toàn và kế hoạch rollback | `shipping-and-launch` |
| [`delivery/deprecation-notice.md`](delivery/deprecation-notice.md) | `.md` | Thông báo sunset tính năng cũ và lộ trình chuyển đổi Expand/Contract | `deprecation-and-migration` |

---

## 4. Nhóm Vận hành & Cảnh báo Sự cố (`platform/` — 3 items)

Sổ tay vận hành, cảnh báo Prometheus và phân tích sự cố production.

| Starter Template | Định dạng | Mục đích sử dụng | Primary Owner Skill |
|---|---|---|---|
| [`platform/runbook.md`](platform/runbook.md) | `.md` | Sổ tay vận hành, chẩn đoán và khắc phục sự cố dịch vụ | `observability-and-instrumentation` |
| [`platform/incident-postmortem.md`](platform/incident-postmortem.md) | `.md` | Biên bản phân tích nguyên nhân gốc rễ (RCA 5 Whys) sau sự cố | `observability-and-instrumentation` |
| [`platform/alert-rules.yaml`](platform/alert-rules.yaml) | `.yaml` | Prometheus Alerting Rules và định nghĩa ngưỡng SLO/latency/error | `observability-and-instrumentation`, `service-mesh-observability` |

---

## 5. Nhóm Quản trị, Bảo mật & Đo lường (`governance/` — 5 items)

Hiến pháp kỹ thuật, mô hình đe dọa an ninh, đo lường dữ liệu và thử nghiệm A/B.

| Starter Template | Định dạng | Mục đích sử dụng | Primary Owner Skill |
|---|---|---|---|
| [`governance/constitution.md`](governance/constitution.md) | `.md` | Hiến pháp kỹ thuật dự án, quy tắc bất biến cho agent và Definition of Done | `writing-for-agents`, `context-engineering` |
| [`governance/threat-model.md`](governance/threat-model.md) | `.md` | Phân tích mô hình đe dọa STRIDE-A, biểu đồ luồng dữ liệu và ranh giới tin cậy | `threat-model-analyst` |
| [`governance/tracking-plan.md`](governance/tracking-plan.md) | `.md` | Kế hoạch telemetry, taxonomy sự kiện và các chiều phân tích dữ liệu | `analytics` |
| [`governance/event-schema.json`](governance/event-schema.json) | `.json` | JSON Schema xác thực payload sự kiện telemetry trước khi nạp vào kho | `analytics` |
| [`governance/experiment-brief.md`](governance/experiment-brief.md) | `.md` | Tài liệu thiết kế thử nghiệm A/B, giả thuyết kiểm định và kết quả thống kê | `ab-testing` |

---

## 6. Lệnh Khởi tạo Nhanh (Scaffolding Commands)

Sử dụng script tiện ích để scaffold bất kỳ template nào ra đúng đường dẫn chuẩn của dự án:
```bash
# Scaffold REST API contract
python scripts/scaffold.py openapi --target contracts/api.yaml

# Scaffold Event-driven messaging contract
python scripts/scaffold.py asyncapi --target contracts/events.yaml

# Scaffold Feature Specification
python scripts/scaffold.py spec --id my-feature --title "User Authentication"

# Scaffold Database Migration
python scripts/scaffold.py migration --id create_users_table

# Scaffold Acceptance Verification Report
python scripts/scaffold.py acceptance --id my-feature
```
