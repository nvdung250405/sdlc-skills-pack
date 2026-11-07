# SDLC Skills Pack

Bộ skill phát triển phần mềm có thể cài trên nhiều coding agent, tuyển chọn từ các upstream đã pin phiên bản và kết hợp bằng một router duy nhất cùng bộ artifact contract thống nhất. Mục tiêu là tái sử dụng skill tốt, tránh trùng chức năng, quy chuẩn **32 Universal SDLC skills**, áp dụng cơ chế **Nạp kỹ năng theo nhu cầu (Demand-Driven Skill Loading)**.

## Cách tổ chức

```text
skills/                    # 32 Universal SDLC skills (kỷ luật công nghệ nền tảng, stack-agnostic)
workflows/                 # 11 quy trình: full SDLC, feature loop, bug fix, quick change, incident, refactoring, performance, upgrade, handoff...
templates/                 # 32 canonical artifact templates across 5 functional groups (contracts, specs, delivery, platform, governance)
docs/sdlc-practical-matrix.md # Master Matrix 16 stages và 32 Universal SDLC skills chuẩn hóa
docs/stage-skill-map.md    # Stage → Output → Core & Extras routing map
docs/architecture.md       # Thiết kế kiến trúc, demand-driven loading & quality gates
adapters/agents.json       # Đường dẫn cài đặt theo agent; có thể override
manifests/skill-map.json   # Nhóm skill, ownership và quy tắc precedence
manifests/upstream-lock.json # Các upstream sync-managed được pin commit
manifests/skill-provenance.json # Nguồn, license, transformations và hash nội dung
upstream.json              # Upstream được chọn, derived skills và nguồn tham khảo
scripts/sync_upstream.py   # Sync transaction, validate, provenance và notices
scripts/lint_pack.py       # Lint cục bộ; --strict là cổng phát hành
scripts/install.py         # Installer có preflight, backup và dry-run
scripts/build_agents_md.py # Tạo mục lục portable cho agent cần AGENTS.md
scripts/scaffold.py        # Khởi tạo nhanh canonical artifacts từ templates chuẩn
```

## Các nguồn và trạng thái provenance

