# Release Readiness Gate & Checklist

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Release Readiness Gate  
> **Primary Owner Skill:** `shipping-and-launch`  
> **Canonical Destination Path:** `docs/releases/release-checklist.md`  
> **Status:** `<Draft | Pre-Release | Approved | Released>`  
> **Last updated:** `<YYYY-MM-DD>`  

Target Release: `v[X.Y.Z]`  
Release Owner: `[Name / Role]`  
Target Date: `[YYYY-MM-DD]`  

---

## 1. Quality & Verification Gates (Required)
- [ ] All feature acceptance criteria verified with fresh empirical test reports
- [ ] Full regression test suite passing in CI (`100% green`)
- [ ] Linters, static analysis, and type-checking pass with zero errors
- [ ] Performance and load benchmarks meet required SLO thresholds

## 2. Security & Compliance Gates (Required)
- [ ] Vulnerability scan (SAST / SCA) passing with 0 critical or high CVEs
- [ ] Threat model mitigations verified (`docs/security/threat-model-*.md`)
- [ ] No secrets, keys, or development certificates present in build artifacts
- [ ] Data privacy, retention, and GDPR compliance rules satisfied

## 3. Deployment & Operational Readiness (Required)
- [ ] Database migrations tested in staging; rollback script verified
- [ ] Monitoring dashboards, alerts, and distributed tracing confirmed active
- [ ] Operational runbook updated for new services or endpoints
- [ ] Release notes and changelog finalized (`docs/releases/v[X.Y.Z].md`)
- [ ] Rollback strategy and responsible engineer designated

---

## 4. Go / No-Go Decision Gate (Required)
- **Verdict:** `GO` | `NO-GO`
- **Approver Sign-off:**
  - Product Lead: `[Approved / Date]`
  - Tech Lead / Architect: `[Approved / Date]`
  - SRE / Ops Lead: `[Approved / Date]`
