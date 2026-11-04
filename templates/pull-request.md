# Pull Request: [PR Title]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Pull Request Description & Review  
> **Primary Owner Skill:** `code-review-and-quality`  
> **Canonical Destination Path:** `.github/pull_request_template.md` (or PR body)  
> **Status:** `<Open | In Review | Approved | Merged>`  
> **Last updated:** `<YYYY-MM-DD>`  

- **Type:** `feat` | `fix` | `refactor` | `perf` | `test` | `docs` | `chore`
- **Related Spec / Issue:** [e.g., `FEAT-001`, `ISSUE-42`]
- **Author:** [Name / Role / Agent]

---

## 1. Summary of Changes (Required)
[Provide a clear, concise bulleted summary of what was changed and why. Highlight any architectural seams or public interface modifications.]

- Change 1: [Implemented X to satisfy US-001]
- Change 2: [Added database migration for Y]
- Change 3: [Added automated integration tests]

---

## 2. Motivation & Context (Required)
[Link to the governing Feature Spec (`docs/features/<feature-id>/spec.md`) and Technical Plan (`docs/features/<feature-id>/plan.md`). Explain why this approach was taken over alternatives.]

---

## 3. Verification & Test Evidence (Required)
Evidence before assertions. List the exact commands executed and their fresh outcomes.

| Check | Command Executed | Result / Exit Code | Evidence / Logs |
|---|---|---|---|
| Unit Tests | `npm test` | Passed (14 tests) | Clean exit 0 |
| Integration Tests | `npm run test:integration` | Passed (5 tests) | DB transactions verified |
| Lint & Typecheck | `npm run lint && npm run typecheck` | Passed (0 errors) | Zero warnings |

### Terminal Verification Snippet
```text
[Paste terminal verification snippet here]
```

---

## 4. Breaking Changes & Migrations (Optional)
- [ ] Database migration included (guaranteed zero downtime)
- [ ] Environment variables or configuration changes required
- [ ] API contract changes (backward-compatible)

---

## 5. Reviewer Checklist (Required)
- [ ] Code follows project architecture, modular seams, and idiomatic standards
- [ ] Acceptance criteria from the feature spec are satisfied
- [ ] New behavioral logic is accompanied by automated tests (TDD)
- [ ] No secrets, credentials, or sensitive debugging code committed
- [ ] No test threshold or quality gate was weakened to pass CI
- **Peer Reviewer Sign-off:** [Reviewer Name / Approval Date]
