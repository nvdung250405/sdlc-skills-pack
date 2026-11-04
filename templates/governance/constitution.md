# [PROJECT_NAME] Engineering Constitution

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Engineering Constitution & Rules  
> **Primary Owner Skill:** `writing-for-agents`, `context-engineering`  
> **Canonical Destination Path:** `AGENTS.md` / `CLAUDE.md` / `.agent/constitution.md`  
> **Status:** `<Ratified | Active | Under Amendment>`  
> **Last updated:** `<YYYY-MM-DD>`  

---

## 1. Core Engineering Principles (Required)

### 1.1 Requirement and evidence traceability
Every non-trivial change MUST link to an accepted requirement or explicitly record why no formal requirement is needed. Completion claims MUST cite observed test/build/review evidence.

### 1.2 Tests protect behavior
Behavioral changes MUST include appropriate tests. A failing test, build, lint or security gate MUST NOT be deleted, weakened or bypassed merely to obtain a green result.

### 1.3 Interfaces and data need owners
Public API, shared schema, migration and architecture-boundary changes MUST be documented and reviewed before implementation when the decision is material or hard to reverse.

### 1.4 Secure by default
Secrets MUST NOT be committed. Input validation, least privilege, safe error handling and dependency risk MUST be considered for exposed or sensitive paths.

### 1.5 Small, reversible changes
Work SHOULD be delivered in small slices with explicit acceptance and rollback strategy. Destructive operations and production changes require an explicit human gate.

---

## 2. Project-Specific Constraints & Commands (Required)

- **Stack & Supported Runtimes:** [e.g., Node.js 20 LTS, Python 3.11, Docker]
- **Required Verification Commands:**
  - Build: `[command]`
  - Unit / Integration Tests: `[command]`
  - Lint / Format: `[command]`
  - Type Check: `[command]`
- **Thresholds:** [Coverage, performance, accessibility, security baseline]
- **Architectural Seams & Forbidden Dependencies:** [e.g., Domain must not depend on Infrastructure directly]
- **Data Retention & Privacy Requirements:** [e.g., PII encrypted, GDPR deletion compliant]

---

## 3. Governance & Compliance Gate (Required)
Changes to this constitution require review by [OWNER/ROLE]. A change that lowers a quality threshold must document the reason, affected risk, approver and expiry/revisit date. The agent MUST NOT amend this file to make its own change pass without approval.

### Constitution Compliance Checklist
- [ ] Engineering principles and Definition of Done (DoD) ratified by engineering leadership
- [ ] Project-specific constraints and verification commands validated on the current codebase
- [ ] No agent or contributor has unilaterally lowered a quality threshold without explicit human approval
- **Ratified by:** [Engineering Lead / Date]
