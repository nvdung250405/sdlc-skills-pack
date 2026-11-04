# Deprecation & migration workflow

> **Document type:** Standardized Workflow Definition  
> **Workflow:** `deprecation-and-migration`  
> **Scenario Group:** Maintenance & Optimization  
> **Trigger / Input:** Sunsetting legacy API, database schema evolution without downtime, replacing core subsystem  
> **Primary Stages:** Deprecation Notice → Expand (Dual-Write) → Backfill & Parity → Contract (Read-Switch) → Purge & Retire  
> **Key Output:** Deprecation notice, migration scripts, zero-downtime data transition  
> **Verification / Exit Gate:** Telemetry confirms 0 active calls, full test suite passing, legacy schema safely purged  

---


Use this workflow when removing legacy systems, migrating database schemas in production without downtime (Expand/Contract), phasing out public APIs, or replacing core dependencies (Stage 10: Maintenance & Evolution).

---

## 1. Announcement & Deprecation Notice
1. **Define Deprecation Scope & Sunset Timeline**:
   - Establish deprecation milestones: Announcement Date $\rightarrow$ Brownout Windows $\rightarrow$ Hard Sunset Date.
2. **Publish Deprecation Guide**: Scaffold and commit `docs/migrations/[slug]-deprecation.md` (from `templates/delivery/deprecation-notice.md`).
3. **Emit Early Warnings**:
   - For APIs: Add standard HTTP `Deprecation: @<timestamp>` and `Sunset: <date>` response headers.
   - For SDKs/Modules: Emit non-blocking compiler/runtime warnings (`@deprecated`) directing users to the replacement.

## 2. Phase 1 — Expand (Additive Changes & Dual-Writing)
4. **Deploy Additive Structure**:
   - For Database: Add new nullable columns or new tables (`database-design`). Never rename or delete active columns in-place.
   - For APIs: Deploy new endpoints or v2 schemas alongside existing endpoints.
5. **Implement Dual-Writing**:
   - Application writes to both old and new data structures simultaneously.
   - Application continues reading from the old structure.

## 3. Phase 2 — Backfill & Parity Verification
6. **Migrate Historical Data**: Run idempotent background workers or batch jobs to backfill historical records from the old structure to the new structure.
7. **Verify Data Parity**: Run checksums or reconciliation queries to ensure old and new stores are 100% consistent under production write load.

## 4. Phase 3 — Contract (Read Switch & Brownout)
8. **Switch Application Reads**:
   - Update application queries to read exclusively from the new structure.
   - Continue dual-writing to the old structure as a temporary fallback mechanism.
9. **Execute Brownout Window**:
   - Introduce brief, scheduled artificial failures (e.g. 15-minute simulated 410 Gone responses) on deprecated endpoints during non-peak hours to identify unmigrated consumer systems before hard cutoff.

## 5. Phase 4 — Drop, Cleanup & Retirement
10. **Cease Dual-Writing**: Remove write paths to the legacy structure.
11. **Drop Legacy Schema**: Execute safe drop commands (`ALTER TABLE ... DROP COLUMN ...`) during low-traffic windows.
12. **Prune Dead Code**: Use `code-simplification` to delete obsolete adapters, dual-write logic, and legacy branches.
13. **Final Verification**: Run `verification-before-completion` to confirm test suites, monitoring dashboards, and build pipelines remain 100% green. Mark migration status as `Retired` in `docs/migrations/[slug]-deprecation.md`.
