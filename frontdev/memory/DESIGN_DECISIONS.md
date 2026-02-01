# Design Decision Records

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This document records significant design decisions affecting the frontend visual language and interaction patterns. Each decision is logged with context, options considered, outcome, and rationale.

---

## DDR Format

```
## DDR-{number}: {Title}

**Date**: YYYY-MM-DD
**Status**: Proposed | Accepted | Deprecated | Superseded by DDR-{n}
**Context**: [Why this decision was needed]
**Options Considered**:
1. [Option A]
2. [Option B]
**Decision**: [What was decided]
**Rationale**: [Why this option]
**Consequences**: [What this means going forward]
```

---

## Current DDRs

### DDR-001: Premium Minimal Aesthetic

**Date**: 2024-01-01
**Status**: Accepted

**Context**:
Enterprise and government users expect sophisticated visual treatment. The interface must communicate seriousness and trustworthiness.

**Options Considered**:
1. Default Streamlit appearance
2. Corporate blue/gray palette
3. Premium minimal (warm neutrals, sharp edges, bold typography)
4. Data-dense dashboard aesthetic

**Decision**: Premium minimal aesthetic

**Rationale**:
- Communicates sophistication without distraction
- Warm neutrals (F2EDE9) feel calming yet serious
- Sharp edges convey precision
- Bold typography creates clear hierarchy
- Distinct from typical "dashboard" appearance

**Consequences**:
- All components must follow design tokens
- Custom CSS required for implementation
- Distinct visual identity established

---

### DDR-002: Risk Level Color Coding

**Date**: 2024-01-01
**Status**: Accepted

**Context**:
Risk levels (LOW, MEDIUM, HIGH, CRITICAL) need visual distinction. Colors must be accessible and meaningful.

**Options Considered**:
1. Single accent color with intensity variation
2. Traffic light (green/yellow/red)
3. Custom palette with semantic meaning
4. Grayscale with badges

**Decision**: Custom palette with semantic meaning

**Rationale**:
- Green (#10B981) for LOW: Safety, normalcy
- Yellow (#F59E0B) for MEDIUM: Caution, awareness
- Orange (#E76237) for HIGH: Warning, action needed
- Red (#DC2626) for CRITICAL: Danger, immediate action

**Consequences**:
- Must maintain 4.5:1 contrast ratios
- Must not rely on color alone (add icons/text)
- Palette locked into design system

---

### DDR-003: No Border Radius (Sharp Edges)

**Date**: 2024-01-01
**Status**: Accepted

**Context**:
Component shape affects perceived personality. Rounded vs sharp edges convey different qualities.

**Options Considered**:
1. Standard rounded corners (4-8px)
2. Pill shapes for buttons
3. Sharp edges (0 radius)
4. Mixed approach

**Decision**: Sharp edges (border-radius: 0) throughout

**Rationale**:
- Communicates precision and decisiveness
- Aligns with "premium minimal" direction
- Creates distinctive visual identity
- Appropriate for serious decision-making context

**Consequences**:
- All components use sharp edges
- Buttons, cards, inputs all have 0 radius
- Creates consistent, distinctive appearance

---

### DDR-004: Scroll-Reveal Animations

**Date**: 2024-01-01
**Status**: Accepted

**Context**:
Page content appears static and abrupt without animation. Needed to determine motion approach.

**Options Considered**:
1. No animations
2. Page transitions
3. Scroll-reveal (elements animate in as they enter viewport)
4. Constant subtle motion

**Decision**: Scroll-reveal animations with 800ms default

**Rationale**:
- Guides user attention
- Creates sense of progression
- Manageable performance impact
- Can be disabled for reduced motion preference

**Consequences**:
- JavaScript required for intersection observer
- Must respect prefers-reduced-motion
- Classes (.reveal, .fade-up) must be applied consistently

---

### DDR-005: Comparison Layout (Side-by-Side)

**Date**: 2024-01-01
**Status**: Accepted

**Context**:
Simulation shows two scenarios: no-action and with-action. Layout affects comparison clarity.

**Options Considered**:
1. Sequential (one after the other)
2. Side-by-side cards
3. Tabbed interface
4. Overlay comparison

**Decision**: Side-by-side cards with visual contrast

**Rationale**:
- Enables direct visual comparison
- No-action in light, with-action in dark creates clear distinction
- Supports "consequences are visible" principle
- Responsive stacking on mobile

**Consequences**:
- Requires two-column layout
- Must stack on mobile (< 768px)
- Dark card needs inverse text treatment

---

### DDR-006: Hero Section for Landing

**Date**: 2024-01-01
**Status**: Accepted

**Context**:
The main entry point (app.py) needs to establish context and purpose immediately.

**Options Considered**:
1. Jump straight to zone selection
2. Hero section with tagline
3. Animated intro sequence
4. Video background

**Decision**: Hero section with tagline, then zone selection

**Rationale**:
- Establishes platform purpose immediately
- "Water Risk Intelligence" clearly communicates domain
- Premium appearance appropriate for B2B/B2G
- Not excessive for users who know what they want

**Consequences**:
- First-time users get context
- Returning users can scroll past quickly
- Mobile must handle large typography gracefully

---

## Pending Decisions

### DDR-007: Urgency Animation Pattern

**Date**: Pending
**Status**: Proposed

**Context**:
Days-to-critical in critical state (<15 days) should have visual urgency. Current design shows color but no motion.

**Options Considered**:
1. Subtle pulse animation
2. Color shift animation
3. Size breathing effect
4. No animation, rely on color intensity

**Decision**: Pending session work

**Rationale**: TBD

**Consequences**: TBD

---

### DDR-008: Multi-Zone Comparison Layout

**Date**: Pending
**Status**: Proposed

**Context**:
Current design shows one zone at a time. Users managing multiple zones may need comparison view.

**Options Considered**:
1. Zone selector with single view
2. Side-by-side zone cards
3. Dashboard-style grid
4. Tabs per zone

**Decision**: Pending — identified as GAP in KNOWN_GAPS.md

---

## Superseded Decisions

*None yet. Decisions that are superseded will be marked and linked to their replacement.*

---

## How to Add a DDR

1. Assign next sequential number
2. Fill out all sections
3. Get approval during session (Design Council or Phase 3)
4. Update this file
5. Reference DDR number in design documentation where relevant

---

*Design decisions create visual coherence. They are the memory of our aesthetic choices.*
