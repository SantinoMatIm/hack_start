# Design Debt Backlog

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This backlog tracks identified design debt — visual or interaction patterns that work but don't fully meet design standards or user needs.

---

## Debt Format

```
## DDEBT-{number}: {Title}

**Status**: Identified | In Progress | Resolved | Accepted
**Severity**: Critical | Major | Minor
**Location**: [Page(s)/Component(s) affected]

**Description**: [What the debt is]
**Impact**: [How it affects users]
**Remediation**: [How to fix it]
**Effort**: Low | Medium | High
**Created**: YYYY-MM-DD
```

---

## Active Design Debt

### DDEBT-001: Inconsistent Button States

**Status**: Identified
**Severity**: Minor
**Location**: All pages

**Description**: 
Selected vs unselected buttons (e.g., zone selection, profile selection) have similar visual weight. The "selected" state uses `type="primary"` but difference is subtle.

**Impact**: 
Users may not immediately perceive which option is selected.

**Remediation**: 
Enhance selected state with stronger visual differentiation (border, background intensity, checkmark).

**Effort**: Low
**Created**: 2026-01-31

---

### DDEBT-002: Action Card Checkbox Position

**Status**: Identified
**Severity**: Minor
**Location**: 2_actions.py

**Description**: 
Checkbox for action selection is in a narrow column to the left of the card. May be easy to miss; doesn't feel integrated.

**Impact**: 
Users might overlook selection mechanism; feels disconnected from card content.

**Remediation**: 
Integrate selection into card design (e.g., card border change on selection, larger touch target).

**Effort**: Medium
**Created**: 2026-01-31

---

### DDEBT-003: Risk Level Badge Consistency

**Status**: Identified
**Severity**: Minor
**Location**: Multiple components

**Description**: 
Risk level display varies slightly between components (risk card vs simulation vs inline mentions).

**Impact**: 
Inconsistent visual language for the same concept.

**Remediation**: 
Create unified risk-level badge component used everywhere.

**Effort**: Medium
**Created**: 2026-01-31

---

### DDEBT-004: Empty State Design

**Status**: Identified
**Severity**: Minor
**Location**: 3_simulation.py

**Description**: 
Empty state (no simulation run yet) shows emoji and text but feels generic.

**Impact**: 
Missed opportunity to guide user; doesn't match premium aesthetic.

**Remediation**: 
Design proper empty state with illustration or stronger visual treatment.

**Effort**: Low
**Created**: 2026-01-31

---

### DDEBT-005: Loading State Consistency

**Status**: Identified
**Severity**: Minor
**Location**: All pages

**Description**: 
Loading states use st.spinner() with varying messages. No consistent loading design.

**Impact**: 
Inconsistent experience during waits.

**Remediation**: 
Define standard loading patterns (spinner style, message format, skeleton screens for long loads).

**Effort**: Medium
**Created**: 2026-01-31

---

### DDEBT-006: Footer Repetition

**Status**: Identified
**Severity**: Minor
**Location**: All pages

**Description**: 
Footer navigation (back/forward buttons) is implemented separately on each page with slight variations.

**Impact**: 
Inconsistent navigation; maintenance burden.

**Remediation**: 
Create shared footer navigation component.

**Effort**: Low
**Created**: 2026-01-31

---

### DDEBT-007: Sidebar Styling on Inner Pages

**Status**: Identified
**Severity**: Minor
**Location**: All inner pages

**Description**: 
Sidebar has dark background but zone/profile selectors use default Streamlit styling that doesn't fully match.

**Impact**: 
Visual inconsistency in sidebar.

**Remediation**: 
Custom style sidebar widgets to match dark theme.

**Effort**: Medium
**Created**: 2026-01-31

---

## Resolved Design Debt

*None yet.*

---

## Accepted Design Debt

*None yet.*

---

## Debt Metrics

| Severity | Count |
|----------|-------|
| Critical | 0 |
| Major | 0 |
| Minor | 7 |

---

## How to Add

1. Assign next sequential number (DDEBT-{n})
2. Complete all fields
3. Assess severity
4. Add to backlog

---

*Design debt accumulates faster than technical debt. Track it to maintain visual coherence.*
