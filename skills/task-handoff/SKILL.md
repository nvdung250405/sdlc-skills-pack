---
name: task-handoff
description: Use when saving multi-step progress, decisions, and next steps to survive context limits or hand off work.
---

# Task handoff

A task file is the single shared memory between roles, sessions and agents.

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

Done when a different agent could continue using only this file and the repo.

## Environment Integration

> [!TIP]
> This skill runs best when the agent exploits the active environment:
> - **Code navigation**: use `.agent/repo_map.txt` for structural orientation or call `ast-grep:find_code` / `ast-grep:analyze-imports` instead of reading whole files.
> - **Command execution**: run all shell commands via `python scripts/bounded_run.py <cmd>` to bound output and auto-extract failure stacktraces.
> - **Completion**: finish each session with `verification-before-completion` → `task-handoff` (and `memory:add_observations` for key architecture decisions).
