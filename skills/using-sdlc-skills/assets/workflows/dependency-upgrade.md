# Dependency & security upgrade workflow

> **Document type:** Standardized Workflow Definition  
> **Workflow:** `dependency-upgrade`  
> **Scenario Group:** Maintenance & Optimization  
> **Trigger / Input:** Security advisory, CVE alert, outdated runtime, major framework version  
> **Primary Stages:** Upgrade Triage → Worktree Isolation → Manifest/Lockfile Bump → Code Adaptation → Security Audit → Compounding  
> **Key Output:** Upgraded package manifest and lockfile, clean security scan report  
> **Verification / Exit Gate:** Full test suite passing, 0 critical/high CVEs remaining, `verification-before-completion`  

---


Use this workflow when upgrading frameworks, runtime versions (Node/Python/Go), third-party libraries, or patching CVE security vulnerabilities reported by audit tools (Dependabot, Snyk, Trivy).

---

## 1. Upgrade Triage & Security Audit
1. **Identify Upgrade Triggers & Target Versions**:
   - Routine dependency refresh vs. major framework upgrade vs. critical CVE security patch.
   - For security vulnerabilities: Use `security-and-hardening` to inspect CVE advisories, CVSS severity, attack vectors, and whether vulnerable code paths are actually reachable in your application.
2. **Review Upstream Changelogs & Breaking Changes**:
   - Use `source-driven-development` to inspect the target library's official release notes, breaking change lists, and migration guides.
   - Check deprecation warnings or dropped runtime support.

## 2. Workspace Isolation
3. **Isolate Upgrade Work**:
   - Use `git-workflow-and-versioning` to create an isolated branch workspace (e.g. `git checkout -b deps/update-[lib]`), protecting your active working tree from lockfile churn or broken dependencies.

## 3. Package Manifest & Lockfile Update
4. **Update Manifest & Lockfile**:
   - Update version constraints in the package manifest (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`).
   - Regenerate the lockfile cleanly (`npm install`, `poetry lock`, `go mod tidy`) without manual edits.
   - Review package lock diffs for unexpected transitive dependencies or supply-chain risks.

## 4. Code Adaptation & Deprecation Fixes
5. **Fix Breaking Changes & Deprecations**:
   - Address any broken imports, altered function signatures, or renamed configuration keys.
   - Apply `incremental-implementation` to migrate to new APIs recommended by the library vendor.
   - Ensure no new compiler or linter warnings are introduced.

## 5. Comprehensive Verification & Security Gate
6. **Execute Automated Test Suites**:
   - Run unit, integration, and wire contract tests (`api-contract-testing`).
   - Verify UI runtime behavior using `webapp-testing` or `browser-testing-with-devtools` if web dependencies were updated.
7. **Run Security Vulnerability Scan**:
   - Execute package manager security audit commands (`npm audit`, `pip-audit`, `cargo audit`).
   - Verify that reported CVEs are resolved and 0 high/critical vulnerabilities remain.
8. **Final Evidence & Review**:
   - Run `verification-before-completion` to record clean audit logs and test suite passes.
   - Review diff using `code-review-and-quality` and merge following repository PR policy.

## 6. Compounding & Supply-Chain Knowledge
9. Record resolved advisories, reachability analysis findings, migration pitfalls, and package lock invariants in Section 5 of `completion-report.md`.
10. Update repository security guidelines or dependency management policies (`AGENTS.md`) with lessons learned to safeguard future upgrade cycles.
