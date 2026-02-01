# Surfaces Backlog

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This backlog tracks proposed or identified decision surfaces that are not yet implemented. Surfaces are distinct UI areas that support specific decision moments.

---

## Backlog Format

```
## SURFACE-{number}: {Name}

**Status**: Proposed | Approved | In Progress | Completed | Rejected
**Priority**: P0 | P1 | P2 | P3
**Related Gap**: GAP-{n} (if applicable)

**Decision Supported**: [What decision does this enable?]
**User Profile**: [Government | Industry | Both]
**Description**: [What this surface would do]
**Dependencies**: [What must exist first]
**Estimated Complexity**: Low | Medium | High
```

---

## Current Surfaces (Implemented)

| Surface | Page | Decision Supported |
|---------|------|-------------------|
| Zone Selection | app.py | Which zone to focus on |
| Profile Selection | app.py | Which lens to apply |
| Risk Overview | 1_risk_overview.py | Understand current state |
| Risk History | 1_risk_overview.py | Understand trend |
| Action Recommendations | 2_actions.py | What actions to consider |
| Action Selection | 2_actions.py | Which actions to simulate |
| Scenario Comparison | 3_simulation.py | Act vs not-act decision |
| Decision Confirmation | 3_simulation.py | Commit to action |

---

## Proposed Surfaces

### SURFACE-001: Urgency Countdown

**Status**: Proposed
**Priority**: P1
**Related Gap**: GAP-001

**Decision Supported**: Immediate visceral understanding of time pressure
**User Profile**: Both
**Description**: Enhanced days-to-critical display with visual urgency escalation (size, color, animation as days decrease)
**Dependencies**: Current risk display exists
**Estimated Complexity**: Medium

---

### SURFACE-002: Cost of Inaction Tracker

**Status**: Proposed
**Priority**: P1
**Related Gap**: GAP-002

**Decision Supported**: Understanding accumulated cost of delay
**User Profile**: Both (especially Government for public impact, Industry for cost)
**Description**: Indicator showing what is lost each day/week of inaction (population affected, economic impact, etc.)
**Dependencies**: Backend calculation of daily impact rates
**Estimated Complexity**: High (may need backend support)

---

### SURFACE-003: Decision Audit Log

**Status**: Proposed
**Priority**: P1
**Related Gap**: GAP-003

**Decision Supported**: Review and defend past decisions
**User Profile**: Government (primary), Industry (secondary)
**Description**: Persistent log of decisions made: what, when, who, based on what data
**Dependencies**: Data persistence mechanism (may need backend)
**Estimated Complexity**: High (needs persistence)

---

### SURFACE-004: Uncertainty Bands

**Status**: Proposed
**Priority**: P1
**Related Gap**: GAP-004

**Decision Supported**: Calibrated confidence in projections
**User Profile**: Both
**Description**: Visual confidence intervals on projections (fan charts, range indicators)
**Dependencies**: Backend providing confidence intervals
**Estimated Complexity**: Medium (if backend provides data)

---

### SURFACE-005: Multi-Zone Dashboard

**Status**: Proposed
**Priority**: P2
**Related Gap**: GAP-005

**Decision Supported**: Resource allocation across zones
**User Profile**: Government (primarily)
**Description**: Side-by-side comparison of multiple zones with priority ranking
**Dependencies**: Current single-zone views
**Estimated Complexity**: Medium

---

### SURFACE-006: Threshold Proximity Indicator

**Status**: Proposed
**Priority**: P2
**Related Gap**: GAP-006

**Decision Supported**: Anticipate escalation, plan proactively
**User Profile**: Both
**Description**: Visual indicator of distance to next risk level threshold
**Dependencies**: Risk level thresholds defined
**Estimated Complexity**: Low

---

### SURFACE-007: Action Implementation Tracker

**Status**: Proposed
**Priority**: P2
**Related Gap**: None (new proposal)

**Decision Supported**: Track action implementation status
**User Profile**: Both
**Description**: After decision confirmation, track which actions are being implemented, status, and effectiveness
**Dependencies**: Decision Audit Log (SURFACE-003)
**Estimated Complexity**: High (needs backend)

---

### SURFACE-008: Notification Configuration

**Status**: Proposed
**Priority**: P3
**Related Gap**: GAP-006 (partial)

**Decision Supported**: Proactive awareness of threshold crossings
**User Profile**: Both
**Description**: Configure alerts when risk level changes, days-to-critical crosses thresholds
**Dependencies**: Backend notification system
**Estimated Complexity**: High (needs backend)

---

### SURFACE-009: Scenario Comparison History

**Status**: Proposed
**Priority**: P3
**Related Gap**: None (new proposal)

**Decision Supported**: Compare current scenarios to past projections
**User Profile**: Both
**Description**: View past simulations vs actual outcomes for calibration
**Dependencies**: Historical data persistence
**Estimated Complexity**: High

---

## Rejected Surfaces

*None yet. Rejected proposals will be documented with rationale.*

---

## Priority Definitions

| Priority | Meaning | Timing |
|----------|---------|--------|
| P0 | Blocks core decision-making | Immediate |
| P1 | Significantly improves decisions | Next sessions |
| P2 | Enhances experience | Backlog |
| P3 | Nice to have | Future |

---

## How to Add

1. Assign next sequential number
2. Complete all fields
3. Link to GAP if applicable
4. Assess priority
5. Review with team

---

*Surfaces are the atoms of decision interfaces. Each one should enable a specific decision.*
