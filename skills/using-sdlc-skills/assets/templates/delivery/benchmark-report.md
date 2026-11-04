# Performance, Load & Benchmark Report: [SYSTEM_OR_FEATURE_NAME]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Performance, Load & Accessibility Benchmark Report  
> **Primary Owner Skill:** `k6-load-testing`, `screen-reader-testing`, `performance-optimization`  
> **Canonical Destination Path:** `docs/features/<feature-id>/benchmark-report.md`  
> **Status:** `<Draft | In Review | Passed SLAs | Regressed>`  
> **Last updated:** `<YYYY-MM-DD>`  

| Metadata | Value |
|---|---|
| **System Under Test** | [SYSTEM_OR_SERVICE_NAME] |
| **Date of Evaluation** | [YYYY-MM-DD] |
| **Lead Evaluator** | [QA / SRE / Performance Engineer] |
| **Commit / Build SHA** | `[COMMIT_HASH]` |
| **Test Environment** | [Staging / Isolated Perf Cluster / Local] |
| **Status** | `Passed SLAs` / `Regressed` / `Blocked` |

---

## 1. Executive Summary & SLO Conformance

| Metric / Objective | Target SLA / SLO | Observed Value (p95) | Conformance | Status |
|---|---|---|---|---|
| **API Response Latency (Read)** | `< 150ms` | `85ms` | 100% within SLO | ✅ Pass |
| **API Response Latency (Write)** | `< 300ms` | `210ms` | 99.2% within SLO | ✅ Pass |
| **Throughput Capacity** | `> 1,500 RPS` | `2,100 RPS` | Exceeds target | ✅ Pass |
| **Error Rate under Peak** | `< 0.1%` | `0.02%` | Low degradation | ✅ Pass |
| **WCAG 2.1 AA Accessibility** | `100% Core Flows`| `0 critical defects` | Compliant | ✅ Pass |

---

## 2. Load & Stress Test Profile (k6 / Artillery)

### Test Configuration
- **Virtual Users (VUs):** Ramp from 50 to 500 VUs over 10 minutes.
- **Sustained Load Duration:** 15 minutes at peak 500 VUs.
- **Scenarios Evaluated:** Authentication flow, paginated resource search, concurrent item creation.

### Latency Distribution

```text
       Latency Percentile Chart
Min:       12ms  |
p50:       45ms  |█████
p90:      110ms  |████████████
p95:      185ms  |██████████████████
p99:      340ms  |████████████████████████████████
Max:      620ms  |█████████████████████████████████████████████
```

### Resource Utilization
- **CPU Peak:** 62% across container replicas.
- **Memory Consumption:** Steady at 410MB / 1GB limit (no memory leaks detected).
- **Database Connection Pool:** Max 38 / 50 active pool connections.

---

## 3. Accessibility & UX Audit (Axe / Lighthouse / Screen Reader)

- **Automated Scanning Tool:** `@axe-core/cli` / Lighthouse v12.
- **Screen Reader Tested:** NVDA / VoiceOver on key flows.
- **Findings & Remediations:**
  - *Contrast Ratios:* All text elements meet minimum 4.5:1 ratio.
  - *Focus Trap / Keyboard Navigation:* Interactive modals trap focus properly; Esc key dismisses.
  - *Aria Attributes:* Correct `aria-expanded` and `aria-live` on dynamic toast updates.

---

## 4. Verification Evidence & Raw Logs

Command executed:
```bash
k6 run --out json=results/k6-summary.json tests/perf/load-test.js
```

Artifacts generated:
- Raw metrics summary: `results/k6-summary.json`
- Accessibility report: `results/axe-report.json`
