# Task Handoff & Session State: [TASK_OR_FEATURE_ID]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Task Session & Role Handoff  
> **Primary Owner Skill:** `task-handoff`  
> **Canonical Destination Path:** `.agent/tasks/<task-id>.md`  
> **Status:** `<Active | Blocked | Complete>`  
> **Last updated:** `<YYYY-MM-DD>`  

- **Current Owner / Agent:** `[Role / Agent ID]`
- **Governing Workflow:** `[e.g. workflows/feature-loop.md]`
- **Current Lifecycle Stage:** `[Requirements / Planning / Construction / Verification]`

---

## 1. Goal & Context (Required)
[One-sentence statement of what this session is accomplishing, constraints, and confirmed stack facts.]

---

## 2. Authoritative Artifact Links (Required)
Do not copy large document bodies here. Maintain strict pointer references:
- **Feature Spec:** `docs/features/<feature-id>/spec.md`
- **Plan & Tasks:** `docs/features/<feature-id>/plan.md`, `tasks.md`
- **Architecture / ADRs:** `docs/architecture.md`, `docs/adr/`
- **Acceptance Report:** `docs/features/<feature-id>/acceptance-report.md`

---

## 3. Work Completed So Far (Required)
- [x] Step 1: [What was implemented and verified with fresh tests]
- [x] Step 2: [Files created/modified, commits made]

---

## 4. Current Blockers & Failed Attempts (Required)
- **Blockers:** [None, or describe technical impediment]
- **Failed Attempts / Dead Ends:** [Document what was tried and why it failed to prevent next agent repeating it]

---

## 5. Immediate Next Step & Verification (Required)
- **Next Exact Action:** [Concrete next task step]
- **Target Files:** `[file paths to edit]`
- **Verification Command:** `[exact command to run next]`

---

## 6. Subagent Dispatch Records (Optional - Multi-Agent / Swarm)
When delegating slices to subagents (`invoke_subagent` / `/teamwork`), log active assignments:
- **Subagent 1:** `[Subagent ID / Conversation ID]`
  - **Assigned Role:** `[Implementer | Reviewer | Debugger]`
  - **Bound Skills:** `[e.g. skills/test-driven-development/SKILL.md]`
  - **Assigned Slice:** `[Task ID / component path]`
  - **Outcome / Evidence:** `[Tests passing / Exit code 0]`

---

## 7. Handoff Integrity Checklist (Required)
- [ ] All modified files are committed or cleanly staged in Git
- [ ] Passing test suite verified before handoff
- [ ] Canonical artifact links updated
- **Handed off by:** [Agent ID / Timestamp]