| Nguồn | Vai trò | Cách quản lý |
|---|---|---|
| [Addy Osmani Agent Skills](https://github.com/addyosmani/agent-skills) | Engineering, testing, review, security, release, observability | 19 skill đã chọn trong `skills/`, commit `aeac41d4d005999432bb7312f7ff06383a91d59d` |
| [Superpowers](https://github.com/obra/superpowers) | Debugging có hệ thống, verification-before-completion | 2 skill đã chọn trong `skills/` (`systematic-debugging`, `verification-before-completion`), commit `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b` |
| [Anthropic Skills](https://github.com/anthropics/skills) | Browser/web app testing với Playwright | 1 skill trong `skills/` (`webapp-testing`), commit `dbd4588f9e1033efb41dad4bef2f7947c8993d44` |
| [Corey Haines Marketing Skills](https://github.com/coreyhaines31/marketingskills) | Product telemetry, analytics tracking taxonomy | 1 skill trong `skills/` (`analytics`), commit `0cd9b3a0ef4c411a1d690419ce843f2a1da32cce` |
| [Uxcel Product Skills](https://github.com/Uxcel-Lab/product-skills) | User Story và BDD Acceptance Criteria | 1 skill adapt cục bộ trong `skills/` (`pm-user-story`); refresh thủ công có bảo toàn content hash |
| [Agentic SDLC Kit](https://github.com/zeeshanhanif/agentic-sdlc-kit) | Kiến trúc hệ thống và phân rã ranh giới | 1 skill adapt cục bộ trong `skills/` (`software-architecture`); refresh thủ công có bảo toàn content hash |
| [William Hobson Agents](https://github.com/wshobson/agents) | Auth patterns, tokens và session lifecycle | 1 skill adapt trong `skills/` (`auth-implementation-patterns`); license MIT |
| [Agentic Awesome Skills (sickn33)](https://github.com/sickn33/agentic-awesome-skills) | Database design, Docker, k6 load testing | 3 skill adapt trong `skills/` (`database-design`, `docker-expert`, `k6-load-testing`); license Code MIT, docs CC BY 4.0 |
| [API Contract Testing](https://github.com/nvdung250405/sdlc-skills-pack) | Wire-level provider/consumer contract testing & fixtures | 1 skill pack-owned trong `skills/` (`api-contract-testing`); license MIT |
| SDLC Router & Task Handoff | Điều hướng SDLC duy nhất và quản trị phiên bàn giao | 2 skill pack-owned trong `skills/` (`using-sdlc-skills`, `task-handoff`); license MIT |
| [GitHub Spec Kit](https://github.com/github/spec-kit) | Tham khảo format Story/AC, independent test, plan/tasks | Nguồn tham khảo, không bundle command/skill nguyên bản |
| [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) | Tham khảo cách tổ chức vai trò và workflow | Nguồn tham khảo; không bundle implementation của BMAD |

**Quy mô hiện tại:** Quy chuẩn đúng **32 Universal SDLC skills** độc lập công cụ, cài đặt mặc định.
- **Exemplar Reference**: [examples/stripe-integration](examples/stripe-integration) được lưu giữ riêng làm thư viện mẫu tham khảo, loại khỏi danh mục đóng gói chính thức.
- **Deprecated Skills Archive**: [archive/deprecated-skills](archive/deprecated-skills) lưu trữ `finishing-a-development-branch` và `requesting-code-review`.

## Workflow và artifact ownership

- `skills/using-sdlc-skills/SKILL.md` là **router mặc định duy nhất**. Không bật router upstream khác làm entry point cạnh tranh.
- `workflows/feature-loop.md` dành cho feature trong repo hiện hữu; `full-sdlc.md` cho sản phẩm/hệ thống mới hoặc thay đổi lớn; `bug-fix.md`, `quick-change.md` và `incident-response.md` dùng theo loại việc.
- PRD chính: `docs/prd.md` (khi cần).
- Story và AC chính thức: `docs/features/<feature-id>/spec.md` theo `templates/specs/feature-spec.md`. Không duy trì một bản Story/AC độc lập khác cho cùng feature.
- SRS, use cases và RTM chỉ dùng khi độ phức tạp/rủi ro/tuân thủ đòi hỏi.
- Architecture, ADR, API contracts và detailed design chỉ sinh khi quyết định hoặc thay đổi tương ứng cần được ghi lại.
- `planning-and-task-breakdown` là chủ sở hữu duy nhất của task list cuối cho một feature; các skill/workflow khác không được tạo danh sách task cạnh tranh.
- `pm-user-story` sở hữu Story/AC; `code-review-and-quality` review diff; `verification-before-completion` kiểm chứng kết quả thực tế bằng bằng chứng tươi.

## Cài đặt

Yêu cầu Python 3.10+; Git chỉ cần khi muốn đồng bộ các upstream đã cấu hình.

```bash
# Kiểm tra nội dung và provenance
python scripts/lint_pack.py --strict
python -m unittest discover -s tests -v

# Cài đặt theo Profile (tối ưu footprint context):
# 1. Profile 'eager-lean' (8 skills, ~20k tokens) — tối ưu cho runtime nạp eager
python scripts/install.py codex --profile eager-lean

# 2. Profile mặc định 'core' / 'canonical-32' (32 skills, ~81k tokens)
python scripts/install.py claude
python scripts/install.py gemini
python scripts/install.py cursor
python scripts/install.py copilot
python scripts/install.py antigravity
python scripts/install.py antigravity-cli

# 3. Cài đặt toàn bộ 32 skills có chỉ định profile hoặc đường dẫn custom
python scripts/install.py codex --profile canonical-32
python scripts/install.py custom --dest ./my-agent/skills
```

Installer không ghi đè skill đã bị thay đổi nếu không yêu cầu rõ; `--force` tạo backup trước khi thay thế. Dùng `--dry-run` để kiểm tra đường dẫn và xung đột trước khi cài. Đường dẫn trong `adapters/agents.json` có thể thay đổi theo phiên bản agent; override bằng `--dest` khi cần.

## Đồng bộ upstream

`python scripts/sync_upstream.py` tải nguồn, stage, kiểm tra rồi mới thay các skill được liệt kê trong `upstream.json`. Sync mặc định dùng commit lock. `python scripts/sync_upstream.py --update` mới yêu cầu cập nhật lên ref mới. **Không chạy sync nếu chưa có mạng hoặc chưa định rõ version/update chủ đích.** Skill adapt trong `derived_skills` không được sync tự động và không bị ghi đè.

```bash
python scripts/sync_upstream.py
python scripts/lint_pack.py --strict
```

Lần đầu sync có thể thay `manifests/upstream-lock.json`, `manifests/skill-provenance.json` và `THIRD_PARTY_NOTICES.md`; review diff trước khi commit. Các skill bị bỏ khỏi manifest được giữ để review; chỉ dùng `--prune` sau khi đã kiểm tra đường dẫn bị retire.

## Quality checks và giới hạn đã biết

- Linter kiểm tra frontmatter, liên kết Markdown cục bộ, thư mục skill được chọn, license, provenance/hash và skill map.
- Unit tests bao phủ linter, installer và sync transaction trên local Git fixture.
- Các test tự động **không chứng minh agent thật kích hoạt đúng skill hay hoàn thành workflow end-to-end**. Chưa xác nhận thực thi trên nhiều agent trong lần build này; nên smoke-test feature, bug fix và release trên ít nhất hai agent trước khi tuyên bố tương thích đã được xác minh.
- `--strict` xác minh pack hiện tại đầy đủ theo manifest và nguồn đã khóa; nó không tự cập nhật revision của các nguồn adapt thủ công.
- Xem `THIRD_PARTY_NOTICES.md`, thư mục `third_party/`, root `LICENSE` và `manifests/skill-provenance.json` trước khi redistribute.
