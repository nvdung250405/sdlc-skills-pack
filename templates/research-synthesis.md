# Research Synthesis: [INITIATIVE_OR_PRODUCT_NAME]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Customer & Market Research Synthesis  
> **Primary Owner Skill:** `customer-research`, `interview-me`, `idea-refine`  
> **Canonical Destination Path:** `docs/discovery/[initiative]/research-synthesis.md`  
> **Status:** `<Draft | In Review | Validated | Superseded>`  
> **Last updated:** `<YYYY-MM-DD>`  

| Metadata | Value |
|---|---|
| **Initiative Name** | [INITIATIVE_NAME] |
| **Research Lead** | [UX Researcher / Product Lead] |
| **Date Completed** | [YYYY-MM-DD] |
| **Data Sources** | [N Customer Interviews, Survey N=XXX, Analytics Cohorts] |
| **Status** | `Validated` / `Pivoted` / `Invalidated` |

---

## 1. Problem Framing & Core Jobs-to-be-Done (JTBD)

### Target User Persona
- **Primary Persona:** [e.g. Senior Backend Engineer managing microservices]
- **Core Motivation:** Accelerate reliable service-to-service integration without manual breaking changes.

### Core JTBD Statement
> *"When I need to update an API endpoint across distributed teams, I want an automated, machine-executable contract verification, so that I can ship changes without breaking consumer applications."*

---

## 2. Key Insights & Voice of Customer (VoC)

| # | User Insight / Pain Point | Evidence / Direct Quote | Severity |
|---|---|---|---|
| **INS-01** | Teams lack a single source of truth for message schemas. | *"We document Kafka payloads in Confluence, but the code drifts after two weeks."* | High |
| **INS-02** | Manual testing of contracts slows down release velocity. | *"We spent 3 days debugging an enum discrepancy in staging."* | High |
| **INS-03** | Engineers prefer standard CLI tools over proprietary UI portals. | *"Just let me run a CLI command in pre-commit or CI."* | Medium |

---

## 3. Competitive & Market Alternatives

| Alternative Approach | Strengths | Critical Weaknesses / Gaps |
|---|---|---|
| **Manual Markdown Specs (`api.md`)** | Easy to write, zero tooling needed. | Non-executable, quickly drifts, no automated validation. |
| **Centralized API Portal (SaaS)** | Good UI visualization. | Vendor lock-in, disconnected from local developer Git workflow. |
| **Packaged Contract-First Pack** | Machine-executable, CLI-first, zero vendor lock-in. | Requires adherence to schema discipline. |

---

## 4. Next Steps & Handoff to Requirements

- [ ] Transition validated insights into **Product Requirements Document (`PRD.md`)**.
- [ ] Scaffold primary interface contract (`templates/openapi.yaml` or `asyncapi.yaml`).
