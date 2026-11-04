# SDLC Skill Pack Live Agent Benchmark Methodology

This document defines the comparative evaluation protocol for benchmarking autonomous coding agents **with** and **without** the `sdlc-skills-pack`.

---

## 1. Objectives

1. **Verify Context Discipline**: Quantify prompt tokens consumed across installation profiles (`eager-lean`, `core`, `core+web`, `full`).
2. **Evaluate Workflow Conformance**: Measure whether the agent autonomously discovers and executes the appropriate SDLC workflow (e.g. `feature-loop.md`, `bug-fix.md`) without being hand-held.
3. **Validate Artifact Ownership**: Confirm that deliverables conform to the 32 lean canonical artifact contracts without generating redundant documents.
4. **Compare Quality**: Benchmark defect escape rate, BDD acceptance criteria satisfaction, and test evidence rigor between unguided agents and pack-guided agents.

---

## 2. Benchmark Protocol: A/B Comparative Run

For each of the 11 golden task fixtures in `evals/*.json`:

### Baseline Condition (A: Control - Without Pack)
- Agent runtime starts in a clean workspace with no `sdlc-skills-pack` installed.
- Agent is given the raw task prompt (e.g. `eval-feature-loop-01`: *"Add an Idempotency-Key header to the POST /v1/payments endpoint..."*).
- System records:
  - Total prompt and completion tokens.
  - Number of tool calls.
  - Deliverables produced (does it invent `api.md`? Does it write tests before code? Does it update OpenAPI?).
  - Passing status of project test suite.

### Treatment Condition (B: Treatment - With Pack)
- Agent runtime starts with `sdlc-skills-pack` installed under appropriate profile (`eager-lean` for eager runtimes, `core` for lazy runtimes).
- Agent is given the identical task prompt.
- System records:
  - Active prompt footprint (initial startup vs per-step loading).
  - Workflow resolved by `using-sdlc-skills`.
  - Skills activated across the 5 demand-driven stages.
  - Conformance to canonical artifacts (`docs/features/<feature-id>/spec.md`, `contracts/openapi.yaml`, etc.).
  - Verification evidence in `.agent/tasks/<task-id>.md` and completion report.

---

## 3. Metrics Matrix

| Metric ID | Metric Name | Definition | Target Direction |
|---|---|---|---|
| `M-TOK` | **Token Efficiency** | Prompt tokens consumed per task step | Lower (aiming for $\le 20k$ tokens/step in eager-lean) |
| `M-STG` | **Stage Traversal** | Adherence to intake $\to$ spec $\to$ contract $\to$ TDD $\to$ verify | Higher (100% stage traversal) |
| `M-ART` | **Artifact Validity** | Conformance to canonical template schemas | 100% conformance (zero rogue prose files) |
| `M-EVI` | **Empirical Evidence** | Presence of fresh command exit codes & output before completion | Mandatory (100% verifiable) |
| `M-REG` | **Zero Regression** | Project test suite passes cleanly after completion | Mandatory (100% pass) |

---

## 4. Transcript Archiving Convention

Empirical run transcripts must be archived in `evals/results/<agent-runtime>/<fixture-id>_<model>_<timestamp>.json` following the schema documented in `evals/results/README.md`.

