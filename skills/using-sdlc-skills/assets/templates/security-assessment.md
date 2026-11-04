# Security Assessment & Vulnerability Record: [SYSTEM_NAME]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Security Assessment & Vulnerability Remediation Record  
> **Primary Owner Skill:** `security-and-hardening`, `secrets-management`, `auth-implementation-patterns`  
> **Canonical Destination Path:** `docs/security/security-assessment-[id].md`  
> **Status:** `<Draft | In Review | Remediated | Action Required>`  
> **Last updated:** `<YYYY-MM-DD>`  

| Metadata | Value |
|---|---|
| **Target System** | [SERVICE_OR_REPOSITORY_NAME] |
| **Audit Date** | [YYYY-MM-DD] |
| **Security Reviewer** | [AppSec / DevSecOps Engineer] |
| **Commit Evaluated** | `[COMMIT_HASH]` |
| **Overall Posture** | `Compliant` / `Action Required` / `Critical Breach` |

---

## 1. Automated Scan Summary & Quality Gate

| Tooling Used | Target Inspected | Critical | High | Medium | Low | Status |
|---|---|---|---|---|---|---|
| **SAST (Semgrep / CodeQL)** | Application Source Code | 0 | 0 | 1 | 2 | ✅ Pass |
| **SCA / Dependency Audit** | Package Lockfiles | 0 | 0 | 0 | 3 | ✅ Pass |
| **Container Scanner (Trivy)** | Docker Base Image | 0 | 1 | 4 | 8 | ⚠️ Remediation Planned |
| **Secret Scanner (Gitleaks)** | Git Commit History | 0 | 0 | 0 | 0 | ✅ Pass (No Leaks) |

---

## 2. Identified Vulnerabilities & Remediation Plan

### Finding SEC-001: [Brief Finding Title]
- **Severity:** High / Medium / Low
- **Vulnerability Type:** CWE-XXX (e.g. Insecure Direct Object Reference, Outdated Dependency)
- **Component Affected:** `src/auth/token_validator.ts:L42`
- **Description:** Untrusted input deserialization without strict schema validation.
- **Remediation Action:** Upgraded dependency `package-xyz` to `v2.4.1` and added input schema constraint.
- **Verification Evidence:**
  ```bash
  npm audit --audit-level=high
  # Result: found 0 vulnerabilities
  ```
- **Remediation Status:** `Remediated` / `Accepted Risk` / `In Progress`

---

## 3. Access Control & Identity Verification (RBAC / ABAC)

- [x] Principle of Least Privilege verified across all API endpoints.
- [x] JWT signature validated using asymmetric public keys (RS256 / Ed25519).
- [x] Explicit token expiration enforced (max 24h).
- [x] Sensitive personal data (PII) masked in application logs and trace contexts.

---

## 4. Privacy & Compliance Checklist (GDPR / CCPA)

- **PII Data Inventory:** Explicit listing of collected fields (`email`, `ip_address`).
- **Data Retention & Purge Policy:** Automated purge after retention period (e.g., 90 days).
- **User Deletion Endpoint:** Verified soft and hard delete cascading.
