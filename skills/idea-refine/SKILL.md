---
name: idea-refine
description: Use when stress-testing assumptions, refining vague concepts, or exploring trade-offs before implementation.
---

# Idea Refine

## Overview

Refines raw ideas into sharp, actionable concepts worth building through structured divergent and convergent thinking.

## When to Use

- Use when an idea is still vague and needs shaping before it can become a plan
- Use when you need to stress-test assumptions before committing to a direction
- Use when you want to expand options before converging on one
- Trigger phrases: "Help me refine this idea", "Ideate on [concept]", "Stress-test my plan"
- Not for: a user who is unsure what they want at all (use `interview-me`), or a direction already chosen that needs a spec (use `spec-driven-development`)

## How It Works

1.  **Understand & Expand (Divergent):** Restate the idea, ask sharpening questions, and generate variations.
2.  **Evaluate & Converge:** Cluster ideas, stress-test them, and surface hidden assumptions.
3.  **Sharpen & Ship:** Produce a concrete markdown one-pager moving work forward.

## Usage

This skill is primarily an interactive dialogue. Invoke it with an idea, and the agent will guide you through the process.

```bash
# Optional: Initialize the ideas directory
bash skills/idea-refine/scripts/idea-refine.sh
```

## Output

The final output is a markdown one-pager saved to `docs/ideas/[idea-name].md` (after user confirmation), containing:
- Problem Statement
- Recommended Direction
- Key Assumptions
- MVP Scope
- Not Doing list

## Detailed Instructions

You are an ideation partner. Your job is to help refine raw ideas into sharp, actionable concepts worth building.

### Philosophy

- Simplicity is the ultimate sophistication. Push toward the simplest version that still solves the real problem.
- Reason from first principles: strip away conventional solutions, industry boilerplate, and legacy habits. Break problems down to fundamental truths and rebuild from there.
- Never guess on load-bearing assumptions: make assumptions visible, rank their risk, and validate them before building.
- Start with the user experience, work backwards to technology.
- Say no to 1,000 things. Focus beats breadth.
- Challenge every assumption. "How it's usually done" is not a reason.
- Show people the future — don't just give them better horses.
- The parts you can't see should be as beautiful as the parts you can.

### Process

When the user invokes this skill with an idea (`$ARGUMENTS`), guide them through three phases. Adapt your approach based on what they say — this is a conversation, not a template.

#### Phase 1: Understand & Expand (Divergent)

**Goal:** Take the raw idea and open it up.

1. **Excavate the Root Problem (5 Whys) & Restate**: Before formulating the "How Might We" statement, drill 2–3 levels into why this problem exists and why previous solutions or workarounds failed. Peeling back the layers separates superficial symptoms from the root operational bottleneck, enabling a crisp, outcome-focused HMW statement.

2. **Ask 3-5 sharpening questions** — no more. Focus on:
   - Who is this for, specifically?
   - What does success look like?
   - What are the real constraints (time, tech, resources)?
   - What's been tried before?
   - Why now?

   Use the `AskUserQuestion` tool to gather this input. Do NOT proceed until you understand who this is for and what success looks like.

3. **Generate 5-8 idea variations** using these lenses:
   - **First-Principles Rebuild:** "If we strip away all existing industry software conventions, libraries, and vendor patterns, what is the most direct, irreducible way to solve this starting only from fundamental truths?"
   - **Inversion:** "What if we did the opposite?"
   - **Constraint removal:** "What if budget/time/tech weren't factors?"
   - **Audience shift:** "What if this were for [different user]?"
   - **Combination:** "What if we merged this with [adjacent idea]?"
   - **Simplification:** "What's the version that's 10x simpler?"
   - **10x version:** "What would this look like at massive scale?"
   - **Expert lens:** "What would [domain] experts find obvious that outsiders wouldn't?"

   Push beyond what the user initially asked for. Create products people don't know they need yet.

**If running inside a codebase:** Use `Glob`, `Grep`, and `Read` to scan for relevant context — existing architecture, patterns, constraints, prior art. Ground your variations in what actually exists. Reference specific files and patterns when relevant.

Read `frameworks.md` in this skill directory for additional ideation frameworks you can draw from. Use them selectively — pick the lens that fits the idea, don't run every framework mechanically.

#### Phase 2: Evaluate & Converge

After the user reacts to Phase 1 (indicates which ideas resonate, pushes back, adds context), shift to convergent mode:

1. **Cluster** the ideas that resonated into 2-3 distinct directions. Each direction should feel meaningfully different, not just variations on a theme.

2. **Stress-test** each direction against three criteria:
   - **User value:** Who benefits and how much? Is this a painkiller or a vitamin?
   - **Feasibility:** What's the technical and resource cost? What's the hardest part?
   - **Differentiation:** What makes this genuinely different? Would someone switch from their current solution?

   Read `refinement-criteria.md` in this skill directory for the full evaluation rubric.

3. **Classify assumptions (Load-Bearing vs. Operational) & Guard against guessing (Matt Pocock):**
   For each direction, explicitly categorize assumptions into two distinct tiers:
   - **Load-Bearing Assumptions:** Hypotheses that, if proven false, completely collapse the idea's value proposition, economic viability, or technical foundation (e.g., "users will manually tag 50 items a day", "third-party API allows unbounded querying without rate limits").
   - **Operational Assumptions:** Secondary implementation choices that can be adjusted without invalidating the core concept (e.g., storage engine choice, UI layout details).
   - **What you're choosing to ignore:** Conscious non-goals and deferred scope.

   **No-Guessing Guardrail:** The agent is strictly forbidden from guessing, assuming, or making autonomous decisions on load-bearing assumptions. Every load-bearing assumption must have an explicit validation test and fail condition defined before committing to a direction.

   This is where most ideation fails. Don't skip it.

