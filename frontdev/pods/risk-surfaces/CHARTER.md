# Risk Surfaces Pod Charter

**Frontend Decision Intelligence Engineering Organization**

---

## Mission

Enable users to quickly and accurately understand current hydric risk state, trend, and time pressure so they can make informed decisions about whether and when to act.

---

## Scope

### Owned Decision Moments

| Decision Moment | User Question |
|-----------------|---------------|
| Risk Assessment | "How bad is it right now?" |
| Trend Understanding | "Is it getting better or worse?" |
| Time Pressure | "How much time do I have?" |
| Context Setting | "What zone and profile am I working with?" |

### Owned Surfaces

| Surface | Location | Purpose |
|---------|----------|---------|
| Risk Overview Page | `dashboard/pages/1_risk_overview.py` | Primary risk assessment |
| Risk Card Component | `dashboard/components/risk_display.py` | Risk summary display |
| SPI Gauge | `dashboard/components/risk_display.py` | Visual SPI indicator |
| Risk History Chart | `dashboard/pages/1_risk_overview.py` | Trend visualization |
| Risk Metrics Row | `dashboard/components/risk_display.py` | Key metrics display |

### Out of Scope

- Action recommendations (→ Action Surfaces Pod)
- Simulation and scenarios (→ Simulation Surfaces Pod)
- Design system tokens (→ Shared Systems Pod)
- API client (→ Shared Systems Pod)

---

## Key Principles

1. **Current State First**: Users must immediately understand where they are now
2. **Trend is Context**: Direction matters as much as current value
3. **Time Pressure is Visceral**: Days-to-critical must be felt, not just read
4. **Uncertainty Visible**: Don't fabricate precision; show estimates as estimates

---

## Quality Standards

### Must Have

- [ ] SPI value matches API exactly
- [ ] Risk level matches API classification
- [ ] Trend indicator matches API
- [ ] Days-to-critical labeled as estimate
- [ ] Risk history chart when data available
- [ ] Clear loading/error states

### Should Have

- [ ] Urgency visual escalation (GAP-001)
- [ ] Threshold proximity indicator (GAP-006)
- [ ] Confidence indicators on estimates (GAP-004)

### Could Have

- [ ] Animated urgency for critical states
- [ ] Comparison to historical baseline
- [ ] Notification trigger configuration

---

## Interfaces

### Upstream Dependencies

| Dependency | Provider | Contract |
|------------|----------|----------|
| Risk data | API `/risk/current` | Returns zone_id, spi_6m, risk_level, trend, days_to_critical |
| Risk history | API `/risk/history` | Returns historical risk snapshots |
| Session state | Shared Systems | selected_zone, selected_profile |

### Downstream Consumers

| Consumer | What They Need |
|----------|----------------|
| Action Surfaces | current_risk in session state |
| Simulation Surfaces | current_risk in session state |
| Navigation | Risk level for urgency indication |

---

## Collaboration

### Regular Touchpoints

- **With Action Surfaces**: Ensure risk context carries forward to action page
- **With Shared Systems**: Coordinate on design tokens for risk colors
- **With Accessibility**: Ensure color-blind safe risk indication

### Escalation Path

- Technical issues → Frontend Engineering Operations
- Design issues → Design Council
- Decision fidelity issues → Review Board

---

## Current State Assessment

### Strengths

- Basic risk display implemented
- Risk card with key metrics
- SPI gauge visualization
- History chart when data available

### Gaps

- No urgency escalation beyond color (GAP-001)
- No threshold proximity indicator (GAP-006)
- Point estimates without uncertainty ranges (GAP-004)
- Demo mode data could be more realistic

### Technical Debt

- CSS loading duplicated (DEBT-001)
- Demo data duplicated (DEBT-003)

---

## Pod Roadmap

### Phase 1: Foundation (Current)
- Basic risk display ✓
- Key metrics ✓
- History chart ✓

### Phase 2: Urgency Enhancement
- Implement GAP-001 (urgency escalation)
- Implement GAP-006 (threshold proximity)
- Address DDEBT-003 (risk badge consistency)

### Phase 3: Uncertainty & Confidence
- Implement GAP-004 (uncertainty visualization)
- Add confidence indicators
- Improve projection labeling

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Time to understand risk state | < 5 seconds | Unknown |
| Urgency communication clarity | Users feel time pressure | Partial |
| Accessibility compliance | WCAG AA | Needs work |

---

*The Risk Surfaces Pod owns the critical first impression: "How bad is it?"*
