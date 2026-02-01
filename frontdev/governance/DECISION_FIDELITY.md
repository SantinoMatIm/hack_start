# Decision Fidelity Standards

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This document defines the truth constraints and grounding rules that ensure the frontend accurately represents system state, capabilities, and uncertainty. Decision fidelity is the measure of how faithfully the interface supports real decision-making.

---

## Core Principle

> **The frontend must not fabricate certainty, invent system capabilities, or obscure uncertainty.**

Every piece of information displayed must be traceable to:
- Actual system data (from API)
- Documented calculations (from heuristics)
- Explicit assumptions (logged and visible)

---

## Truth Constraints

### 1. Data Provenance

| Constraint | Requirement |
|------------|-------------|
| All displayed data must have a source | API endpoint, calculation, or documented assumption |
| Timestamps must be visible | Users must know data freshness |
| Demo data must be labeled | Never mix demo and live data without clear indication |

### 2. Uncertainty Visibility

| Data Type | Uncertainty Treatment |
|-----------|----------------------|
| Measured values (SPI) | Display as-is with measurement timestamp |
| Projections | Label as "projected" or "estimated" |
| Days to critical | Label as estimate, note methodology |
| AI-generated parameters | Show that AI selected from allowed ranges |
| Combined effects | Note penalty factors (H6: ×0.8) |

### 3. System Capability Boundaries

**The system CAN:**
- Calculate SPI from precipitation data
- Classify risk levels from SPI
- Detect trends from historical data
- Estimate days to critical threshold
- Select actions from the 15-action catalog
- Parameterize actions within defined ranges
- Project scenarios based on heuristic formulas

**The system CANNOT:**
- Invent new actions
- Create policies outside the catalog
- Predict beyond heuristic formulas
- Guarantee outcomes
- Account for all external factors

**Frontend must NOT imply capabilities the system doesn't have.**

---

## Fidelity Checklist

Use this checklist during Phase 3 Fidelity Review:

### Accuracy

- [ ] SPI value matches API response exactly
- [ ] Risk level matches API classification
- [ ] Trend indicator matches API trend
- [ ] Days to critical matches API estimate
- [ ] Action parameters match API recommendations
- [ ] Simulation results match API response

### Uncertainty Communication

- [ ] Projections labeled as estimates/projections
- [ ] Confidence levels shown where available
- [ ] Methodology accessible (expandable or linked)
- [ ] "Estimated" vs "measured" visually distinct
- [ ] AI involvement transparent

### Consequence Clarity

- [ ] No-action scenario clearly shown
- [ ] With-action scenario clearly shown
- [ ] Delta (days gained, risk reduction) prominent
- [ ] Comparison is visual, not just numeric
- [ ] User can understand what they gain/lose

### Capability Honesty

- [ ] No promises beyond system capability
- [ ] No fabricated precision
- [ ] No hidden assumptions
- [ ] Limitations accessible

---

## Anti-Patterns

### Fabricated Precision

```
Wrong: "Days to critical: 24"
Right: "Days to critical: ~24 (estimated based on current trend)"
```

### Hidden Uncertainty

```
Wrong: [Chart showing single projection line]
Right: [Chart showing projection with confidence band or range]
```

### Implied Capabilities

```
Wrong: "AI recommends the optimal action"
Right: "AI selected and parameterized from 15 available actions based on heuristics"
```

### Missing Context

```
Wrong: "Implement this action for best results"
Right: "Implementing this action is expected to add ~6 days before critical threshold"
```

---

## Decision Support Evaluation

### Key Questions

For each frontend surface, ask:

1. **Can the user make a defensible decision?**
   - Is the information complete enough?
   - Can they justify their choice to stakeholders?

2. **Can the user understand the consequences?**
   - Is the no-action path clear?
   - Is the with-action path clear?
   - Is the delta prominent?

3. **Can the user explain what they decided?**
   - Is the audit trail visible?
   - Are assumptions documented?
   - Is the methodology accessible?

4. **Can the user trust the information?**
   - Is data provenance clear?
   - Is uncertainty visible?
   - Are limitations honest?

### Decision Fidelity Score

| Score | Meaning |
|-------|---------|
| High | User can make and defend decision with confidence in the information |
| Medium | User can decide but may have questions about accuracy or completeness |
| Low | User cannot make defensible decision; information is incomplete or misleading |

Low fidelity = **Fail Phase 3 review**

---

## Profile-Specific Fidelity

### Government Users Need:

- Audit trail for public accountability
- Clear documentation of decision rationale
- Timestamps and data provenance
- Access to methodology details
- Defensible numbers for public communication

### Industry Users Need:

- Cost-benefit quantification
- ROI-relevant metrics
- Operational impact clarity
- Implementation feasibility indicators
- Board-presentable summaries

Both need truth and uncertainty; the emphasis differs.

---

## Fidelity Violations

### Detection

Signs of fidelity violations:
- Values displayed that don't match API
- Projections without uncertainty indication
- Capabilities implied that don't exist
- Assumptions not logged or visible
- Mixing demo and live data

### Resolution

1. Document the violation
2. Assess severity (Critical / Major / Minor)
3. Determine fix approach
4. Implement correction
5. Update session artifacts
6. Flag for Learning & Calibration review

### Severity Levels

| Severity | Definition | Action |
|----------|------------|--------|
| Critical | Could lead to wrong decision | Block release, immediate fix |
| Major | Misleading but not decision-altering | Fix before release |
| Minor | Suboptimal clarity | Fix in next iteration |

---

## Fidelity in Simulation

Simulation requires special attention:

### What Simulation Shows

- **No-action scenario**: Projected outcome based on current trend
- **With-action scenario**: Projected outcome with action effects applied
- **Delta**: Difference between scenarios (days gained, risk change)

### What Simulation Must Clarify

- These are projections, not guarantees
- Projections based on historical patterns and heuristic formulas
- Actual results depend on implementation effectiveness
- External factors not accounted for

### Simulation Honesty Statement

Include accessible text like:

> "Simulations project outcomes based on historical patterns and defined impact formulas. Actual results may vary based on implementation effectiveness and external factors not modeled."

---

## Documentation Requirements

### Per Session

- FIDELITY_REVIEW.md must document:
  - Checklist completion
  - Any violations found
  - Resolutions applied
  - Remaining concerns

### Per Surface

- Document data sources
- Document calculations
- Document assumptions
- Document limitations

---

*Decision fidelity is the foundation of trust. Without fidelity, the interface fails its mission.*
