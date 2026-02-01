# Known Gaps

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This document tracks identified gaps in the frontend — missing surfaces, features, or capabilities that would materially improve decision-making. Gaps are logged for prioritization and eventual resolution.

---

## Gap Format

```
## GAP-{number}: {Title}

**Identified**: YYYY-MM-DD
**Status**: Identified | In Progress | Resolved | Deferred
**Severity**: Critical | Major | Minor
**Affects**: [User profiles, decision contexts affected]

**Current State**: [What exists now]
**Gap Description**: [What's missing]
**Decision Impact**: [How this affects decision-making]
**Proposed Resolution**: [How to address]
**Session**: [Session ID if being worked, or "Backlog"]
```

---

## Active Gaps

### GAP-001: Urgency Visual Escalation

**Identified**: 2026-01-31
**Status**: Identified
**Severity**: Major
**Affects**: All users, especially in high-risk situations

**Current State**: 
Days-to-critical is shown as a number with risk-level color. The visual treatment is static regardless of urgency level.

**Gap Description**:
As time to critical decreases, there is no progressive visual escalation beyond color change. Users must read and interpret the number rather than feeling the urgency.

**Decision Impact**:
- Users may not perceive escalating urgency
- Critical situations may not feel critical
- Violates "Urgency Is Visual" principle

**Proposed Resolution**:
1. Define urgency tiers (>45, 30-45, 15-30, <15 days)
2. Implement progressive visual treatment:
   - Size increase
   - Animation (with reduced-motion alternative)
   - Visual weight escalation
3. Ensure accessibility compliance

**Session**: Backlog

---

### GAP-002: Cost of Inaction Visibility

**Identified**: 2026-01-31
**Status**: Identified
**Severity**: Major
**Affects**: All users, especially government (accountability)

**Current State**:
Simulation shows two scenarios side-by-side, but "what you lose by waiting" is not prominently displayed.

**Gap Description**:
Users see projected outcomes but not the accumulating cost of delay. No indicator shows "each day you wait costs X."

**Decision Impact**:
- Consequence of inaction is implicit, not explicit
- May reduce decision urgency
- Violates "Consequences Before Features" principle

**Proposed Resolution**:
1. Add "cost of inaction" indicator
2. Show daily/weekly impact of delay
3. Consider economic or population impact quantification
4. Make visible on actions and simulation pages

**Session**: Backlog

---

### GAP-003: Decision Audit Trail

**Identified**: 2026-01-31
**Status**: Identified
**Severity**: Major
**Affects**: Government users (primary), Industry (secondary)

**Current State**:
"Confirm Decision" button shows success message and balloons. No persistent record is visible to the user.

**Gap Description**:
Users cannot see a history of decisions made, by whom, when, based on what data. No accountability surface exists.

**Decision Impact**:
- Government users cannot demonstrate decision trail to stakeholders
- No institutional memory of actions taken
- Audit requirements unmet

**Proposed Resolution**:
1. Create decision log surface
2. Record: decision, timestamp, user, zone, risk context, actions selected
3. Make accessible from main navigation
4. Consider export functionality

**Session**: Backlog

---

### GAP-004: Uncertainty Visualization

**Identified**: 2026-01-31
**Status**: Identified
**Severity**: Major
**Affects**: All users

**Current State**:
Single point values displayed (SPI: -1.72, Days: 24). No confidence intervals or uncertainty ranges shown.

**Gap Description**:
Users see precision that may not reflect actual confidence. Projections appear certain when they are estimates.

**Decision Impact**:
- May create false confidence
- Violates "Truth Over Comfort" principle
- Defensibility of decisions reduced

**Proposed Resolution**:
1. Add confidence indicators to projections
2. Show ranges where applicable (e.g., "20-28 days")
3. Visual uncertainty treatment (bands on charts)
4. Clear "estimated" vs "measured" labeling

**Session**: Backlog

---

### GAP-005: Multi-Zone Comparison

**Identified**: 2026-01-31
**Status**: Identified
**Severity**: Minor
**Affects**: Users managing multiple zones

**Current State**:
Single zone selected at a time. No way to compare zones for resource allocation decisions.

**Gap Description**:
Users with responsibility for multiple zones cannot easily compare risk levels and prioritize.

**Decision Impact**:
- Resource allocation decisions harder
- Must context-switch between zones
- Portfolio view missing

**Proposed Resolution**:
1. Add zone comparison surface
2. Show key metrics side-by-side
3. Priority ranking indicator
4. Enable cross-zone action recommendations

**Session**: Backlog

---

### GAP-006: Escalation Threshold Visibility

**Identified**: 2026-01-31
**Status**: Identified
**Severity**: Minor
**Affects**: All users

**Current State**:
Risk levels shown (LOW, MEDIUM, HIGH, CRITICAL) but no indication of how close to the next level.

**Gap Description**:
Users don't know how close they are to escalation (e.g., SPI is -1.45, HIGH threshold is -1.5).

**Decision Impact**:
- Threshold crossings may be surprising
- Proactive intervention harder to plan
- "Distance to next level" not visible

**Proposed Resolution**:
1. Show threshold proximity indicator
2. Visual "distance to escalation" display
3. Consider notification configuration for threshold crossings

**Session**: Backlog

---

## Resolved Gaps

*None yet. Gaps that are resolved will be moved here with resolution details.*

---

## Deferred Gaps

*Gaps that are acknowledged but intentionally deferred will be listed here with rationale.*

---

## Gap Prioritization

### Priority Matrix

| Severity | Decision Impact | Priority |
|----------|-----------------|----------|
| Critical | Blocks decisions | P0 — Immediate |
| Major | Degrades decisions | P1 — Next session |
| Minor | Inconvenient | P2 — Backlog |

### Current Priority Order

1. GAP-001: Urgency Visual Escalation (Major)
2. GAP-002: Cost of Inaction Visibility (Major)
3. GAP-003: Decision Audit Trail (Major)
4. GAP-004: Uncertainty Visualization (Major)
5. GAP-005: Multi-Zone Comparison (Minor)
6. GAP-006: Escalation Threshold Visibility (Minor)

---

## How to Add a Gap

1. Assign next sequential number
2. Fill out all sections
3. Determine severity and priority
4. Add to backlog or assign to session
5. Update this file

---

*Gaps are opportunities. Identifying them is the first step to better decision interfaces.*
