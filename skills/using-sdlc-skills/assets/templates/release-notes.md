# Release Notes: v[X.Y.Z]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Release Notes & Changelog  
> **Primary Owner Skill:** `shipping-and-launch`  
> **Canonical Destination Path:** `docs/releases/v[X.Y.Z].md`  
> **Status:** `<Draft | Published>`  
> **Last updated:** `<YYYY-MM-DD>`  

- **Release Date:** `[YYYY-MM-DD]`
- **Release Owner / Lead:** `[Name / Role]`
- **Target Environment:** `[Staging / Production]`
- **Semver Type:** `Major` | `Minor` | `Patch`

---

## 1. Highlights & Summary (Required)
[Concise executive summary of key user-facing features, improvements, and business value delivered in this release.]

---

## 2. Changelog (Required)

### 🚀 New Features
- **[Feature Name]:** [Summary of capability, linking to `docs/features/<feature-id>/spec.md`]

### 🐛 Bug Fixes
- **[Bug Title]:** [Summary of fix, linking to issue ticket and root cause]

### ⚡ Performance & Maintenance
- **[Optimization]:** [Latency reduction, dependency upgrades, refactoring]

---

## 3. Breaking Changes & Upgrade Path (Optional / When Applicable)
- **Breaking Change:** [Description of contract change]
- **Action Required:** [Exact steps consumers must take to migrate]

---

## 4. Deployment & Migration Procedures (Required)
- **Pre-deployment Steps:** [Database migrations, cache priming]
- **Deployment Command:** `[e.g., helm upgrade ... / terraform apply]`
- **Post-deployment Verification:** [Smoke test commands and health checks]
- **Rollback Procedure:** [Exact commands to revert to previous stable tag]

---

## 5. Release Verification Sign-off (Required)
- [ ] Build artifacts and container images signed and verified
- [ ] Smoke tests verified in target environment
- [ ] Error budgets and latency metrics within healthy limits
- **Release Published by:** [Release Lead / Date]
