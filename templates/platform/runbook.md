# Operational Runbook: [SERVICE_OR_SYSTEM_NAME]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Operational Runbook  
> **Primary Owner Skill:** `observability-and-instrumentation`  
> **Canonical Destination Path:** `docs/runbooks/[service-name].md`  
> **Status:** `<Active | Under Review | Deprecated>`  
> **Last updated:** `<YYYY-MM-DD>`  

- **Service / Component:** `[service-name]`
- **Primary Owner / Team:** `[Team / On-Call Rotation]`
- **Repository:** `[Repo URL / path]`
- **Last Verified Date:** `[YYYY-MM-DD]`

---

## 1. System Overview & Architecture (Required)
[Concise summary of what this service does, its critical upstream callers, downstream dependencies, datastores, and SLAs.]

- **Health Check Endpoint:** `GET /healthz` (Expects HTTP 200 `{"status": "ok"}`)
- **Metrics Dashboard:** `[Link to Grafana / Datadog dashboard]`
- **Alert Channel:** `[Slack #alerts-channel / PagerDuty service]`

---

## 2. Common Alerts & Triage Procedures (Required)

### Alert: High Error Rate (HTTP 5xx > 1%)
1. **Diagnosis:** Check recent deployments, error logs, and downstream database latency.
   ```bash
   # View recent error logs
   kubectl logs -l app=service-name --tail=100 | grep "ERROR"
   ```
2. **Mitigation:** If correlated with recent release, rollback to previous image tag.
3. **Escalation:** If database latency is elevated, page On-Call DBA.

### Alert: High Memory / OOMKilled
1. **Diagnosis:** Check pod restart counts and heap memory utilization graph.
2. **Mitigation:** Scale replica count horizontally; increase memory limit if traffic surged.

---

## 3. Routine Operational Procedures (Required)
- **Service Restart:** `[Safe restart command]`
- **Cache Clearing:** `[Cache flush command with safety precautions]`
- **Database Backup Verification:** `[Backup inspection command]`

---

## 4. Runbook Validation & Drill Gate (Required)
- [ ] Diagnostic queries and metrics dashboards verified against live monitoring
- [ ] Mitigation and recovery procedures tested in staging/drill environment
- [ ] Escalation contacts and on-call rotation up to date
- [ ] Last verified date updated
- **Verified by:** [SRE / On-Call Engineer / Date]
