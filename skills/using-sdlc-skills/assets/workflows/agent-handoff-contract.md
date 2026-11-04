# Cross-agent handoff contract

> **Document type:** Standardized Workflow Definition  
> **Workflow:** `agent-handoff-contract`  
> **Scenario Group:** Agent Coordination  
> **Trigger / Input:** Session context limits, role hand-off, agent hand-off, resuming prior work  
> **Primary Stages:** Context Capture → Artifact Pointer Linking → Work & Blockers Summary → Next Concrete Action  
> **Key Output:** Persistent session handoff record in `.agent/tasks/<task-id>.md`  
> **Verification / Exit Gate:** Clean git worktree, fresh verification evidence recorded, pointer links verified  

---

## 1. Hand-off Responsibilities
Every stage, role, or agent handing work to another must record in `.agent/tasks/<task-id>.md` (seeded from `templates/delivery/task-handoff.md` via `task-handoff`):

1. **Task ID & Goal:** Clear, one-sentence statement of what is being accomplished and confirmed tech stack facts.
2. **Authoritative Artifact Pointers:** Strict relative file paths to authoritative documents (`docs/features/<feature-id>/spec.md`, `docs/architecture.md`, `tasks.md`). Do not copy large document bodies into context.
3. **Decisions & Rationale:** Distinguish approved decisions from open proposals. Reference ADRs where applicable.
4. **Files Changed & Worktree State:** Exact list of modified files, git branches, or worktree paths.
5. **Empirical Verification Evidence:** Commands executed, exit codes, and test pass/fail results captured via `verification-before-completion`.
6. **Failed Attempts & Dead Ends:** Document what failed and why, preventing the next agent from repeating dead ends.
7. **Open Questions & Assumptions:** Explicitly stated risks, unverified assumptions, and owner names.
8. **Next Exact Action:** Specific concrete action, target files, and next verification command for the receiving agent.

## 2. Safety & Hygiene Rules
- **Zero Secrets:** Never pass passwords, tokens, API keys, or private customer data into handoff files.
- **Pointer Discipline:** The receiving agent must re-read authoritative files from disk rather than relying solely on copied excerpts.
- **Git State:** Ensure all work in progress is committed to a feature branch or cleanly stashed before hand-off.
