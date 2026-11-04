# Production incident response workflow

> **Document type:** Standardized Workflow Definition  
> **Workflow:** `incident-response`  
> **Scenario Group:** Defect Resolution  
> **Trigger / Input:** Production alert, outage, service degradation, SLO breach  
> **Primary Stages:** Stabilize & Mitigate → Diagnose Root Cause → Surgical Fix → Postmortem & Prevention  
> **Key Output:** Incident postmortem, preventative action items, runbook update  
> **Verification / Exit Gate:** System SLIs/SLOs restored to healthy baseline for ≥ 15 minutes, postmortem published  

---


Use this workflow for active production or staging incidents affecting service stability, customer experience, data integrity, or security. Follow organizational incident policies and severity definitions when established.

---

## 1. Stabilize & Coordinate
1. **Assess Symptoms & Scope**: Inspect incoming alerts, error rates, p95/p99 latency spikes, affected user segments, and recent deployments.
2. **Assign Incident Commander**: Establish a single operational lead and communication channel (`#war-room`). State provisional severity:
   - `SEV-1 (Critical)`: Full customer outage, critical data corruption, or active security exploit.
   - `SEV-2 (Major)`: High error rate or degraded performance on core revenue/business paths.
   - `SEV-3 (Minor)`: Isolated non-critical failure with available workaround.
3. **Check Service Runbook**: Follow triage instructions in `docs/runbooks/[service-name].md` (from `templates/runbook.md`).
4. **Prioritize Mitigation Over Root Cause**: Restore user service immediately before deep investigation:
   - Revert recent deploy: Roll back to last-known-good version.
   - Shift traffic: Reroute traffic away from unhealthy instances or regions.
   - Throttle / Circuit break: Shed non-critical traffic or disable degraded features via feature flags.
5. **Preserve Evidence**: Snapshot logs, container states, and metrics. Never paste secrets, credentials, or customer PII into incident notes.

## 2. Diagnose & Resolve Root Cause
6. **Telemetry Deep-Dive**: Once service is restored or stabilized, use `observability-and-instrumentation` and `service-mesh-observability` to correlate traces, error spikes, and database pool saturation.
7. **Isolate in Non-Production**: Use `systematic-debugging` to reproduce the failure in staging or a local reproduction environment. Do not perform high-risk exploratory experiments directly on production.
8. **Develop Smallest Surgical Fix**: Write a regression test proving the failure, implement the fix with `test-driven-development`, and verify against production-equivalent volume/edge conditions.
9. **Verification Gate**: Execute `verification-before-completion` to document build, test, and health check pass logs before promoting the fix to production or declaring recovery.

## 3. Postmortem, Action Items & Prevention
10. **Author Blameless Postmortem**: Scaffold and publish `docs/incidents/[YYYYMMDD-slug]/postmortem.md` (from `templates/incident-postmortem.md`) within 48 hours:
   - Summary and customer impact (duration, % requests affected).
   - Detailed timeline in UTC.
   - Root cause analysis using 5 Whys.
   - What went well vs. where response was delayed or fortunate.
11. **Track Preventative Action Items**: Convert preventative measures (index additions, alert threshold tuning, pipeline gates, circuit breakers) into concrete backlog tickets with designated owners and target completion dates.
12. **Update Runbooks & Alerts**: Ensure `docs/runbooks/[service-name].md` and alert thresholds are updated to catch or auto-mitigate similar failure modes in the future.

---

> [!CAUTION]
> Do not declare an incident resolved solely because an alert cleared. Confirm end-user traffic and core SLIs/SLOs have normalized within the target operating envelope for at least 15 minutes.