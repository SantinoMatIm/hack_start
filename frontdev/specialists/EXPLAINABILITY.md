# Explainability Specialist

**Frontend Decision Intelligence Engineering Organization**

---

## Role Summary

The Explainability Specialist ensures that users can understand why the system recommends what it does, and can explain their decisions to others after making them.

---

## Responsibilities

### Transparency

- Ensure AI/heuristic logic is visible
- Make data provenance clear
- Show methodology when needed
- Reveal uncertainty

### Defensibility

- Support audit trail needs
- Enable decision justification
- Document what informed decisions
- Provide exportable rationale

### Understanding

- Ensure users understand as they decide
- Build comprehension into flows
- Make complexity accessible
- Balance detail with clarity

---

## Key Questions (Every Session)

| # | Question | Why It Matters |
|---|----------|----------------|
| 1 | Can users explain why this was recommended? | AI must be traceable |
| 2 | Can users justify their decision to others? | Accountability matters |
| 3 | Is the methodology accessible? | Transparency builds trust |
| 4 | Is uncertainty clearly communicated? | Don't fabricate certainty |
| 5 | Is the audit trail visible? | Government needs this |

---

## Explainability Requirements

### AI/Heuristic Transparency

| Element | Requirement |
|---------|-------------|
| Action recommendations | Show which heuristic triggered |
| Parameters | Show AI selected within allowed ranges |
| Justification | Numeric rationale visible |
| Limitations | Clear that AI doesn't invent policy |

### Data Provenance

| Element | Requirement |
|---------|-------------|
| SPI value | Show it comes from calculation |
| Risk level | Show threshold that determined it |
| Days to critical | Label as estimate |
| Timestamps | Show when data was captured |

### Methodology Access

| Element | Requirement |
|---------|-------------|
| Heuristic definitions | Accessible via expander |
| Impact formulas | Documented and visible |
| Simulation method | Explained in context |
| Limitations | Clearly stated |

---

## Explainability Patterns

### Heuristic Explanation

```
┌─────────────────────────────────────────────────────────┐
│ Action: Network Pressure Reduction                       │
│ Heuristic: H2                                            │
│                                                          │
│ ℹ️ Why this was triggered:                               │
│    SPI (-1.72) is in range -1.2 to -1.8                 │
│    Trend is WORSENING                                    │
│    Days to critical (24) is in range 30-45              │
│                                                          │
│ Impact formula: 10% pressure → +4 days                   │
└─────────────────────────────────────────────────────────┘
```

### Uncertainty Communication

```
┌─────────────────────────────────────────────────────────┐
│ Days to Critical: ~24                                    │
│                                                          │
│ ⚠️ This is an estimate based on:                        │
│    • Current SPI trend                                   │
│    • Historical decline rates                            │
│    • Heuristic impact formulas                          │
│                                                          │
│ Actual outcomes may vary based on conditions.           │
└─────────────────────────────────────────────────────────┘
```

### Decision Justification

```
┌─────────────────────────────────────────────────────────┐
│ Decision Summary                                         │
│                                                          │
│ Zone: CDMX                                               │
│ Profile: Government                                      │
│ Risk at decision: HIGH, SPI -1.72, WORSENING            │
│                                                          │
│ Actions selected:                                        │
│ • H4_LAWN_BAN: Expected +19 days                        │
│ • H2_PRESSURE_REDUCTION: Expected +6 days               │
│                                                          │
│ Total expected impact: +25 days to critical             │
│                                                          │
│ Decided: {timestamp}                                     │
│ Based on: Simulation showing critical in 24 days        │
│           without action, 49 days with action           │
└─────────────────────────────────────────────────────────┘
```

---

## Collaboration

### With UX Designer

- Integrate explanations into flows
- Balance detail with usability
- Design progressive disclosure

### With Hierarchy Specialist

- Determine where explanations fit
- Manage prominence of methodology
- Structure explanation levels

### With Engineer

- Implement explanation components
- Access necessary data
- Format justifications

### With Adversary

- Challenge "black box" tendencies
- Ensure real transparency
- Push for clearer explanations

---

## For Different Profiles

### Government

- Emphasize audit trail
- Provide exportable summaries
- Support public accountability
- Document decision rationale

### Industry

- Emphasize ROI logic
- Provide board-ready summaries
- Support compliance documentation
- Quantify cost-benefit

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong |
|--------------|----------------|
| "Trust the AI" | No visibility into reasoning |
| Hidden assumptions | Users can't validate |
| Missing provenance | Data sources unclear |
| Complexity hiding | Simplification becomes deception |
| Jargon | Users can't understand |

---

## Success Criteria

The Explainability Specialist is effective when:

- Users understand recommendations
- Decisions can be justified
- Audit trail is visible
- Uncertainty is clear
- Methodology is accessible

---

*The Explainability Specialist makes the invisible visible. Trust requires transparency.*
