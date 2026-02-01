# Pattern Library

**Design Council — Frontend Decision Intelligence Organization**

---

## Purpose

This document catalogs approved design patterns for use across the frontend.

---

## Card Patterns

### Standard Card

```
┌─────────────────────────────────────────┐
│                                          │
│  Card content                            │
│                                          │
└─────────────────────────────────────────┘

CSS: .card or direct styles
Border: 1px solid var(--border-default)
Background: var(--bg-surface)
Padding: var(--space-lg)
```

### Risk Card

```
┌─────────────────────────────────────────┐
│  [Risk level indicator via border]      │
│                                          │
│  Metrics row                             │
│                                          │
└─────────────────────────────────────────┘

CSS: .risk-card.{level}
Border: 2px for HIGH/CRITICAL, 1px for others
Border color: Risk level color
```

### Action Card

```
┌─────────────────────────────────────────┐
│  [Priority badge]                        │
│                                          │
│  Title                                   │
│  Code                                    │
│                                          │
│  Parameters list                         │
│                                          │
│  Expected effect                         │
│                                          │
│  Justification (muted background)        │
└─────────────────────────────────────────┘

CSS: .action-card
Hover: Border color transitions to accent
```

---

## Comparison Patterns

### Side-by-Side Comparison

```
┌────────────────────┐  ┌────────────────────┐
│    SCENARIO A      │  │    SCENARIO B      │
│   (light bg)       │  │   (dark bg)        │
│                    │  │                    │
│   Metrics          │  │   Metrics          │
│   Description      │  │   Description      │
│                    │  │   + DELTA          │
└────────────────────┘  └────────────────────┘

CSS: .comparison-container (grid)
      .comparison-card.no-action
      .comparison-card.with-action
Responsive: Stack on mobile
```

---

## Button Patterns

### Primary Button

```
┌──────────────────────────┐
│    BUTTON TEXT           │
└──────────────────────────┘

Background: var(--action-primary)
Color: var(--text-inverse)
Hover: Background transitions to secondary
```

### Secondary Button

```
┌──────────────────────────┐
│    BUTTON TEXT           │
└──────────────────────────┘

Background: var(--action-secondary)
Color: var(--text-inverse)
Hover: Background transitions to primary
```

---

## Badge Patterns

### Priority Badge

```
┌────────┐
│  HIGH  │
└────────┘

CSS: .action-priority.{level}
HIGH: var(--action-primary) bg, white text
MEDIUM: var(--risk-medium) bg, dark text
LOW: var(--accent-light) bg, dark text
```

### Risk Level Badge

```
┌──────────┐
│ CRITICAL │
└──────────┘

Colors match risk level
Always include text (not color alone)
```

---

## Section Patterns

### Standard Section

```
<div class="section">
  <h2 class="section-title">Title</h2>
  Content
</div>

Padding: var(--space-xl) 0
Margin-bottom: var(--space-xl)
```

### Dark Section (CTA)

```
┌─────────────────────────────────────────┐
│                                          │
│        Centered headline                 │
│        Muted description                 │
│        [CTA Button]                      │
│                                          │
└─────────────────────────────────────────┘

CSS: .dark-section
Background: var(--bg-dark)
Text: var(--text-inverse)
Full-width bleed
```

---

## Metric Patterns

### Large Metric

```
      -1.72
     SPI-6m

CSS: .metric-container, .metric-value, .metric-label
Value: Large, bold, colored by level
Label: Small, muted, uppercase
```

### Metrics Row

```
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│  -1.72  │ │  HIGH   │ │   ↓     │ │   24    │
│ SPI-6m  │ │  RISK   │ │ TREND   │ │  DAYS   │
└─────────┘ └─────────┘ └─────────┘ └─────────┘

Grid or flex layout
Equal spacing
Responsive wrap
```

---

## Navigation Patterns

### Page Navigation Cards

```
┌────────────────────┐
│  01                │
│  Title             │
│  Description       │
│  [Button]          │
└────────────────────┘

Number: Accent color, small
Title: h3
Description: Muted
```

### Footer Navigation

```
[← Back]        [Home]        [Next →]

Three-column layout
Consistent across pages
```

---

## State Patterns

### Loading State

```
⟳ Loading message...

Use st.spinner()
Clear message indicating what's loading
```

### Error State

```
⚠️ Error message

[Retry]  [Alternative action]

Clear description
Recovery options
```

### Empty State

```
        [Icon]
        
  Empty state message
  Guidance text
  
     [Action]

Centered
Icon appropriate to context
Clear next action
```

---

## Animation Patterns

### Scroll Reveal

```css
.reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: all 800ms ease;
}

.reveal.revealed {
    opacity: 1;
    transform: translateY(0);
}
```

### Reduced Motion Override

```css
@media (prefers-reduced-motion: reduce) {
    .reveal {
        animation: none;
        transition: none;
        opacity: 1;
        transform: none;
    }
}
```

---

*Patterns are building blocks. Use them consistently.*
