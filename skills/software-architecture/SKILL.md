---
name: software-architecture
description: Use when designing system boundaries, component decomposition, data ownership, or integration architecture.
license: Apache-2.0
---

# Software Architecture (pack adaptation)

Adapted for this pack from Agentic SDLC Kit's `skills/software-architecture/SKILL.md` (Apache-2.0). The procedure is intentionally adapted to the pack's artifact ownership and risk-based workflow; it is not a verbatim upstream copy.

## Inputs

- Existing repository and deployment context.
- Approved product/system requirements, constraints and important NFRs.
- Known interfaces, data stores, dependencies, runtime/operational requirements and risks.
- Explicit foundational assumptions (scale, throughput, latency, fault tolerance, tenant boundaries). Agent MUST NOT silently assume critical system parameters.

If a requirement document is absent, state the architecture drivers in prose. Never invent FR/NFR IDs or cite documents that do not exist.

## Procedure

1. Determine whether a system-level design is warranted. For a small local change, use a short technical note or no new architecture artifact if the existing design remains valid.
2. Describe system context and external actors/systems; identify trust boundaries, sensitive data and critical flows.
3. Choose architecture structure based on explicit drivers and constraints. Deconstruct the system from **first principles** (fundamental data lifecycle, state transitions, and concurrency boundaries) rather than copying generic framework scaffolding or layer-cake patterns. Apply the **Deep Modules Philosophy** (Ousterhout / Pocock / gstack):
   - Design modules that are **deep**: providing powerful, complex functionality behind a narrow, simple interface that conceals internal mechanics.
   - Maximize information hiding: keep implementation details, private data representations, and internal mechanics sealed behind module boundaries.
   - Ruthlessly eliminate **shallow modules** and pass-through layers (modules whose interface complexity approaches their implementation, or that merely map and forward calls across arbitrary layers without adding business logic).
   - Describe components/modules, responsibilities, data ownership, communication paths and deployment shape. Use C4 or equivalent diagrams when complexity merits them.
4. Evaluate important quality attributes: security/privacy, reliability, performance, scalability, operability, testability, maintainability and compatibility as relevant. Document foundational architectural assumptions explicitly (e.g., peak load, data retention, consistency models); flag unverified assumptions as critical risks requiring confirmation. Strictly forbid silent guesswork on system scale or availability parameters. Make trade-offs explicit, not generic.
5. Review integration and failure behavior: authentication/authorization, validation, retries/timeouts, idempotency, version compatibility, observability and recovery where relevant.
6. Perform a proportionate threat analysis when trust boundaries, sensitive information, external input or privileged operations are involved. STRIDE is an option, not a mandatory method for every system. Record threats, mitigations and residual risk.
7. Record consequential choices with `documentation-and-adrs` when they have real alternatives/trade-offs or are difficult to reverse. Do not create an ADR for every implementation detail.
8. Ensure API/data contracts are owned by `api-and-interface-design` when interfaces change. Detailed module/task design belongs to `detailed-design` or the feature plan, not this system overview.
9. Check that proposed architecture can be built, tested, deployed and operated within known constraints. Strictly prohibit silent guesswork: if any critical architectural decision or scale assumption is uncertain, escalate it as an explicit open decision in the architecture artifact requiring stakeholder confirmation.

## Output contract

Default path: `docs/architecture.md`, unless a repository has an existing canonical architecture document. Include only applicable sections:

- Context and drivers.
- Deep module seams and component/container responsibilities (hiding internal complexity behind narrow interfaces).
- Data ownership and external interfaces.
- Foundational architectural assumptions (scale, throughput, SLA constraints).
- Quality attributes and trade-offs.
- Security/trust boundaries and mitigation summary when applicable.
- Deployment/operational considerations.
- Links to relevant ADRs and contracts.
- Open decisions, unvalidated assumptions, and risks.

## Anti-Patterns & Shallow Architecture Traps

- **Shallow Modules & Pass-Through Bloat:** Introducing layers (Controller → Facade → Service → Repository → DAO) where each layer merely re-packages and forwards calls without adding real domain logic or information hiding.
- **Cargo-Cult Layering:** Splitting systems along generic framework tiers rather than decomposing along first-principles data lifecycles and cohesion boundaries.
- **Silent Parameter Invention:** Guessing critical operational numbers (QPS, storage volume, latency SLAs) without explicit confirmation.
- **Leaky Abstractions:** Exposing internal storage schemas or implementation types through the public interface of a module.

## Quality gate

Architecture supports the accepted requirements and quality attributes, module boundaries form deep modules (narrow interfaces, powerful hidden logic) avoiding shallow wrappers and pass-through bloat, system decomposition is grounded in first principles (data lifecycles and operational invariants), material trade-offs are recorded, interfaces and data ownership are explicit where needed, all critical architectural assumptions are explicitly recorded with zero silent guesswork by the agent on scalability or security parameters, and material risks have owners/mitigations. Specifically verify:
- Module boundaries form deep modules (narrow interfaces, substantial hidden complexity), actively avoiding shallow pass-through bloat.
- Foundational architectural assumptions are explicitly recorded; zero silent guessing on scalability, consistency, or security.
- System decomposition derives from first-principles data lifecycles, not cargo-cult scaffolding.
Do not silently modify product scope. Architecture approval is not proof that implementation meets the design.
