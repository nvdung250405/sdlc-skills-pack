# Growth Experiment Brief: [EXPERIMENT_NAME]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Growth Experiment Brief  
> **Primary Owner Skill:** `ab-testing`  
> **Canonical Destination Path:** `docs/experiments/[exp-id]-[slug].md`  
> **Status:** `<Draft | Running | Completed | Rolled Out | Discarded>`  
> **Last updated:** `<YYYY-MM-DD>`  

---

## 1. Hypothesis & Problem Framing (Required)
- **Experiment ID:** `EXP-NNN`
- **Target Surface:** `[e.g., Onboarding Flow / Pricing Page / Checkout Step 2]`
- **Experiment Owner:** `[Growth Engineer / PM]`

### The Hypothesis
> **If** we [implement this change / variant capability],  
> **Then** [expected behavioral shift for target user cohort],  
> **Because** [underlying user psychology / friction identified in customer research].

---

## 2. Experiment Setup & Variant Specs (Required)

### Traffic Allocation & Sample Sizing
- **Traffic Split:** Control 50% / Variant 50%
- **Target Audience:** [e.g., 100% of new signups on Web desktop]
- **Minimum Detectable Effect (MDE):** [e.g., +5% relative conversion lift]
- **Estimated Runtime:** [e.g., 14 days to achieve 95% statistical power]

### Variant Definitions
- **Control (A):** [Existing user experience and baseline code]
- **Variant (B):** [Experimental change, UI layout, copy, or logic]

---

## 3. Success Metrics & Telemetry (Required)
| Metric Type | Metric Name | Event Taxonomy / Key | Expected Direction | Guardrail Threshold |
|---|---|---|---|---|
| Primary Metric | Conversion Rate | `signup_completed` | +8% relative lift | N/A |
| Secondary Metric | Time to Activate | `project_created` | -15% duration | N/A |
| Guardrail Metric | Churn / Bounce | `page_abandoned` | Flat | Must not rise > 2% |

---

## 4. Results & Statistical Analysis (Required when completed)
- **Actual Runtime:** `[YYYY-MM-DD]` to `[YYYY-MM-DD]`
- **Sample Size Reached:** Control: `[N]`, Variant: `[N]`
- **Observed Lift:** `[+X.X%]` on Primary Metric
- **Statistical Significance (p-value):** `[p < 0.05 / 95% confidence]`
- **Guardrail Impact:** `[No adverse effect observed]`

---

## 5. Rollout Decision & Verification Gate (Required)
- **Verdict:** `Rollout Variant` | `Iterate Hypothesis` | `Revert to Control`
- **Rollout Action:** [e.g., Gradual 100% rollout via feature flag `ff_new_onboarding`]
- **Code Clean-up:** [ ] Dead control/variant branches removed from codebase

### Experiment Gate Sign-off
- [ ] Experiment setup approved before traffic exposure
- [ ] Sample size and runtime thresholds respected (no peeking bias)
- [ ] Decision recorded and communicated to product stakeholders
- **Approved by:** [Growth Lead / Product Lead / Date]
