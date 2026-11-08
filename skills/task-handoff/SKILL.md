---
name: task-handoff
description: Use when saving multi-step progress, decisions, and next steps to survive context limits or hand off work.
---

# Task handoff

A task file is the single shared memory between roles, sessions and agents.

## The Compounding Loop (Plan → Work → Review → Compound → Repeat)

Every software task follows a continuous, compounding knowledge cycle:
1. **Plan:** Establish clear, falsifiable goals, acceptance criteria, explicit assumptions, and authoritative artifact links (`spec.md`, `ADR`) before writing code.
2. **Work:** Execute in thin, incremental vertical slices (TDD, YAGNI, surgical diffs). Append progress, decisions, and unexpected blockers to the log.
3. **Review:** Conduct multi-axis verification (correctness, architecture boundaries, security reachability, performance, git history) before declaring completion.
4. **Compound:** Distill institutional knowledge at milestone or task completion:
   - *Validated Patterns:* Approaches and test fixtures that worked cleanly.
   - *Footguns & Pitfalls:* Deceptive edge cases, false assumptions, or dead ends encountered.
   - *Systemic Improvements:* Propose concrete updates to `AGENTS.md`, `docs/architecture.md`, ADRs, or persistent memory.
5. **Repeat:** Seed the next task planning cycle with compounded context so the agent team never repeats past mistakes.

## Start
1. Copy `assets/task-template.md` to `.agent/tasks/<YYYYMMDD>-<slug>.md`.
2. Fill Goal, Scope, Acceptance criteria, Links (spec, ADRs). Leave other sections for later.

## While working
Append, do not rewrite. After each meaningful step add a dated line under **Log**:
- decisions and the reason,
- approaches tried that failed, and why,
- open questions or blockers.

## Hand off
Before stopping or switching role/agent, update **Next step** so a fresh agent with no memory can continue. State: current status, exact next action, files touched, commands to verify.

## Resume
Read the task file first, then only the files it points to. Do not re-derive decisions already logged. If the log contradicts the code, trust the code and note the discrepancy.

## Rules
- Pass paths between roles, not pasted content.
- Never put secrets in the task file.
- One task file per task; link related tasks.
- When Knowledge Graph Memory tools are present (`create_entities`, `add_observations`), persist key architecture decisions to the graph so cross-session context survives.
- Always execute the **Compound** step before marking a task complete or starting the next iteration.

Done when a different agent could continue using only this file and the repo.
