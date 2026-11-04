# Infrastructure & Cost Attribution Report: [BILLING_PERIOD]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Infrastructure & Model Cost Attribution Report  
> **Primary Owner Skill:** `cost-optimization`, `terraform-specialist`  
> **Canonical Destination Path:** `docs/finops/cost-report-[period].md`  
> **Status:** `<Draft | In Review | Within Budget | Over Budget>`  
> **Last updated:** `<YYYY-MM-DD>`  

| Metadata | Value |
|---|---|
| **Billing Period** | [YYYY-MM-DD to YYYY-MM-DD] |
| **FinOps Lead** | [FinOps Practitioner / Engineering Manager] |
| **Total Cloud Spend** | \$[TOTAL_SPEND] (Δ [PERCENT_CHANGE]% vs previous period) |
| **AI Inference Token Spend**| \$[TOKEN_SPEND] |
| **Governance Status** | `Within Budget` / `Approaching Threshold` / `Budget Breached` |

---

## 1. Cost Breakdown by Service & Domain

| Workload / Service Tier | Monthly Spend | Primary Driver | Tagging Conformance |
|---|---|---|---|
| **Core API & Compute (EKS / GKE)** | \$4,200 | Container replica scaling | 98% tagged |
| **Database & Caching (RDS / Redis)**| \$2,850 | Multi-AZ storage & IOPS | 100% tagged |
| **Object Storage (S3 / GCS)** | \$950 | Artifact & log archiving | 95% tagged |
| **AI Inference API (LLM Tokens)** | \$1,400 | Prompt context token volume | 100% tagged |
| **Networking & Egress** | \$600 | Cross-region data transfer | 90% tagged |

---

## 2. AI Inference & Context Optimization Metrics

- **Total Prompt Tokens Consumed:** 45M tokens.
- **Total Completion Tokens Generated:** 6.2M tokens.
- **Token Efficiency Optimization:**
  - Implemented *Progressive Disclosure* on skill docs: saved ~28% prompt tokens per session.
  - Replaced markdown API docs with compact YAML contracts: saved ~15% input payload tokens.

---

## 3. Rightsizing & Cost Optimization Actions

| Recommendation ID | Targeted Resource | Expected Monthly Savings | Effort | Status |
|---|---|---|---|---|
| **OPT-01** | Convert unattached EBS volumes to gp3 | \$180 / mo | Low | Implemented |
| **OPT-02** | Enable S3 Intelligent-Tiering for logs | \$320 / mo | Low | In Progress |
| **OPT-03** | Rightsize staging RDS instance from r6g to t4g | \$250 / mo | Medium | Planned |

---

## 4. Verification & Audit Trail

- Billing data source: AWS Cost Explorer / GCP Cloud Billing Export.
- Unit economic cost per active user: \$0.042 / user / month.
