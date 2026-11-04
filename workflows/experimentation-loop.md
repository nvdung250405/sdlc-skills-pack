# Product experimentation & A/B testing loop

> **Document type:** Standardized Workflow Definition  
> **Workflow:** `experimentation-loop`  
> **Scenario Group:** Product Learning  
> **Trigger / Input:** Growth hypothesis, competing UX variants, conversion funnel optimization  
> **Primary Stages:** Hypothesis & Metrics → Telemetry Instrumentation → Variant Construction → Execution → Statistical Evaluation  
> **Key Output:** Experiment brief with statistical analysis, variant rollout or cleanup commit  
> **Verification / Exit Gate:** Target sample size achieved, p < 0.05 on primary metric, zero dead code after rollout  

---


Use this workflow when testing competing UX variants, optimizing conversion funnels, measuring feature adoption, or running continuous growth experiments (Stage 11: Product Learning & Measurement).

---

## 1. Hypothesis Formulation & Success Metrics
1. **Grounded Observation**: Anchor the experiment in qualitative feedback (`customer-research`, user interviews) or analytics friction (`analytics` funnel drop-offs).
2. **Formulate Falsifiable Hypothesis**:
   > *Because [observation], we believe that [variant change] will cause [expected behavioral outcome] for [target audience]. We will know this is true when [primary metric reaches significance].*
3. **Define Metrics in `docs/experiments/[exp-id]-[slug].md`** (scaffold from `templates/experiment-brief.md`):
   - **Primary Metric (Overall Evaluation Criterion - OEC)**: The single decision metric (e.g., checkout completion rate).
   - **Secondary & Guardrail Metrics**: Metrics that must not degrade (e.g., page load latency, error rate, refund requests).
   - **Target Parameters**: Minimum Detectable Effect (MDE), 95% confidence level ($p < 0.05$), 80% statistical power.

## 2. Telemetry & Tracking Instrumentation
4. **Define Event Taxonomy**: Use `analytics` to specify event triggers, parameters, and property schemas in `docs/analytics/tracking-plan.md` (from `templates/tracking-plan.md`).
5. **Implement Event Telemetry**: Instrument frontend/backend event tracking. Verify in debug mode that payloads match schema and contain no PII.

## 3. Variant Construction & Traffic Allocation
6. **Implement Treatment Variants**: Build experimental UI/logic using `incremental-implementation` and `vercel-react-best-practices` behind an experimentation flag or feature management service.
7. **Define Cohort Eligibility**: Specify traffic allocation (e.g., 50% Control / 50% Treatment), user segmentation, and exclusions.

## 4. Execution & Monitoring
8. **Launch Experiment**: Ramp traffic safely (e.g. 5% canary $\rightarrow$ 50/50 full split).
9. **Monitor Guardrails**: Continuously monitor system health and guardrail metrics with `observability-and-instrumentation`. Trigger immediate abort if error rates spike.
10. **Run to Fixed Sample Size**: Avoid premature stopping (peeking problem); run until pre-calculated sample size or duration is achieved.

## 5. Statistical Evaluation & Rollout Decision
11. **Analyze Results**: Calculate conversion rates, relative lift, standard error, and p-value using `ab-testing` and `analytics`.
12. **Make Rollout Decision**:
    - **Winner ($p < 0.05$ with positive lift)**: Roll out Treatment to 100% of users. Remove feature flags and dead control code using `code-simplification`.
    - **Inconclusive / Neutral**: Analyze secondary signals. Decide whether to iterate hypothesis or discard.
    - **Degraded**: Roll back immediately to Control.
13. **Verification Gate**: Run `verification-before-completion` after flag removal and cleanup to capture fresh test suite and build evidence, proving zero regressions in production paths.
14. **Record Learnings**: Document final findings, statistical tables, and next test recommendations in `docs/experiments/[exp-id]-[slug].md`.
