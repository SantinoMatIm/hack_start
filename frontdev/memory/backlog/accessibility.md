# Accessibility Backlog

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This backlog tracks identified accessibility issues and improvements needed to meet WCAG AA standards and crisis usability requirements.

---

## Issue Format

```
## A11Y-{number}: {Title}

**Status**: Identified | In Progress | Resolved
**WCAG Criterion**: [Specific criterion if applicable]
**Severity**: Critical | Major | Minor
**Location**: [Page(s)/Component(s) affected]

**Description**: [What the issue is]
**Impact**: [Who is affected and how]
**Remediation**: [How to fix it]
**Effort**: Low | Medium | High
**Created**: YYYY-MM-DD
```

---

## Active Issues

### A11Y-001: Color-Only Risk Indication

**Status**: Identified
**WCAG Criterion**: 1.4.1 Use of Color
**Severity**: Major
**Location**: Risk cards, risk gauge, simulation comparison

**Description**: 
Risk levels are primarily distinguished by color (green/yellow/orange/red).

**Impact**: 
Color-blind users may not distinguish risk levels.

**Remediation**: 
Add icons, patterns, or text labels alongside color. Ensure risk level text is always present.

**Effort**: Medium
**Created**: 2026-01-31

---

### A11Y-002: Reduced Motion Not Fully Respected

**Status**: Identified
**WCAG Criterion**: 2.3.3 Animation from Interactions
**Severity**: Minor
**Location**: Scroll-reveal animations throughout

**Description**: 
CSS includes @media (prefers-reduced-motion: reduce) but implementation may not cover all animations.

**Impact**: 
Users with vestibular disorders may experience discomfort.

**Remediation**: 
Audit all animations; ensure all respect prefers-reduced-motion.

**Effort**: Low
**Created**: 2026-01-31

---

### A11Y-003: Focus Visibility on Custom Components

**Status**: Identified
**WCAG Criterion**: 2.4.7 Focus Visible
**Severity**: Major
**Location**: Custom HTML components rendered via st.markdown()

**Description**: 
Custom HTML elements may not have visible focus states for keyboard navigation.

**Impact**: 
Keyboard users may lose track of focus position.

**Remediation**: 
Add :focus-visible styles to all interactive custom elements.

**Effort**: Medium
**Created**: 2026-01-31

---

### A11Y-004: Screen Reader Order in Cards

**Status**: Identified
**WCAG Criterion**: 1.3.2 Meaningful Sequence
**Severity**: Minor
**Location**: Action cards, risk cards

**Description**: 
Visual layout may not match DOM order; screen readers may read content in unexpected sequence.

**Impact**: 
Screen reader users may find content confusing.

**Remediation**: 
Audit DOM order vs visual order; adjust HTML structure or use CSS order property carefully.

**Effort**: Medium
**Created**: 2026-01-31

---

### A11Y-005: Chart Accessibility

**Status**: Identified
**WCAG Criterion**: 1.1.1 Non-text Content
**Severity**: Major
**Location**: Risk history chart, simulation projection chart

**Description**: 
Plotly charts may lack adequate alt text or text alternatives for data visualization.

**Impact**: 
Screen reader users cannot access chart information.

**Remediation**: 
Add descriptive text summary of chart data; use Plotly accessibility features.

**Effort**: Medium
**Created**: 2026-01-31

---

### A11Y-006: Touch Target Size

**Status**: Identified
**WCAG Criterion**: 2.5.5 Target Size
**Severity**: Minor
**Location**: Checkboxes on action cards, some buttons

**Description**: 
Some interactive elements may be smaller than 44x44 CSS pixels.

**Impact**: 
Users with motor impairments may have difficulty activating small targets.

**Remediation**: 
Increase touch target sizes; add padding to clickable areas.

**Effort**: Low
**Created**: 2026-01-31

---

### A11Y-007: Error Identification

**Status**: Identified
**WCAG Criterion**: 3.3.1 Error Identification
**Severity**: Minor
**Location**: API error states

**Description**: 
Error messages appear via st.error() but may not be announced to screen readers properly.

**Impact**: 
Screen reader users may miss error feedback.

**Remediation**: 
Ensure errors are in ARIA live regions or use Streamlit's built-in accessibility.

**Effort**: Low
**Created**: 2026-01-31

---

### A11Y-008: Link Purpose

**Status**: Identified
**WCAG Criterion**: 2.4.4 Link Purpose
**Severity**: Minor
**Location**: Navigation buttons

**Description**: 
Buttons like "→" arrow-only may not convey purpose without visible text context.

**Impact**: 
Context may be lost when navigating by links/buttons.

**Remediation**: 
Ensure all buttons have descriptive text or ARIA labels.

**Effort**: Low
**Created**: 2026-01-31

---

## Resolved Issues

*None yet.*

---

## Accessibility Metrics

| Severity | Count |
|----------|-------|
| Critical | 0 |
| Major | 3 |
| Minor | 5 |

### WCAG Coverage

| Category | Status |
|----------|--------|
| Perceivable | Needs work (A11Y-001, A11Y-005) |
| Operable | Needs work (A11Y-002, A11Y-003, A11Y-006) |
| Understandable | Needs work (A11Y-004, A11Y-007) |
| Robust | Not yet assessed |

---

## Crisis Usability Considerations

Beyond WCAG, consider:

| Factor | Concern | Mitigation |
|--------|---------|------------|
| Stress | Reduced attention | Clear hierarchy, minimal choices |
| Fatigue | Eye strain | High contrast, appropriate type size |
| Time pressure | Quick scanning | Prominent key metrics |
| Poor environment | Glare, noise | Consider high-contrast mode |

---

## How to Add

1. Assign next sequential number (A11Y-{n})
2. Link to WCAG criterion if applicable
3. Complete all fields
4. Assess severity
5. Add to backlog

---

*Accessibility is not optional. Decision-makers under stress have reduced capabilities.*