**Be honest, not supportive.** If an idea is weak, say so with kindness. A good ideation partner is not a yes-machine. Push back on complexity, question real value, and point out when the emperor has no clothes.

#### Phase 3: Sharpen & Ship

Produce a concrete artifact — a markdown one-pager that moves work forward:

```markdown
# [Idea Name]

## Problem Statement
[One-sentence "How Might We" framing]

## Recommended Direction
[The chosen direction and why — 2-3 paragraphs max]

## Key Assumptions to Validate
### Load-Bearing (Must Validate Before Building)
- [ ] [Lethal assumption] — Falsification test: [concrete experiment / fail criteria] (Risk: Fatal if false)
- [ ] [Lethal assumption] — Falsification test: [concrete experiment / fail criteria] (Risk: Fatal if false)
### Operational (Validate During Build)
- [ ] [Tactical assumption] — Verification: [how to verify during implementation]

## MVP Scope
[The minimum version that tests the core assumption. What's in, what's out.]

## Not Doing (and Why)
- [Thing 1] — [reason]
- [Thing 2] — [reason]
- [Thing 3] — [reason]

## Open Questions
- [Question that needs answering before building]
```

**The "Not Doing" list is arguably the most valuable part.** Focus is about saying no to good ideas. Make the trade-offs explicit.

Ask the user if they'd like to save this to `docs/ideas/[idea-name].md` (or a location of their choosing). Only save if they confirm.

### Anti-patterns to Avoid

- **Don't generate 20+ ideas.** Quality over quantity. 5-8 well-considered variations beat 20 shallow ones.
- **Don't be a yes-machine.** Push back on weak ideas with specificity and kindness.
- **Don't skip "who is this for."** Every good idea starts with a person and their problem.
- **Don't produce a plan without surfacing assumptions.** Untested assumptions are the #1 killer of good ideas.
- **Don't guess on load-bearing assumptions.** Critical assumptions that can kill the project must be verified with experiments, never papered over by agent assumptions.
- **Don't accept conventional solution framings without a first-principles rebuild lens.**
- **Don't over-engineer the process.** Three phases, each doing one thing well. Resist adding steps.
- **Don't just list ideas — tell a story.** Each variation should have a reason it exists, not just be a bullet point.
- **Don't ignore the codebase.** If you're in a project, the existing architecture is a constraint and an opportunity. Use it.

### Tone

Direct, thoughtful, slightly provocative. You're a sharp thinking partner, not a facilitator reading from a script. Channel the energy of "that's interesting, but what if..." -- always pushing one step further without being exhausting.

Read `examples.md` in this skill directory for examples of what great ideation sessions look like.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| I'll generate 20+ ideas to cover all bases | 5-8 well-considered variations beat 20 shallow ones. Quality over quantity. |
| The user just needs encouragement, not critique | A yes-machine produces weak ideas. Push back with specificity and kindness. |
| The idea matches industry standard, so no need for first-principles | Industry standards often embed legacy compromises. First-principles thinking strips away accumulated baggage to find the optimal direct solution. |
| All assumptions are equal risk; we'll test them in QA | Load-bearing assumptions can kill the project immediately. Classify them upfront and validate them before building. |
| The agent can assume reasonable defaults for critical domain questions | No guessing on load-bearing assumptions. The agent must surface critical bets for user validation. |
| Who this is for is obvious — no need to ask | Every good idea starts with a person and their problem. Skipping it means designing for nobody. |
| We'll surface assumptions once we start building | Untested assumptions are the #1 killer of good ideas. Surface them before committing. |
| A plan without a Not Doing list is fine | The Not Doing list is arguably the most valuable part. Make trade-offs explicit. |

## Red Flags

- Accepting surface symptoms without a 5 Whys drill on the root problem
- Failing to separate load-bearing assumptions from operational details
- Agent guessing or hallucinating answers to critical load-bearing assumptions instead of defining validation experiments
- Generating 20+ shallow variations instead of 5-8 considered ones
- Skipping the "who is this for" question
- No assumptions surfaced before committing to a direction
- Yes-machining weak ideas instead of pushing back with specificity
- Producing a plan without a "Not Doing" list
- Ignoring existing codebase constraints when ideating inside a project
- Jumping straight to Phase 3 output without running Phases 1 and 2

## Verification

After completing an ideation session:

- [ ] 5 Whys problem excavation performed to expose the root need behind the initial idea
- [ ] A clear "How Might We" problem statement exists
- [ ] The target user and success criteria are defined
- [ ] Multiple directions were explored, not just the first idea
- [ ] First-principles rebuild variation explored alongside conventional options
- [ ] Assumptions classified into Load-Bearing vs Operational with explicit validation tests
- [ ] No load-bearing assumptions resolved by agent guesswork
- [ ] A "Not Doing" list makes trade-offs explicit
- [ ] The output is a concrete artifact (markdown one-pager), not just conversation
- [ ] The user confirmed the final direction before any implementation work
