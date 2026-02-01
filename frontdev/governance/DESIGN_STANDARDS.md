# Design Standards

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This document defines the visual and interaction standards for all frontend work. These standards ensure consistency, accessibility, and alignment with decision-support principles.

---

## Design Philosophy

### Core Tenets

1. **Clarity over decoration** — Every visual element serves comprehension
2. **Urgency is communicated visually** — Time pressure is felt, not just read
3. **Consequences are visible** — Act vs not-act must be clear
4. **Premium minimalism** — Sophisticated simplicity, not bare functionality

### Anti-Patterns

| Anti-Pattern | Why It's Wrong |
|--------------|----------------|
| Dashboard theater | Beautiful but passive; doesn't compel action |
| Visual noise | Competing elements dilute decision clarity |
| False neutrality | Treating all information as equally important |
| Hidden complexity | Obscuring critical data behind interactions |

---

## Design Tokens

All visual decisions must use defined tokens from `styles.css`:

### Colors

```css
/* Background */
--bg-primary: #F2EDE9;    /* Main background */
--bg-surface: #FFFFFF;    /* Cards, containers */
--bg-dark: #292929;       /* Inverse sections */

/* Text */
--text-primary: #292929;  /* Main text */
--text-inverse: #FFFFFF;  /* On dark backgrounds */
--text-muted: #7E8076;    /* Secondary text */

/* Actions */
--action-primary: #E76237; /* Primary CTA, high urgency */
--action-secondary: #292929; /* Secondary actions */

/* Risk Levels - MUST be used consistently */
--risk-critical: #DC2626;  /* SPI ≤ -1.5, Days < 15 */
--risk-high: #E76237;      /* SPI -1.5 to -1.0 */
--risk-medium: #F59E0B;    /* SPI -1.0 to -0.5 */
--risk-low: #10B981;       /* SPI > -0.5 */
```

### Typography

| Element | Size | Weight | Use Case |
|---------|------|--------|----------|
| Display | clamp(48px, 8vw, 90px) | 800 | Hero headlines only |
| H1 | clamp(40px, 6vw, 70px) | 800 | Page titles |
| H2 | clamp(32px, 4vw, 55px) | 800 | Section titles |
| H3 | clamp(24px, 3vw, 38px) | 700 | Card titles |
| Body | 18px | 450 | Paragraphs, descriptions |
| Body Large | 20px | 500 | Intro text, emphasis |
| Caption | 14px | 600 | Labels, metadata |
| Micro | 12px | 700 | Tags, badges |

### Spacing

```css
--space-xs: 8px;   /* Tight grouping */
--space-sm: 12px;  /* Related elements */
--space-md: 20px;  /* Standard padding */
--space-lg: 32px;  /* Section separation */
--space-xl: 48px;  /* Major sections */
--space-2xl: 72px; /* Page sections */
--space-3xl: 96px; /* Hero spacing */
```

### Motion

```css
--duration-fast: 200ms;    /* Micro-interactions */
--duration-medium: 600ms;  /* State changes */
--duration-slow: 800ms;    /* Reveals, transitions */
--ease-default: cubic-bezier(0.4, 0, 0.2, 1);
--ease-smooth: cubic-bezier(0.19, 1, 0.22, 1);
```

---

## Component Patterns

### Risk Card

```
┌─────────────────────────────────────────────────────────────┐
│  RISK CARD                                                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ ZONE: CDMX                              GOVERNMENT  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌─────────┐  │
│  │   -1.72   │  │   HIGH    │  │ WORSENING │  │ 24 DAYS │  │
│  │  SPI-6m   │  │   RISK    │  │   TREND   │  │TO CRIT. │  │
│  └───────────┘  └───────────┘  └───────────┘  └─────────┘  │
│                                                              │
│  Border color reflects risk level (high = accent orange)    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Action Card

```
┌─────────────────────────────────────────────────────────────┐
│  ☐  ACTION CARD                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐                                                │
│  │   HIGH   │  ← Priority badge (colored)                   │
│  └──────────┘                                                │
│                                                              │
│  Network Pressure Reduction                                  │
│  H2_PRESSURE_REDUCTION                                       │
│                                                              │
│  Parameters:                                                 │
│  • Reduction: 15%                                            │
│  • Duration: 30 days                                         │
│                                                              │
│  Expected Effect: +6 days to critical                        │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Justification: SPI in range -1.2 to -1.8, worsening │    │
│  │ conditions warrant pressure management per H2.       │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Comparison Layout (Simulation)

```
┌─────────────────────────────┐  ┌─────────────────────────────┐
│  NO ACTION                  │  │  WITH ACTION                │
│  (Light background)         │  │  (Dark background)          │
├─────────────────────────────┤  ├─────────────────────────────┤
│                             │  │                             │
│  Projected SPI: -2.12       │  │  Projected SPI: -1.87       │
│  Risk Level: CRITICAL       │  │  Risk Level: HIGH           │
│  Days to Critical: 24       │  │  Days to Critical: 52       │
│                             │  │                             │
│  "Without intervention..."  │  │  "With selected actions..." │
│                             │  │  DAYS GAINED: +28           │
│                             │  │                             │
└─────────────────────────────┘  └─────────────────────────────┘
```

