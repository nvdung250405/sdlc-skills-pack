# Incident Postmortem: [INCIDENT_TITLE_OR_ID]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Incident Postmortem  
> **Primary Owner Skill:** `observability-and-instrumentation`  
> **Canonical Destination Path:** `docs/incidents/[YYYYMMDD-slug]/postmortem.md`  
> **Status:** `<Draft | In Review | Published>`  
> **Last updated:** `<YYYY-MM-DD>`  

---

## 1. Executive Summary & Impact (Required)
- **Incident Date:** `[YYYY-MM-DD]`
- **Incident Severity:** `[SEV-1 / SEV-2 / SEV-3]`
- **Incident Commander / Lead:** `[Name / Role]`
- **Duration of Impact:** `[e.g., 42 minutes (14:18 UTC to 15:00 UTC)]`

### Impact Summary
- **User Impact:** [e.g., ~15% of checkout requests failed with HTTP 500]
- **Data Loss / Breach:** [Zero data corruption; zero unauthorized exposure]
- **Financial / SLA Impact:** [e.g., $1,200 estimated revenue delay; SLA budget consumed 4%]

---

## 2. Incident Timeline & Chronology (Required)
All timestamps recorded in UTC.

| Timestamp (UTC) | Source / Alert | Event Description & Mitigation Action |
|---|---|---|
| `14:18` | Datadog Alert | Automated PagerDuty trigger on API 5xx rate > 2% |
| `14:22` | Slack #incident | Incident Commander acknowledged alert and opened triage war room |
| `14:35` | SRE Investigation | Identified high DB connection pool exhaustion following release v2.4.1 |
| `14:48` | Mitigation | Rollback of v2.4.1 initiated via deployment pipeline |
| `15:00` | Resolution | Error rate dropped to 0.01%; SLO restored to healthy baseline |

---

## 3. Root Cause Analysis (5 Whys) (Required)
1. **Why did checkouts fail?** Database connection pool became exhausted.
2. **Why was the pool exhausted?** A new unindexed query in v2.4.1 performed sequential table scans under load.
3. **Why did queries perform table scans?** An index migration was omitted from the release deployment step.
4. **Why was the index migration omitted?** The release pipeline script lacked an automated pre-deploy migration check.
5. **Why was the check missing?** CI/CD pipeline lacked an integration gate enforcing schema parity before rollout.

---

## 4. What Went Well / What Went Poorly (Required)

### What Went Well
- Monitoring alerts triggered within 2 minutes of error rate elevation.
- Rollback procedure worked cleanly and restored availability immediately.

### What Went Poorly
- Unindexed query passed local testing due to small test dataset volume.
- Staging environment lacked production-scale performance benchmark gating.

### Where We Got Lucky
- Failure occurred during mid-afternoon off-peak window, limiting affected user count.

---

## 5. Action Items & Remediation Ledger (Required)

| ID | Action Item | Type (Prevent / Mitigate / Detect) | Owner | Target Date | Tracking Ticket |
|---|---|---|---|---|---|
| ACT-01 | Add composite index on `orders(user_id, status)` | Prevent | DBA / Backend | YYYY-MM-DD | `ISSUE-101` |
| ACT-02 | Add automated CI schema check blocking unindexed queries | Detect | Platform Eng | YYYY-MM-DD | `ISSUE-102` |
| ACT-03 | Update deployment runbook with explicit pre-migration gate | Mitigate | SRE Lead | YYYY-MM-DD | `ISSUE-103` |

---

## 6. Postmortem Review & Closure Gate (Required)
- [ ] Root cause identified and backed by timeline telemetry evidence
- [ ] Blameless culture maintained (focused on systemic and tooling failure, not personal blame)
- [ ] Remediation action items have assigned owners, Jira tickets, and realistic due dates
- [ ] Operational runbooks and alert thresholds updated
- **Postmortem Reviewed & Closed by:** [SRE Lead / Engineering Director / Date]
