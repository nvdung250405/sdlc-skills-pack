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

If a requirement document is absent, state the architecture drivers in prose. Never invent FR/NFR IDs or cite documents that do not exist.

## Procedure

1. Determine whether a system-level design is warranted. For a small local change, use a short technical note or no new architecture artifact if the existing design remains valid.
2. Describe system context and external actors/systems; identify trust boundaries, sensitive data and critical flows.
3. Choose architecture structure based on explicit drivers and constraints. Describe components/modules, responsibilities, data ownership, communication paths and deployment shape to the level useful for implementation and review. Use C4 or equivalent diagrams when complexity merits them.
4. Evaluate important quality attributes: security/privacy, reliability, performance, scalability, operability, testability, maintainability and compatibility as relevant. Make trade-offs explicit, not generic.
5. Review integration and failure behavior: authentication/authorization, validation, retries/timeouts, idempotency, version compatibility, observability and recovery where relevant.
6. Perform a proportionate threat analysis when trust boundaries, sensitive information, external input or privileged operations are involved. STRIDE is an option, not a mandatory method for every system. Record threats, mitigations and residual risk.
7. Record consequential choices with `documentation-and-adrs` when they have real alternatives/trade-offs or are difficult to reverse. Do not create an ADR for every implementation detail.
8. Ensure API/data contracts are owned by `api-and-interface-design` when interfaces change. Detailed module/task design belongs to `detailed-design` or the feature plan, not this system overview.
9. Check that proposed architecture can be built, tested, deployed and operated within known constraints. Flag uncertainty requiring stakeholder/architect decision.

## Output contract

Default path: `docs/architecture.md`, unless a repository has an existing canonical architecture document. Include only applicable sections:

- Context and drivers.
- Component/container/module responsibilities and key flows.
- Data ownership and external interfaces.
- Quality attributes and trade-offs.
- Security/trust boundaries and mitigation summary when applicable.
- Deployment/operational considerations.
- Links to relevant ADRs and contracts.
- Open decisions and risks.

## Quality gate

Architecture supports the accepted requirements and quality attributes, responsibilities and boundaries are understandable, material trade-offs are recorded, interfaces and data ownership are explicit where needed, and material risks have owners/mitigations. Do not silently modify product scope. Architecture approval is not proof that implementation meets the design.

## Environment Integration

> [!TIP]
> On completion: finish with `verification-before-completion` to confirm any generated artifacts meet acceptance criteria, then `task-handoff` to persist state across sessions.
