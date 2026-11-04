# ADR-NNN: [Decision Title]

> **Document type:** Canonical Artifact Contract  
> **Artifact:** Architecture Decision Record (ADR)  
> **Primary Owner Skill:** `documentation-and-adrs`  
> **Canonical Destination Path:** `docs/adr/ADR-NNN-[slug].md`  
> **Status:** `<Proposed | Accepted | Superseded | Rejected>`  
> **Last updated:** `<YYYY-MM-DD>`  

---

## 1. Context & Problem Framing (Required)
- **Decision Owners:** [Architect / Tech Lead / Specialist]
- **Related Requirements / Features:** [FR/NFR/FEAT IDs or user stories]

[Describe the context, technical problem, and constraints driving this decision. What forces are at play?]

---

## 2. Decision Drivers & Quality Attributes (Required)
- [Driver 1: e.g., Sub-50ms query latency under 10k RPS]
- [Driver 2: e.g., Multi-region active-active database replication]
- [Driver 3: e.g., Zero vendor lock-in on proprietary cloud services]

---

## 3. Options Considered (Required)

### Option A — [Name / Technology]
- **Benefits:** [Pros, strengths, alignment with team skills]
- **Costs & Risks:** [Cons, operational overhead, license costs]

### Option B — [Name / Technology]
- **Benefits:** [Pros, strengths]
- **Costs & Risks:** [Cons, trade-offs]

---

## 4. Chosen Decision (Required)
[State clearly the chosen option and the technical rationale explaining why it best satisfies the decision drivers over the alternatives.]

---

## 5. Consequences & Impact (Required)
- **Positive Impacts:** [What becomes easier, faster, or safer?]
- **Negative Impacts & Trade-offs:** [What compromises or complexities are accepted?]
- **Security & Reliability Implications:** [Impact on trust boundaries, failover, backup]
- **Operational & Migration Implications:** [Changes to tooling, deployment, team training]
- **Cost & Financial Governance (FinOps):** [Estimated infrastructure/cloud spend impact, token budgeting considerations]

---

## 6. Validation, Revisit Conditions & Review Gate (Required)
- **Empirical Validation Plan:** [How will this decision be verified in practice? e.g. PoC benchmark, load test]
- **Revisit Triggers:** [Explicit conditions that will trigger re-evaluation, e.g. traffic exceeds 100k RPS]

### ADR Review Gate
- [ ] Context clearly states the problem without biasing toward a pre-selected solution
- [ ] At least two realistic options were evaluated with objective trade-offs
- [ ] Consequences (positive, negative, operational, and cost) are fully articulated
- [ ] Decision recorded and approved by architectural stakeholders
