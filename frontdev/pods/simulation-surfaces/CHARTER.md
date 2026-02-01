# Simulation Surfaces Pod Charter

**Frontend Decision Intelligence Engineering Organization**

---

## Mission

Enable users to compare the consequences of action vs inaction through clear scenario simulation, supporting the final decision to act.

---

## Scope

### Owned Decision Moments

| Decision Moment | User Question |
|-----------------|---------------|
| Scenario Comparison | "What happens if I act vs don't act?" |
| Impact Quantification | "How much do I gain by acting?" |
| Decision Confirmation | "Am I ready to commit to these actions?" |
| Outcome Understanding | "What specifically will change?" |

### Owned Surfaces

| Surface | Location | Purpose |
|---------|----------|---------|
| Simulation Page | `dashboard/pages/3_simulation.py` | Primary simulation display |
| Comparison Cards | `dashboard/components/simulation_chart.py` | Act vs not-act comparison |
| Projection Chart | `dashboard/components/simulation_chart.py` | Timeline projection |
| Impact Breakdown | `dashboard/components/simulation_chart.py` | Per-action impact |
| Decision Summary | `dashboard/components/simulation_chart.py` | Final decision CTA |

### Out of Scope

- Risk assessment (→ Risk Surfaces Pod)
- Action selection (→ Action Surfaces Pod)
- Design system tokens (→ Shared Systems Pod)

---

## Key Principles

1. **Consequences Are Central**: The difference between acting and not acting must be visceral
2. **Uncertainty Acknowledged**: Projections are projections; label them as such
3. **Decision Is Real**: The confirmation moment is significant, not a checkbox
4. **Impact Is Traceable**: Per-action contribution to total effect is visible

---

## Quality Standards

### Must Have

- [ ] No-action scenario clearly displayed
- [ ] With-action scenario clearly displayed
- [ ] Delta prominently shown (days gained)
- [ ] Projection chart showing timeline
- [ ] Per-action impact breakdown
- [ ] Decision confirmation mechanism

### Should Have

- [ ] Confidence indicators on projections (GAP-004)
- [ ] "Cost of inaction" framing (GAP-002)
- [ ] Methodology explanation accessible
- [ ] Re-run simulation option

### Could Have

- [ ] Decision audit log (GAP-003)
- [ ] Historical projection accuracy
- [ ] Export simulation results

---

## Interfaces

### Upstream Dependencies

| Dependency | Provider | Contract |
|------------|----------|----------|
| Simulation results | API `/scenarios/simulate` | Returns scenarios and deltas |
| Selected actions | Action Surfaces | session_state.selected_actions |
| Current risk | Risk Surfaces | session_state.current_risk |
| Zone/Profile | Shared Systems | session_state.selected_zone, selected_profile |

### Downstream Consumers

| Consumer | What They Need |
|----------|----------------|
| Decision Log (future) | Confirmed decisions for audit trail |

---

## Collaboration

### Regular Touchpoints

- **With Action Surfaces**: Coordinate on selected_actions handoff
- **With Risk Surfaces**: Ensure current_risk context is displayed
- **With Shared Systems**: Coordinate on comparison layout patterns

### Escalation Path

- Projection accuracy questions → Backend team
- Design of comparison → Design Council
- Decision confirmation UX → Core Council

---

## Comparison Layout

```
┌─────────────────────────────────┐ ┌─────────────────────────────────┐
│  NO ACTION                      │ │  WITH ACTION                    │
│  ───────────────────────        │ │  ────────────────────────       │
│                                 │ │                                 │
│  Projected SPI: -2.12           │ │  Projected SPI: -1.87           │
│                                 │ │                                 │
│  Risk Level: CRITICAL           │ │  Risk Level: HIGH               │
│                                 │ │                                 │
│  Days to Critical: 24           │ │  Days to Critical: 52           │
│                                 │ │                                 │
│  ┌───────────────────────────┐  │ │  ┌───────────────────────────┐  │
│  │ Without intervention,     │  │ │  │ With selected actions,    │  │
│  │ conditions deteriorate    │  │ │  │ critical threshold is     │  │
│  │ to critical levels.       │  │ │  │ extended significantly.   │  │
│  └───────────────────────────┘  │ │  └───────────────────────────┘  │
│                                 │ │                                 │
│  Light background               │ │  Dark background + DELTA: +28   │
└─────────────────────────────────┘ └─────────────────────────────────┘
```

---

## Current State Assessment

### Strengths

- Comparison cards implemented
- Projection chart available
- Impact breakdown per action
- Decision confirmation exists

### Gaps

- No uncertainty visualization (GAP-004)
- "Cost of inaction" not framed strongly (GAP-002)
- No persistent decision log (GAP-003)
- Decision confirmation feels light (balloons)

### Technical Debt

- Demo data duplicated (DEBT-003)
- Empty state could be stronger (DDEBT-004)

---

## Pod Roadmap

### Phase 1: Foundation (Current)
- Comparison layout ✓
- Projection chart ✓
- Impact breakdown ✓
- Confirmation ✓

### Phase 2: Consequence Emphasis
- Stronger "cost of inaction" framing
- Visual urgency in no-action scenario
- Improved decision confirmation UX

### Phase 3: Fidelity Enhancement
- Uncertainty bands on projections
- Confidence indicators
- Methodology accessibility

### Phase 4: Accountability
- Decision audit log
- Export capability
- Historical tracking

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Consequence clarity | User can articulate what they gain/lose | Partial |
| Decision confidence | User feels informed when confirming | Unknown |
| Projection transparency | User knows projections are estimates | Needs work |

---

*The Simulation Surfaces Pod owns the moment of decision.*
