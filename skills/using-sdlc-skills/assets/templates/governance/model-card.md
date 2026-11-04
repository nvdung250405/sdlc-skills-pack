# AI Model Card & Governance Audit: [MODEL_OR_AGENT_NAME]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** AI Model Card & Governance Audit  
> **Primary Owner Skill:** `using-sdlc-skills`, `context-engineering`, `skill-authoring`  
> **Canonical Destination Path:** `docs/ai/model-card-[id].md`  
> **Status:** `<Draft | In Review | Verified | Deprecated>`  
> **Last updated:** `<YYYY-MM-DD>`  

| Metadata | Value |
|---|---|
| **Model / Agent Name** | [AGENT_OR_MODEL_IDENTIFIER] |
| **Model Base / Provider** | [e.g. Claude 3.5 Sonnet / Gemini 1.5 Pro / Self-Hosted] |
| **Version & Release Date** | `v1.0.0` / [YYYY-MM-DD] |
| **Responsible Team** | [AI / ML Governance Team] |
| **Operational Tier** | Production / Staging / Sandbox |

---

## 1. Intended Use & Capabilities

- **Primary Task Scope:** Code synthesis, contract verification, technical task breakdown.
- **Out-of-Scope Activities:** Direct production deployment without human sign-off; executing raw untested migrations on customer databases.
- **Target User Personas:** Software Developers, QA Engineers, SREs.

---

## 2. Safety Guardrails & Operational Constraints

- **System Boundaries:** Read/Write isolation enforced via isolated Git worktrees.
- **Forbidden Operations:** Bypassing authentication gates, cracking challenges, disabling security linters.
- **Prompt Injection Defense:** Strict separation of system instructions and user-supplied untrusted inputs.

---

## 3. Evaluation Benchmarks & Verification Results

| Benchmark Dataset | Metric Evaluated | Observed Score | Conformance Target | Status |
|---|---|---|---|---|
| **HumanEval / Golden Tasks** | Pass@1 Accuracy | 88.5% | > 80% | ✅ Pass |
| **Security Prompt Injection** | Rejection Rate | 99.1% | > 98% | ✅ Pass |
| **Contract Schema Linting** | Valid YAML Output | 100% | 100% | ✅ Pass |

---

## 4. Execution Audit & Audit Logging Policy

- **Input/Output Retention Period:** 30 days stored in encrypted audit logs.
- **PII Scrubbing:** All API tokens, customer names, and emails masked prior to inference.
