# Design Tokens Reference

**Shared Systems Pod — Frontend Decision Intelligence Organization**

---

## Purpose

This document serves as the authoritative reference for all design tokens used in the frontend. Tokens are the single source of truth for visual decisions.

---

## Color Tokens

### Base Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--color-white` | `#F2EDE9` | Warm white, primary background |
| `--color-surface` | `#FFFFFF` | Pure white, cards and elevated surfaces |
| `--color-black` | `#292929` | Near black, primary text |

### Semantic Background Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--bg-primary` | `#F2EDE9` | Main page background |
| `--bg-surface` | `#FFFFFF` | Cards, modals, elevated elements |
| `--bg-dark` | `#292929` | Inverse sections, footer |

### Text Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--text-primary` | `#292929` | Main body text |
| `--text-inverse` | `#FFFFFF` | Text on dark backgrounds |
| `--text-muted` | `#7E8076` | Secondary text, captions |

### Action Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--action-primary` | `#E76237` | Primary CTA, accent color |
| `--action-secondary` | `#292929` | Secondary actions |
| `--accent-light` | `#D9D7CC` | Subtle accents |
| `--accent-dark` | `#7E8076` | Muted accents |

### Risk Level Colors

| Token | Value | Risk Level | SPI Range |
|-------|-------|------------|-----------|
| `--risk-critical` | `#DC2626` | CRITICAL | ≤ -1.5 |
| `--risk-high` | `#E76237` | HIGH | -1.5 to -1.0 |
| `--risk-medium` | `#F59E0B` | MEDIUM | -1.0 to -0.5 |
| `--risk-low` | `#10B981` | LOW | > -0.5 |

### Border Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--border-default` | `#292929` | Standard borders |

---

## Typography Tokens

### Font Family

```css
--font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
```

### Type Scale

| Class | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| `.display-text` | clamp(48px, 8vw, 90px) | 800 | 0.95 | Hero headlines |
| `h1` | clamp(40px, 6vw, 70px) | 800 | 1.0 | Page titles |
| `h2`, `.section-title` | clamp(32px, 4vw, 55px) | 800 | 1.1 | Section titles |
| `h3` | clamp(24px, 3vw, 38px) | 700 | 1.2 | Card titles |
| `.body-large` | 20px | 500 | 1.35 | Intro text |
| `p` | 18px | 450 | 1.45 | Body text |
| `.metric-label` | 14px | 600 | — | Labels, captions |
| Micro | 12px | 700 | — | Tags, badges |

---

## Spacing Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | 8px | Tight grouping |
| `--space-sm` | 12px | Related elements |
| `--space-md` | 20px | Standard padding |
| `--space-lg` | 32px | Section separation |
| `--space-xl` | 48px | Major sections |
| `--space-2xl` | 72px | Page sections |
| `--space-3xl` | 96px | Hero spacing |

---

## Motion Tokens

### Duration

| Token | Value | Usage |
|-------|-------|-------|
| `--duration-fast` | 200ms | Micro-interactions |
| `--duration-medium` | 600ms | State changes |
| `--duration-slow` | 800ms | Reveals, page transitions |
| `--duration-default` | 800ms | Default animation |

### Easing

| Token | Value | Usage |
|-------|-------|-------|
| `--ease-default` | cubic-bezier(0.4, 0, 0.2, 1) | Standard easing |
| `--ease-smooth` | cubic-bezier(0.19, 1, 0.22, 1) | Smooth out |

---

## Shape Tokens

| Property | Value | Notes |
|----------|-------|-------|
| Border radius | 0 | Sharp edges throughout |
| Border width | 1px | Standard borders |

---

## Component Patterns

### Cards

```css
.card-base {
    background-color: var(--bg-surface);
    border: 1px solid var(--border-default);
    padding: var(--space-lg);
}
```

### Buttons

```css
.button-primary {
    background-color: var(--action-primary);
    color: var(--text-inverse);
    border: none;
    padding: 16px 24px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.button-secondary {
    background-color: var(--action-secondary);
    color: var(--text-inverse);
    /* Same padding/font */
}
```

### Sections

```css
.section {
    padding: var(--space-xl) 0;
    margin-bottom: var(--space-xl);
}

.dark-section {
    background-color: var(--bg-dark);
    color: var(--text-inverse);
    padding: var(--space-3xl) var(--space-xl);
}
```

---

## Responsive Breakpoints

| Name | Width | Behavior |
|------|-------|----------|
| Desktop | > 1024px | Full layout |
| Tablet | 768-1024px | Adjusted spacing |
| Mobile | < 768px | Single column |

---

## Accessibility Requirements

| Requirement | Standard |
|-------------|----------|
| Text contrast | 4.5:1 minimum |
| Large text contrast | 3:1 minimum |
| Focus indicator | 2px solid accent |
| Touch target | 44x44px minimum |

---

## Token Usage Rules

1. **Always use tokens** — Never hardcode values
2. **Semantic over literal** — Use `--risk-high` not `#E76237`
3. **Add tokens through governance** — New tokens require Design Council approval
4. **Document new tokens** — Update this file when adding

---

*Tokens are the vocabulary of our visual language.*
