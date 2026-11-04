# Deprecation Notice: [TARGET_CAPABILITY_OR_API]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Deprecation Notice & Migration  
> **Primary Owner Skill:** `deprecation-and-migration`  
> **Canonical Destination Path:** `docs/migrations/[slug]-deprecation.md`  
> **Status:** `<Announced | In Deprecation | Retired>`  
> **Last updated:** `<YYYY-MM-DD>`  

---

## 1. Deprecation Overview & Motivation (Required)
- **Target Item:** `[API Endpoint / Database Column / Subsystem / Feature]`
- **Effective Deprecation Date:** `[YYYY-MM-DD]`
- **Target Retirement Date:** `[YYYY-MM-DD]`
- **Primary Owner / Team:** `[Team / Lead]`

### Rationale
[Explain why this capability is being deprecated (e.g., technical debt, security vulnerability, replacement by modern API, lack of usage). Ground this in business and technical justification.]

---

## 2. Affected APIs, Schemas & Consumers (Required)
| Deprecated Item | Modern Replacement | Breaking Severity | Impacted Consumers / Services |
|---|---|---|---|
| `v1/getUsers` | `v2/users` | High (Contract change) | Web Client, Mobile App v1.x |

---

## 3. 4-Phase Expand/Contract Migration Strategy (Required)

### Phase 1: Expand (Dual-Write / Dual-Support)
- [ ] Deploy new replacement capability alongside deprecated item
- [ ] Enable telemetry/logging on deprecated item to monitor active callers
- [ ] Add runtime deprecation headers/warnings (`Warning: 299 - "Deprecated API"`)

### Phase 2: Migrate Consumers
- [ ] Provide backward-compatible adapters or client SDK updates
- [ ] Migrate internal services and high-volume consumers to new API
- [ ] Active telemetry tracking shows caller count decreasing to 0

### Phase 3: Contract (Read-Only / Soft-Deprecate)
- [ ] Disable write operations or introduce brownout tests (temporary synthetic downtime)
- [ ] Confirm no unhandled customer alerts or blocking errors occur

### Phase 4: Purge & Retire (Hard Deprecation)
- [ ] Remove old code, schemas, and routes entirely from codebase
- [ ] Archive documentation and mark notice as `Retired`

---

## 4. Client Migration Guide & Code Examples (Required)

### Deprecated Usage (Before)
```typescript
// Deprecated: Do not use
const users = await api.v1.getUsers({ filter: "active" });
```

### Modern Usage (After)
```typescript
// Modern replacement
const users = await api.v2.users.list({ status: UserStatus.ACTIVE });
```

---

## 5. Verification & Sunsetting Gate (Required)
- [ ] Deprecation notice published and communicated to all consumers
- [ ] Telemetry confirms 0 active calls/references to deprecated capability
- [ ] Migration path validated with end-to-end integration tests
- [ ] Final retirement and code removal executed and verified
- **Retirement Sign-off:** [Engineering Lead / Date]
