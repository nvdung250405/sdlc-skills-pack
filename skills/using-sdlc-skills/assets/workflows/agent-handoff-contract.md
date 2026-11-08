# Cross-agent handoff contract

> **Document type:** Standardized Workflow Definition  
> **Workflow:** `agent-handoff-contract`  
> **Scenario Group:** Agent Coordination  
> **Trigger / Input:** Session context limits, role hand-off, agent hand-off, resuming prior work  
> **Primary Stages:** Context Capture → Artifact Pointer Linking → Work & Blockers Summary → Next Concrete Action → Compounding  
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

---

## 3. Subagent Dispatch & Multi-Agent Coordination Protocol

When an Orchestrator / Master Agent delegates tasks to subagents (via `invoke_subagent`, `/teamwork`, or multi-agent orchestration), each subagent starts with a **fresh, isolated context window**. Subagents do **not** inherit previous chat history.

### The Explicit Skill Binding Invariant
> [!IMPORTANT]
> A subagent will **never** automatically know which skill to load or follow unless explicitly instructed. The orchestrating agent **MUST** supply explicit relative file paths to 1–2 required `SKILL.md` files in the subagent's prompt, along with pointers to the authoritative artifact contracts.

### Canonical Subagent Roles & Prompt Templates

#### A. Implementer Subagent (Worker)
Dispatch when executing a vertical code slice or feature task:
```markdown
Role: Feature Implementer Subagent
Assigned Slice: [Task ID & Name from tasks.md, e.g., Task 2.1: User Authentication API]

MANDATORY SKILL INSTRUCTIONS:
Before writing or modifying any code, you MUST read and strictly follow these skills:
1. `skills/test-driven-development/SKILL.md`: Enforce strict Red-Green-Refactor. Write a failing behavioral test first, verify failure, write minimal logic, verify pass.
2. `skills/incremental-implementation/SKILL.md`: Stay strictly within your assigned vertical slice. Do not edit unrelated files.

AUTHORITATIVE POINTERS:
- Feature Spec: `docs/features/<feature-id>/spec.md`
- Task List: `docs/features/<feature-id>/tasks.md`
- API Contracts: `contracts/` (if modifying interfaces)

REQUIRED OUTPUT & EVIDENCE:
- Run all test and build commands through `python scripts/bounded_run.py "<cmd>"`.
- Return to Orchestrator:
  1. Terminal evidence showing test failed first.
  2. Terminal evidence showing test passed after implementation.
  3. Git diff summary of files modified.
```

#### B. Adversarial Reviewer Subagent (Verifier)
Dispatch to review an implemented slice independently without author bias:
```markdown
Role: Adversarial Code & Spec Reviewer Subagent
Assigned Target: [Branch name, PR, or list of modified files from Task ID]

MANDATORY SKILL INSTRUCTIONS:
Before conducting the review, you MUST read and strictly follow these skills:
1. `skills/code-review-and-quality/SKILL.md`: Perform multi-axis audit (correctness, architecture boundaries, complexity, error handling).
2. `skills/verification-before-completion/SKILL.md`: You MUST empirically execute the test suite in the terminal yourself. Do not accept unverified claims.

AUTHORITATIVE POINTERS:
- Acceptance Criteria (Gherkin): `docs/features/<feature-id>/spec.md`
- Quality Checklists: `shared/references/security-checklist.md`, `shared/references/performance-checklist.md`

REQUIRED OUTPUT & EVIDENCE:
- Independent terminal test execution output via `python scripts/bounded_run.py "<test-cmd>"`.
- Categorized findings: Blocker (must fix), Major (defect/debt), Minor (style/nit).
- Final Verdict: `APPROVED` or `CHANGES_REQUESTED`.
```

#### C. Root-Cause Debugger Subagent (Investigator)
Dispatch when investigating unexpected test failures or defect reports:
```markdown
Role: Systematic Debugger Subagent
Assigned Defect: [Exact error message, failing test output, or defect description]

MANDATORY SKILL INSTRUCTIONS:
You MUST read and strictly follow:
1. `skills/systematic-debugging/SKILL.md`: Follow the strict 4-phase root cause isolation process:
   Phase 1: Reproduce & create minimal failing reproduction.
   Phase 2: Isolate root cause with empirical evidence (no guessing).
   Phase 3: Formulate and test hypothesis.
   Phase 4: Implement minimal fix and add permanent regression guard.
   NEVER apply symptom patches or speculative edits.

REQUIRED OUTPUT & EVIDENCE:
- Root cause explanation with proof.
- Automated regression test file path and failure trace.
- Passing test verification command and terminal evidence.
```

---

## 4. Institutionalizing Knowledge (The Compounding Step)

Upon receiving handoffs or concluding task execution across subagents, the Orchestrator must synthesize findings into repository memory (Plan → Work → Review → Compound → Repeat):
1. **Extract Reusable Patterns:** Identify successful code structures, test fixtures, and architectural invariants, updating `docs/architecture.md` or recording ADRs.
2. **Document Pitfalls & Gotchas:** Record failed attempts, edge cases, and deceptive library quirks into `.agent/tasks/<task-id>.md` or `completion-report.md`.
3. **Systemic Rule Updates:** Propose concrete amendments to `AGENTS.md` when recurring friction or coordination gaps between subagents are identified.
4. **Seed Next Cycle:** Carry compounded context forward into the next iteration planning phase.
