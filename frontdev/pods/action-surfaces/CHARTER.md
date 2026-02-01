# Action Surfaces Pod Charter

**Frontend Decision Intelligence Engineering Organization**

---

## Mission

Enable users to understand, evaluate, and select recommended actions based on current risk conditions, user profile, and heuristic-driven AI parameterization.

---

## Scope

### Owned Decision Moments

| Decision Moment | User Question |
|-----------------|---------------|
| Action Understanding | "What actions are available?" |
| Recommendation Evaluation | "Why is this action recommended?" |
| Parameter Understanding | "What are the specific parameters?" |
| Selection for Simulation | "Which actions do I want to simulate?" |

### Owned Surfaces

| Surface | Location | Purpose |
|---------|----------|---------|
| Actions Page | `dashboard/pages/2_actions.py` | Primary actions display |
| Action Card Component | `dashboard/components/action_card.py` | Individual action display |
| Action List | `dashboard/components/action_card.py` | Action collection display |
| Heuristic Explanations | `dashboard/components/action_card.py` | H1-H6 explanations |

### Out of Scope

- Risk assessment display (→ Risk Surfaces Pod)
- Simulation execution and results (→ Simulation Surfaces Pod)
- Design system tokens (→ Shared Systems Pod)

---

## Key Principles

1. **Explainability First**: Every recommendation must show why it was selected
2. **Parameters Visible**: All parameterization decisions must be transparent
3. **Selection is Active**: Users must consciously choose actions for simulation
4. **Heuristics Are Traceable**: Users can understand the rule that triggered the action

---

## Quality Standards

### Must Have

- [ ] All recommended actions displayed with parameters
- [ ] Justification text for each action
- [ ] Expected effect shown (days gained)
- [ ] Heuristic reference (H1-H6)
- [ ] Selection mechanism for simulation
- [ ] Profile context displayed

### Should Have

- [ ] Priority ranking visualization
- [ ] Cost indicators (for Industry profile)
- [ ] Implementation complexity indicator
- [ ] Expandable heuristic explanations

### Could Have

- [ ] Action comparison mode
- [ ] Historical action effectiveness
- [ ] Alternative parameter suggestions

---

## Interfaces

### Upstream Dependencies

| Dependency | Provider | Contract |
|------------|----------|----------|
| Recommended actions | API `/actions/recommended` | Returns prioritized, parameterized actions |
| Current risk | Risk Surfaces Pod | session_state.current_risk |
| Zone/Profile | Shared Systems | session_state.selected_zone, selected_profile |

### Downstream Consumers

| Consumer | What They Need |
|----------|----------------|
| Simulation Surfaces | session_state.selected_actions (list of action codes) |

---

## Collaboration

### Regular Touchpoints

- **With Risk Surfaces**: Ensure risk context is displayed on actions page
- **With Simulation Surfaces**: Coordinate on action selection handoff
- **With Shared Systems**: Coordinate on card component patterns

### Escalation Path

- Technical issues → Frontend Engineering Operations
- Design issues → Design Council
- Heuristic clarity issues → Core Council (involves backend)

---

## Current State Assessment

### Strengths

- Action cards display key information
- Heuristic explanations available via expander
- Selection mechanism exists
- Profile context shown

### Gaps

- Priority visualization could be stronger
- No cost indicators for Industry profile
- Selection UX has friction (small checkboxes)
- No comparison mode for similar actions

### Technical Debt

- Demo data duplicated (DEBT-003)
- Action card checkbox position (DDEBT-002)

---

## Action Card Anatomy

```
┌─────────────────────────────────────────────────────────────┐
│ ☐ [Checkbox]                                                │
├─────────────────────────────────────────────────────────────┤
│ ┌──────────┐                                                │
│ │  HIGH    │  ← Priority badge                             │
│ └──────────┘                                                │
│                                                              │
│ Network Pressure Reduction                    ← Title        │
│ H2_PRESSURE_REDUCTION                         ← Code        │
│                                                              │
│ Parameters:                                   ← Section      │
│ • Reduction: 15%                                             │
│ • Duration: 30 days                                          │
│ • Priority Level: HIGH                                       │
│                                                              │
│ Expected Effect: +6 days to critical          ← Impact       │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Justification: SPI in range -1.2 to -1.8, worsening    │ │
│ │ conditions warrant pressure management per H2.          │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                              │
│ [ℹ️ About H2 Heuristic]                      ← Expander     │
└─────────────────────────────────────────────────────────────┘
```

---

## Pod Roadmap

### Phase 1: Foundation (Current)
- Action cards ✓
- Selection mechanism ✓
- Heuristic explanations ✓

### Phase 2: Selection UX
- Improve checkbox integration
- Add select all / clear all
- Better visual feedback on selection

### Phase 3: Profile-Specific Enhancements
- Cost indicators for Industry
- Urgency indicators for Government
- Implementation timeline estimates

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Action understanding | User can explain why action is recommended | Partial |
| Selection completion | Users complete selection for simulation | Unknown |
| Parameter visibility | All parameters visible without extra clicks | Yes |

---

*The Action Surfaces Pod owns the "what can I do?" moment.*
