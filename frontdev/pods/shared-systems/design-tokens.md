# Design Tokens

**Shared Systems Pod — Frontend Decision Intelligence Engineering Organization**

---

## Overview

Design tokens are the foundational values that define the visual language of the platform. All styling should reference these tokens rather than raw values.

---

## Token Location

Tokens are defined in:
- `frontend/src/app/globals.css` — CSS variables
- Tailwind utility classes — Primary styling method

---

## Color Tokens

### Base Colors

| Token | CSS Variable | Tailwind | Hex Value |
|-------|--------------|----------|-----------|
| Background | `--background` | `bg-background` | #FAFBFC |
| Foreground | `--foreground` | `text-foreground` | #0F172A |
| Card | `--card` | `bg-card` | #FFFFFF |
| Primary | `--primary` | `bg-primary` / `text-primary` | #2563EB |
| Secondary | `--secondary` | `bg-secondary` | #F1F5F9 |
| Muted | `--muted` | `bg-muted` | #F1F5F9 |
| Muted Foreground | `--muted-foreground` | `text-muted-foreground` | #64748B |
| Border | `--border` | `border` | #E2E8F0 |
| Destructive | `--destructive` | `bg-destructive` | #DC2626 |

### Risk Level Colors

| Level | CSS Variable | Tailwind Class | Hex Value |
|-------|--------------|----------------|-----------|
| Critical | `--risk-critical` | `text-red-600` / `bg-red-100` | #DC2626 |
| High | `--risk-high` | `text-orange-600` / `bg-orange-100` | #EA580C |
| Medium | `--risk-medium` | `text-amber-600` / `bg-amber-100` | #D97706 |
| Low | `--risk-low` | `text-emerald-600` / `bg-emerald-100` | #059669 |

### Usage Examples

```tsx
// Risk level styling
<Badge className="bg-red-100 text-red-700 border-red-200">Critical</Badge>
<Badge className="bg-orange-100 text-orange-700 border-orange-200">High</Badge>
<Badge className="bg-amber-100 text-amber-700 border-amber-200">Medium</Badge>
<Badge className="bg-emerald-100 text-emerald-700 border-emerald-200">Low</Badge>

// Primary actions
<Button className="bg-primary text-primary-foreground">Action</Button>

// Muted text
<p className="text-muted-foreground">Secondary information</p>
```

---

## Typography

### Font Family

```css
font-family: 'Inter', system-ui, -apple-system, sans-serif;
```

Loaded via Google Fonts in `globals.css`.

### Scale

| Element | Tailwind Classes | Size |
|---------|------------------|------|
| Display | `text-5xl md:text-6xl font-extrabold` | 48-64px |
| H1 | `text-3xl md:text-4xl font-bold` | 30-36px |
| H2 | `text-2xl md:text-3xl font-bold` | 24-30px |
| H3 | `text-lg md:text-xl font-semibold` | 18-20px |
| Body | `text-base` | 16px |
| Body Large | `text-lg` | 18px |
| Caption | `text-sm font-medium` | 14px |
| Micro | `text-xs font-semibold` | 12px |

### Usage

```tsx
<h1 className="text-3xl font-bold tracking-tight">Page Title</h1>
<p className="text-muted-foreground">Description text</p>
<span className="text-sm text-muted-foreground">Caption</span>
```

---

## Spacing

Use Tailwind's spacing scale:

| Token | Tailwind | Value |
|-------|----------|-------|
| xs | `p-1`, `m-1`, `gap-1` | 4px |
| sm | `p-2`, `m-2`, `gap-2` | 8px |
| md | `p-3`, `m-3`, `gap-3` | 12px |
| lg | `p-4`, `m-4`, `gap-4` | 16px |
| xl | `p-6`, `m-6`, `gap-6` | 24px |
| 2xl | `p-8`, `m-8`, `gap-8` | 32px |

### Container

```tsx
<div className="container py-8">
  {/* Centered content with responsive padding */}
</div>
```

---

## Border Radius

| Token | Tailwind | Value |
|-------|----------|-------|
| None | `rounded-none` | 0 |
| Small | `rounded-sm` | 2px |
| Default | `rounded` / `rounded-md` | 6px |
| Large | `rounded-lg` | 8px |
| XL | `rounded-xl` | 12px |
| Full | `rounded-full` | 9999px |

shadcn/ui components use `--radius` variable (0.5rem default).

---

## Shadows

| Token | Tailwind | Use Case |
|-------|----------|----------|
| None | `shadow-none` | Flat elements |
| XS | `shadow-xs` | Subtle depth |
| Small | `shadow-sm` | Cards at rest |
| Medium | `shadow-md` | Elevated elements |
| Large | `shadow-lg` | Modals, dropdowns |
| XL | `shadow-xl` | Focus elements |

### Usage

```tsx
<Card className="shadow-sm hover:shadow-md transition-shadow">
```

---

## Motion

### Durations

| Token | Tailwind | Value | Use Case |
|-------|----------|-------|----------|
| Fast | `duration-150` | 150ms | Micro-interactions |
| Default | `duration-200` | 200ms | State changes |
| Slow | `duration-300` | 300ms | Reveals |
| Slower | `duration-500` | 500ms | Page transitions |

### Transitions

```tsx
// Standard transition
<Card className="transition-all duration-200">

// Hover effects
<Card className="transition-all duration-200 hover:shadow-lg hover:-translate-y-1">
```

### Reduced Motion

```tsx
// Respect user preferences
<div className="motion-safe:animate-fade-in">
```

---

## Animations

Defined in `globals.css`:

```css
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fade-up {
  from { 
    opacity: 0; 
    transform: translateY(10px); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}

.animate-fade-in { animation: fade-in 0.3s ease-out; }
.animate-fade-up { animation: fade-up 0.4s ease-out; }
```

### Usage

```tsx
<div className="animate-fade-in">
  {/* Content fades in on mount */}
</div>
```

---

## Dark Mode (Ready)

Tokens support dark mode via CSS variables:

```css
.dark {
  --background: #0A0F1A;
  --foreground: #F8FAFC;
  --card: #141B2D;
  /* ... */
}
```

Toggle with class on `<html>`:

```tsx
<html className="dark">
```

---

## Usage Guidelines

### DO

- Use Tailwind utility classes
- Use CSS variables for custom values
- Use `cn()` for conditional classes
- Follow the spacing scale

### DON'T

- Use inline styles
- Use arbitrary Tailwind values (`w-[123px]`) without justification
- Hardcode colors
- Create one-off custom classes

---

*Design tokens ensure visual consistency across the entire frontend.*
