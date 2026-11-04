# Event Tracking Plan: [PRODUCT_OR_FEATURE_NAME]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Event Tracking Plan & Schemas  
> **Primary Owner Skill:** `analytics`  
> **Canonical Destination Path:** `docs/analytics/tracking-plan.md`  
> **Status:** `<Draft | Implemented | Verified>`  
> **Last updated:** `<YYYY-MM-DD>`  

- **Owner:** `[Data Analyst / Product Lead]`
- **Target Platforms:** `[Web / iOS / Android / Backend]`

---

## 1. Tracking Philosophy & Global Properties (Required)
All events follow the standard naming convention: `object_action` in snake_case (e.g., `checkout_started`, `button_clicked`).

### Global Context Properties (Sent with every event)
| Property | Type | Description | Example |
|---|---|---|---|
| `user_id` | String | Unique identified user ID | `"usr_12345"` |
| `session_id` | String | Session identifier | `"ses_98765"` |
| `platform` | String | Client environment | `"web"` / `"ios"` |
| `timestamp` | ISO8601 | Event generation time (UTC) | `"2026-11-04T12:00:00Z"` |

---

## 2. Event Taxonomy & Schemas (Required)

### Event: `signup_completed`
- **Description:** Triggered immediately when a new user successfully confirms their account.
- **Trigger Location:** `src/auth/signup-service.ts`

| Property | Type | Required | Description | Allowed Values |
|---|---|---|---|---|
| `auth_provider` | String | Yes | Method of signup | `email`, `google`, `github` |
| `referral_source` | String | No | Source campaign | `google_ads`, `organic`, `invite` |

### Event: `feature_used`
- **Description:** Triggered when the user interacts with the core capability.
- **Trigger Location:** `src/features/action.ts`

| Property | Type | Required | Description | Allowed Values |
|---|---|---|---|---|
| `feature_id` | String | Yes | Identifier of the feature | `"export_csv"`, `"filter_view"` |
| `duration_ms` | Number | Yes | Latency of the action | Positive integer |

---

## 3. Privacy & Governance Rules (Required)
- **Zero PII in Event Payloads:** Never pass email addresses, passwords, credit cards, or phone numbers in event properties.
- **Data Subject Rights:** All tracked events must support user pseudonymization and GDPR deletion requests.

---

## 4. Verification & Testing Checklist (Required)
- [ ] Telemetry schemas verified with automated schema validator
- [ ] Staging event dispatch confirmed via debug proxy or test telemetry endpoint
- [ ] Event volume and payload size verified to prevent client performance regressions
- **Analytics Sign-off:** [Data Lead / PM / Date]
