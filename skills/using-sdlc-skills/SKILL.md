---
name: using-sdlc-skills
description: Use when routing software tasks through standardized SDLC workflows, templates, and specialized engineering skills.
---

# Using the SDLC skill pack

This is the **only default pack-level router**. Classify the task, select the smallest adequate workflow, call only the skills needed, and ensure each stage hands off its output through the canonical artifact contract.

## Demand-Driven Skill Loading

The pack separates installation from active prompt loading. With **29 Core skills** (default engineering discipline) and **34 Extras skills** (specialized domain/stack capabilities), agents follow a 5-step demand-driven lifecycle:

```
Task Intake ──► Discover & Select ──► Load & Scaffold ──► Execute Work ──► Verify & Handoff
      │                 │                     │                   │                 │
  Classify       Workflow + Skills       Read Workflow &      Domain Work      Evidence-backed
   Stage          + Template             Scaffold Template   (Code/Spec/Design)   Check
```

1. **Task Intake**: Map user intent to an SDLC Stage.
2. **Discover & Select**: Select 1 procedural workflow (`workflows/<name>.md`), the smallest sufficient set of skills (typically 1–2 Core + 0–1 Extras), and the target artifact template (`templates/<path>`).
3. **Load & Scaffold**: Read the workflow steps into active context and scaffold the starter template into the canonical destination path on disk using `python scripts/scaffold.py <alias>`.
4. **Execute**: Follow workflow steps, populating real domain logic and acceptance criteria.
5. **Verify & Handoff**: Prove completion with evidence (`verification-before-completion`) and record state in `.agent/tasks/<task-id>.md` (`task-handoff`).

## Fast Triage: Workflow Selection

| Task Type | Recommended Route | Primary Workflow |
|---|---|---|
| New initiative / product | Discovery (`interview-me`, `idea-refine`, `pm-product-spec`) → Architecture → Planning → Implementation | `workflows/full-sdlc.md` |
| User-facing feature | `pm-product-spec` → `pm-user-story` → `pm-spec-quality-audit` → `planning-and-task-breakdown` → TDD/Implementation | `workflows/feature-loop.md` |
| Small, clear change | Repository guidance → `incremental-implementation` → `test-driven-development` → `verification-before-completion` | `workflows/quick-change.md` |
| Bug / unexpected behavior | `systematic-debugging` → reproduce → regression test → minimal fix → `verification-before-completion` | `workflows/bug-fix.md` |
| Refactor / Cleanup | Characterization tests → `codebase-design` (if installed) → `code-simplification` micro-steps → regression verification | `workflows/refactoring.md` |
| Incident / outage | Immediate mitigation → restore service → `systematic-debugging` root cause → regression test | `workflows/incident-response.md` |
| Session / agent transfer | Update `.agent/tasks/<task-id>.md` via `task-handoff`; use `using-git-worktrees` if isolated worktree needed | `workflows/agent-handoff-contract.md` |
| Deprecation / migration | 4-phase Expand/Contract zero-downtime transition using `database-design`, `deprecation-and-migration` (if installed), and contract updates | `workflows/deprecation-and-migration.md` |
| Performance tuning | Baseline benchmark → bottleneck profiling → surgical fix with comparative verification | `workflows/performance-tuning.md` |
| Dependency / CVE update | Audit advisory → worktree branch → bump manifest/lockfile → verify regressions | `workflows/dependency-upgrade.md` |
| A/B experimentation | Metric hypothesis → telemetry schema → variant branch/flag → statistical verification | `workflows/experimentation-loop.md` |

For detailed lookups across all 38 specific intent variants and specialist technologies, see [references/routing-table.md](references/routing-table.md).

## Skill Availability & Graceful Fallback Protocol

When a workflow recommends an Extras specialist skill (e.g. `k6-load-testing`, `browser-testing-with-devtools`, `api-contract-testing`, `terraform-specialist`):
1. **Check Availability**: If the skill directory is not present in the current target installation profile (e.g. Core-only):
2. **Do Not Hallucinate**: Never claim an uninstalled specialist tool was run or silent-fail.
3. **Execute Fallback**: Execute the standard engineering fallback built into the active workflow:
   - *Contract tests missing*: Run `python scripts/verify_contracts.py` to validate contract syntax and schemas.
   - *Load testing missing*: Run standard benchmark/timing scripts with execution logs.
   - *Browser automation missing*: Run unit/DOM tests and inspect component output directly.
   - *Specialist review missing*: Audit changes against canonical checklists in `shared/references/` (or skill references).
4. **Report Limitations**: Honestly document the fallback and any verification limitations in `.agent/tasks/<task-id>.md`.

## Canonical Artifact Contracts

The pack provides **32 lean starter templates** in `templates/` (and router assets `assets/templates/`). Always scaffold to canonical project paths:
- Feature Spec: `docs/features/<feature-id>/spec.md` (from `templates/specs/feature-spec.md`)
- Product Spec (PRD): `docs/prd.md` (from `templates/specs/PRD.md`)
- Architecture Overview: `docs/architecture.md` (from `templates/specs/architecture-overview.md`)
- ADR: `docs/adr/ADR-NNN-[slug].md` (from `templates/specs/ADR.md`)
- Tasks: `docs/features/<feature-id>/tasks.md` (from `templates/delivery/tasks.md`)
- Contracts: `contracts/{openapi,asyncapi,stomp-websocket}.yaml`, `contracts/service.proto`, `contracts/schema.graphql` (from `templates/contracts/`)
- Task State & Handoff: `.agent/tasks/<task-id>.md` (from `templates/delivery/task-handoff.md`)
- Acceptance Report: `docs/features/<feature-id>/acceptance-report.md` (from `templates/delivery/acceptance-report.md`)
- Postmortem: `docs/incidents/[YYYYMMDD-slug]/postmortem.md` (from `templates/platform/incident-postmortem.md`)

For the full 32-row contract mapping table and CLI aliases, see [references/artifact-contracts.md](references/artifact-contracts.md).

## Deterministic Execution Scripts

Use helper scripts in `scripts/` (or router bundled `scripts/`):
- **Scaffold Artifacts**: `python scripts/scaffold.py <alias> [--id <id>]`
- **Bounded Command Runner**: `python scripts/bounded_run.py "<command>" [--timeout 180]`
- **Contract Gate**: `python scripts/verify_contracts.py [--dir contracts]`

## Cross-Skill Invariants

1. **One artifact, one owner**: PRD is owned by `pm-product-spec`; Stories/AC by `pm-user-story`; formal system requirements by `requirements-engineering`; architecture by `software-architecture`; ADRs by `documentation-and-adrs`; final tasks by `planning-and-task-breakdown`.
2. **Single pack router**: `using-sdlc-skills` is the only pack router.
3. **Stable IDs**: Never invent references to absent documents, recycle IDs, or renumber downstream references.
4. **No fabricated facts**: Separate evidence, approved decisions, assumptions, and proposed defaults.
5. **Specification precedes implementation**: When scope or behavior changes, amend the spec before writing code.
6. **Evidence before completion**: Use `verification-before-completion`; report exact commands and output.
7. **Tailor by risk**: Do not force PRD/SRS/DDS/ADR onto trivial changes.
8. **Fallback honestly**: Report tool limitations and fallbacks explicitly.
9. **Approval boundaries**: Production/destructive operations require explicit human approval.
10. **Context discipline**: Load strictly on demand (1 workflow + 1–2 skills). Do not dump entire skill packs or templates into prompt context.
