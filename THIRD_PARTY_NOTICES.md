# Third-party notices

This pack redistributes selected upstream skills and contains a small number of locally adapted skills. Preserve the applicable license text when redistributing. Exact pinned revisions and per-skill provenance are recorded in `upstream.json`, `manifests/upstream-lock.json`, and `manifests/skill-provenance.json`.

## Vendored from pinned upstream revisions

### Addy Osmani — Agent Skills
- Source: https://github.com/addyosmani/agent-skills
- Revision: `aeac41d4d005999432bb7312f7ff06383a91d59d`
- License: MIT — see `third_party/addyosmani-agent-skills/LICENSE`
- Selected skills: 19 under `skills/` (`interview-me`, `idea-refine`, `spec-driven-development`, `api-and-interface-design`, `documentation-and-adrs`, `planning-and-task-breakdown`, `incremental-implementation`, `test-driven-development`, `git-workflow-and-versioning`, `source-driven-development`, `code-simplification`, `code-review-and-quality`, `security-and-hardening`, `ci-cd-and-automation`, `shipping-and-launch`, `observability-and-instrumentation`, `performance-optimization`, `frontend-ui-engineering`, `deprecation-and-migration`).

### Superpowers
- Source: https://github.com/obra/superpowers
- Revision: `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`
- License: MIT — see `third_party/obra-superpowers/LICENSE`
- Selected skills: 2 under `skills/` (`systematic-debugging`, `verification-before-completion`).

### Anthropic Skills
- Source: https://github.com/anthropics/skills
- Revision: `dbd4588f9e1033efb41dad4bef2f7947c8993d44`
- License: Apache-2.0 — see `third_party/anthropics-skills/LICENSE`
- Selected skills: 1 under `skills/` (`webapp-testing`).

### Corey Haines — Marketing Skills
- Source: https://github.com/coreyhaines31/marketingskills
- Revision: `0cd9b3a0ef4c411a1d690419ce843f2a1da32cce`
- License: MIT — see `third_party/coreyhaines31-marketingskills/LICENSE`
- Selected skills: 1 under `skills/` (`analytics`).

## Locally adapted skills (not verbatim upstream copies)

### Uxcel Product Skills
- Source: https://github.com/Uxcel-Lab/product-skills
- License: MIT — see `third_party/uxcel-product-skills/LICENSE`
- Adapted skills: 1 under `skills/` (`pm-user-story`).
- Manual-review-only refresh policy with content hash tracking.

### Agentic SDLC Kit
- Source: https://github.com/zeeshanhanif/agentic-sdlc-kit
- License: Apache-2.0 — see `third_party/agentic-sdlc-kit/LICENSE`
- Adapted skills: 1 under `skills/` (`software-architecture`).
- Compact adaptation of software architecture.

### William Hobson — Agents
- Source: https://github.com/wshobson/agents
- License: MIT — see `third_party/wshobson-agents/LICENSE`
- Adapted skills: 1 under `skills/` (`auth-implementation-patterns`).
- Selected agent skill providing authentication token lifecycles and RBAC authorization boundaries.

### Agentic Awesome Skills (sickn33)
- Source: https://github.com/sickn33/agentic-awesome-skills
- License: Code MIT, documentation CC BY 4.0 — see `third_party/sickn33-agentic-awesome-skills/LICENSE`
- Adapted skills: 3 under `skills/` (`database-design`, `docker-expert`, `k6-load-testing`).

## Reference-only projects (no upstream files bundled)

- GitHub Spec Kit: https://github.com/github/spec-kit — used as a reference for specification, Story/AC, independent test and task formats.
- BMAD Method: https://github.com/bmad-code-org/BMAD-METHOD — used as a reference for organizing roles and workflows.

## Pack-owned integration assets

The pack router (`skills/using-sdlc-skills`), handoff (`skills/task-handoff`), contract testing (`skills/api-contract-testing`), local integration workflows, templates, adapters, manifests and scripts are covered by the root `LICENSE`, except where a file explicitly identifies another license or source. Adaptations and their source paths/transformations are listed in `manifests/skill-provenance.json`.
