# Core Frontend Principles

**Frontend Decision Intelligence Engineering Organization**

---

These principles govern all frontend work. They are not guidelines or suggestions — they are constraints that shape every decision, every component, every line of code.

---

## 1. Decision Primacy

**The frontend exists to enable defensible, timely decisions under hydric risk.**

Every UI element must pass the test: *"Does this help someone decide?"*

- If a component displays data but doesn't inform a decision, question its existence
- If a flow captures clicks but doesn't build understanding, redesign it
- If a feature is "nice to have" but doesn't serve decision-making, defer it

```
Dashboard: "Here is information."
Decision Interface: "Here is what you need to decide, and what happens if you don't."
```

We build the latter.

---

## 2. Truth Over Comfort

**Never fabricate certainty. Never obscure uncertainty.**

If the system doesn't know something, the interface must communicate that clearly.

- Projections are projections — label them as such
- Confidence intervals belong on screen, not hidden
- "Estimated" vs "Measured" must be visually distinct
- AI-generated parameters must be traceable to numeric heuristics

```
Wrong: "Days to critical: 24"
Right: "Days to critical: ~24 (estimated, based on current trend)"
```

Enterprise and government users need defensible decisions. Defensibility requires visible uncertainty.

---

## 3. Urgency Is Visual

**Time pressure must be felt, not just read.**

As risk increases and days decrease, the interface must communicate escalating urgency through progressive visual treatment.

| Condition | Visual Treatment |
|-----------|------------------|
| Days > 45 | Standard presentation |
| Days 30-45 | Elevated prominence |
| Days 15-30 | Warning state, increased visual weight |
| Days < 15 | Critical state, maximum urgency indicators |

Urgency communication includes:
- Color saturation and hue shifts
- Size and weight changes
- Animation and motion (respecting accessibility)
- Spatial prominence

A user should *feel* the difference between 45 days and 15 days before reading the number.

---

## 4. Consequences Before Features

**Act vs not-act must be viscerally clear.**

Users should understand what they lose by waiting, not just what they gain by acting.

- Every action recommendation must show expected impact
- Simulation must contrast futures, not just display projections
- "Cost of inaction" should be as prominent as "benefit of action"

```
Weak: "Recommended action: Pressure reduction (+4 days)"
Strong: "Without action: Critical in 24 days. With action: Critical in 52 days. You gain 28 days."
```

Decisions are made when consequences are understood.

---

## 5. Explainable Over Magical

**Every recommendation must be traceable to numeric heuristics.**

The AI orchestrator parameterizes; it does not invent policy.

- All 15 actions come from a fixed catalog
- All heuristics have defined trigger conditions
- All impact formulas are documented and auditable
- No black boxes in the decision path

Users must be able to answer: *"Why is the system recommending this?"* with specific numbers.

---

## 6. Accessibility Is Non-Negotiable

**Decision-makers under stress have degraded capabilities.**

Crisis conditions affect:
- Attention span
- Color perception (stress, fatigue)
- Fine motor control
- Cognitive load capacity

Requirements:
- WCAG AA minimum, AAA where feasible
- Color-blind safe urgency indicators
- Reduced motion alternatives
- Clear focus states
- Screen reader compatibility

The interface must work for users who are exhausted, stressed, and under pressure.

---

## 7. No Dashboard Theater

**Dashboards display. Decision interfaces compel.**

This organization builds the latter.

Warning signs of dashboard theater:
- Beautiful visualizations that don't drive action
- Data density without decision clarity
- Charts that impress but don't inform
- Metrics without context or thresholds

If a surface doesn't change behavior, question its existence.

---

## 8. Skepticism As Process

**The Adversary role exists to challenge weak thinking.**

- Dissent is logged, not suppressed
- "Easy consensus" is a warning sign
- Comfortable decisions should be uncomfortable to reach
- Every major choice should survive devil's advocate review

Healthy process:
1. Proposal made
2. Adversary challenges
3. Debate logged
4. Decision strengthened or revised
5. Rationale documented

---

## 9. Profile Differentiation Is Real

**Government and Industry users have different mental models.**

| Aspect | Government | Industry |
|--------|------------|----------|
| Priority | Impact + Urgency | Impact + Cost |
| Accountability | Public welfare | Shareholder value |
| Decision Mode | Defensible to citizens | Defensible to board |
| Key Anxiety | Political fallout | Operational disruption |

The same data may require different presentation, hierarchy, and emphasis.

---

## 10. Code Is The Artifact

**Markdown explains. Code implements.**

- Session artifacts document *why*
- Code is *what* actually gets deployed
- No amount of documentation compensates for bad code
- No amount of good code excuses missing documentation

Both are required. Neither is sufficient alone.

---

## Principle Violations

When a principle is violated:

1. Log the violation in the session's DEBATE_LOG.md
2. Document the rationale for the exception
3. Flag for Learning & Calibration review
4. Consider whether the principle needs amendment

Principles evolve through deliberate process, not silent drift.

---

## Principle Hierarchy

When principles conflict:

1. **Decision Primacy** takes precedence — if it doesn't serve decisions, other principles are moot
2. **Truth Over Comfort** and **Accessibility** cannot be traded against features
3. **Profile Differentiation** may override presentation choices
4. **Skepticism** applies to principle interpretation itself

---

*These principles are living constraints. They may be amended through governance process, but never ignored.*