---

## Visual Hierarchy Rules

### Information Priority

```
Level 1: DECISION OUTCOME
         What happens if I act vs don't act?
         ↓
Level 2: CURRENT STATE
         Where are we now? (SPI, Risk, Trend)
         ↓
Level 3: RECOMMENDED ACTION
         What should I do?
         ↓
Level 4: SUPPORTING DETAIL
         Parameters, justifications, methodology
```

### Visual Weight Mapping

| Priority | Visual Treatment |
|----------|------------------|
| Critical information | Largest type, highest contrast, prominent position |
| Primary data | Clear type, strong contrast, above fold |
| Supporting context | Medium type, muted color, accessible on demand |
| Reference material | Small type, expandable/collapsible |

---

## Urgency Communication

### Days-to-Critical Visual Escalation

| Days | Visual Treatment |
|------|------------------|
| > 45 | Standard display, --text-primary |
| 30-45 | Elevated size, --risk-medium |
| 15-30 | Warning state, --risk-high, increased weight |
| < 15 | Critical state, --risk-critical, animation, maximum prominence |

### Urgency Indicators

```css
/* Progressive urgency */
.urgency-low { color: var(--text-primary); }
.urgency-medium { color: var(--risk-medium); font-weight: 600; }
.urgency-high { color: var(--risk-high); font-weight: 700; font-size: 1.1em; }
.urgency-critical { 
    color: var(--risk-critical); 
    font-weight: 800; 
    font-size: 1.2em;
    animation: pulse 2s infinite; /* Must respect prefers-reduced-motion */
}
```

---

## Accessibility Standards

### Color

- Never convey information by color alone
- Maintain 4.5:1 contrast for normal text
- Maintain 3:1 contrast for large text and UI components
- Provide patterns or icons alongside color coding

### Motion

```css
@media (prefers-reduced-motion: reduce) {
    .reveal,
    .urgency-critical {
        animation: none;
        transition: none;
    }
}
```

### Focus States

All interactive elements must have visible focus:

```css
:focus-visible {
    outline: 2px solid var(--action-primary);
    outline-offset: 2px;
}
```

### Screen Readers

- Use semantic HTML structure
- Provide meaningful alt text for visualizations
- Ensure logical reading order
- Use ARIA labels where needed

---

## Responsive Behavior

### Breakpoints

| Breakpoint | Width | Behavior |
|------------|-------|----------|
| Desktop | > 1024px | Full layout, side-by-side comparisons |
| Tablet | 768-1024px | Adjusted spacing, stacked where needed |
| Mobile | < 768px | Single column, stacked cards |

### Critical Adjustments

```css
@media (max-width: 768px) {
    /* Comparison cards stack */
    .comparison-container {
        grid-template-columns: 1fr;
    }
    
    /* Maintain readability */
    .metric-value {
        font-size: clamp(28px, 4vw, 36px);
    }
}
```

---

## Interaction Patterns

### Button Hierarchy

| Type | Use Case | Visual |
|------|----------|--------|
| Primary | Main CTA, recommended action | --action-primary background |
| Secondary | Alternative actions | --action-secondary background |
| Tertiary | Navigation, less important | Border only |

### Loading States

```
┌─────────────────────────────────────────┐
│                                          │
│  ⟳ Loading risk data...                  │
│                                          │
│  [Progress indicator if long operation]  │
│                                          │
└─────────────────────────────────────────┘
```

### Error States

```
┌─────────────────────────────────────────┐
│  ⚠️ Unable to fetch risk data            │
│                                          │
│  Please ensure the API server is running │
│                                          │
│  [Try Again]  [Show Demo Data]           │
│                                          │
└─────────────────────────────────────────┘
```

### Empty States

```
┌─────────────────────────────────────────┐
│                                          │
│              🔮                           │
│                                          │
│  No simulation results yet               │
│  Click "Run Simulation" to compare       │
│  scenarios                               │
│                                          │
│        [Run Simulation]                  │
│                                          │
└─────────────────────────────────────────┘
```

---

## Profile-Specific Adaptations

### Government Profile

- Emphasize urgency indicators
- Prioritize public impact messaging
- Include accountability/audit trail prompts
- Use formal, authoritative tone

### Industry Profile

- Emphasize cost-benefit metrics
- Prioritize operational impact
- Include ROI indicators where applicable
- Use efficiency-focused language

---

## Design Review Checklist

Before Phase 3 Fidelity Review, verify:

- [ ] All colors from design tokens (no hardcoded values)
- [ ] Typography follows scale
- [ ] Spacing uses token values
- [ ] Risk levels have consistent color treatment
- [ ] Urgency escalation is visual
- [ ] Accessibility requirements met
- [ ] Responsive behavior tested
- [ ] Loading/error/empty states designed
- [ ] Profile-specific needs considered

---

*Design standards ensure visual consistency and decision-support effectiveness across all frontend surfaces.*
