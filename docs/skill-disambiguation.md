# SDLC Skill Disambiguation Guide

This document clarifies boundaries, scopes, and handoffs for skill clusters that address related domains, eliminating overlap and ensuring precise agent activation.

---

## 1. Frontend Engineering Cluster

| Skill | Primary Phase | Focus & Boundary | When to Choose |
|---|---|---|---|
| `frontend-design` | **Design / Aesthetic Direction** | Typography, distinctive visual aesthetics, color palettes, and avoiding generic AI templates. Does not write backend or state logic. | Choose when starting a new UI or redesigning visual styling and needing creative direction. |
| `frontend-ui-engineering` | **Implementation & Construction** | Production React/HTML/CSS component engineering, DOM accessibility, state management, responsive layouts, and performance. | Choose when writing, structuring, or maintaining front-end code and components. |
| `web-design-guidelines` | **Review & Acceptance Gate** | Auditing existing UI code against Web Interface Guidelines, WCAG accessibility benchmarks, touch targets, and interaction ergonomics. | Choose during code review or pre-release verification to audit UI quality. |

### Decision Flow:
```
Need creative visual style / brand identity?  ──► frontend-design
Writing / editing frontend component code?     ──► frontend-ui-engineering
Reviewing / auditing UI for UX & WCAG flaws?   ──► web-design-guidelines
```

---

## 2. Browser & Web Verification Cluster

| Skill | Primary Phase | Focus & Boundary | When to Choose |
|---|---|---|---|
| `webapp-testing` | **Automated Regression (SDET)** | Scripting, running, and maintaining Playwright end-to-end and integration test suites in CI or headless environments. | Choose when writing automated browser regression tests or verifying user flows in headless runs. |
| `browser-testing-with-devtools` | **Interactive Runtime Inspection** | Live Chrome DevTools runtime inspection via MCP: console errors, network waterfalls, DOM element inspection, CSS computed styles, and frame profiling. | Choose when actively debugging a live runtime issue, analyzing network failures, or profiling layout shifts in a real browser. |

### Decision Flow:
```
Writing scripted E2E / regression test suites? ──► webapp-testing (Playwright)
Debugging live runtime errors / inspecting DOM? ──► browser-testing-with-devtools (DevTools MCP)
```
*(Rule: Never invoke both simultaneously unless the task requires both scripted test authoring and active DevTools timeline profiling).*

---

## 3. Architecture & Codebase Design Cluster

| Skill | Scope & Granularity | Focus & Boundary | When to Choose |
|---|---|---|---|
| `software-architecture` | **Macro System Level** | System boundaries, C4 models, service topologies, data ownership, cross-cutting quality attributes, and integration contracts. | Choose when designing a new subsystem, defining service boundaries, or evaluating system-wide trade-offs. |
| `codebase-design` | **Module / Package Level** | Deep module philosophy (simple interface, powerful hidden logic), seam creation, dependency inversion, and clean internal APIs. | Choose when structuring a class, package, or module boundary within an existing service. |
| `improve-codebase-architecture` | **Diagnostics & Refactoring** | Scanning existing codebases for architectural erosion, shallow modules, leaky abstractions, and proposing progressive refactorings. | Choose when diagnosing technical debt or planning a structural refactoring campaign. |

### Decision Flow:
```
System boundaries, microservices, data ownership? ──► software-architecture
Structuring a deep, clean module or class seam?     ──► codebase-design
Auditing legacy code for architectural decay?       ──► improve-codebase-architecture
```

---

## 4. Scope Boundaries & Non-Goals

### Non-Goals (Out of Scope for this General Pack):
1. **Native Mobile Development (iOS / Android Native SDKs):**
   - The pack does not contain native Swift/Obj-C (Xcode) or Kotlin/Java (Android Studio) tool-specific skills.
   - *Alternative:* Mobile projects follow universal core skills (`spec-driven-development`, `api-and-interface-design`, `test-driven-development`, `git-workflow-and-versioning`) alongside platform-native SDK tooling.
2. **Specialized ML / Deep Learning Modeling:**
   - Training neural networks, hyperparameter optimization, and MLOps pipelines (e.g., PyTorch, Kubeflow, MLflow) are specialized domains outside this general SDLC pack.
   - *Alternative:* Data projects utilize contract-first schemas (`contracts/data-contract.json`), database design, and CI/CD automation while bringing their specialized scientific compute stack.
3. **Stack Neutrality for Interface Contracts:**
   - Interface contracts must be machine-executable. While OpenAPI, AsyncAPI, STOMP, Protobuf, and GraphQL are standard canonical templates, teams may substitute other machine-readable IDLs (e.g. Cap'n Proto, Thrift, FlatBuffers).
   - Unstructured prose markdown (such as an ad-hoc `api.md`) is prohibited because it cannot be validated by automated schema parsers or contract test fixtures.
