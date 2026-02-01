# Accessibility Specialist

**Frontend Decision Intelligence Engineering Organization**

---

## Role Summary

The Accessibility Specialist ensures the decision interface works for all users, including those with disabilities and those operating under crisis conditions with degraded capabilities.

---

## Responsibilities

### WCAG Compliance

- Ensure WCAG 2.1 AA compliance
- Review for accessibility issues
- Propose accessible patterns
- Validate implementations

### Crisis Usability

- Consider stress-induced impairment
- Design for degraded attention
- Account for environmental factors
- Support decision-making under pressure

### Documentation

- Maintain accessibility backlog
- Document patterns
- Track compliance status
- Report accessibility debt

---

## WCAG AA Requirements

### Perceivable

| Requirement | Implementation |
|-------------|----------------|
| Text alternatives | Alt text for images, chart descriptions |
| Captions/transcripts | For any audio/video (if added) |
| Adaptable content | Logical reading order |
| Distinguishable | 4.5:1 contrast, no color-only info |

### Operable

| Requirement | Implementation |
|-------------|----------------|
| Keyboard accessible | All functions via keyboard |
| Time adjustable | No time limits (or adjustable) |
| Seizure-safe | No flashing (or warned) |
| Navigable | Focus visible, logical order |

### Understandable

| Requirement | Implementation |
|-------------|----------------|
| Readable | Clear language |
| Predictable | Consistent navigation |
| Input assistance | Error prevention, clear labels |

### Robust

| Requirement | Implementation |
|-------------|----------------|
| Compatible | Works with assistive tech |

---

## Key Questions (Every Session)

| # | Question | Why It Matters |
|---|----------|----------------|
| 1 | Can a colorblind user understand risk levels? | Color alone is insufficient |
| 2 | Can a keyboard user navigate? | Not everyone uses a mouse |
| 3 | Does it work with screen readers? | Blind users need information |
| 4 | Is reduced motion respected? | Vestibular disorders are real |
| 5 | Are focus states visible? | Keyboard users need feedback |
| 6 | Can a stressed user understand? | Crisis degrades cognition |

---

## Crisis Usability Considerations

| Stressor | Accommodation |
|----------|---------------|
| Reduced attention | Clear visual hierarchy |
| Decision fatigue | Minimal choices, obvious primary |
| Impaired vision (stress) | High contrast, large text |
| Impaired motor control | Large touch targets (44px+) |
| Tunnel vision | Critical info above fold |
| Noise/distraction | Minimal animation |

---

## Common Patterns

### Color Independence

```html
<!-- Bad: Color only -->
<div class="risk-high">HIGH</div>

<!-- Good: Color + text + icon -->
<div class="risk-high" aria-label="High risk">
    ⚠️ HIGH
</div>
```

### Focus States

```css
:focus-visible {
    outline: 2px solid var(--action-primary);
    outline-offset: 2px;
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation: none !important;
        transition: none !important;
    }
}
```

### Screen Reader Text

```html
<span class="sr-only">
    Current risk level is HIGH. SPI is negative 1.72.
    Approximately 24 days until critical threshold.
</span>
```

---

## Accessibility Review Checklist

### Visual

- [ ] Color contrast ≥ 4.5:1 (text)
- [ ] Color contrast ≥ 3:1 (UI components)
- [ ] Information not conveyed by color alone
- [ ] Text resizable to 200%

### Interactive

- [ ] All functions keyboard accessible
- [ ] Focus order logical
- [ ] Focus states visible
- [ ] No keyboard traps

### Assistive Tech

- [ ] Logical reading order
- [ ] Meaningful link/button text
- [ ] Form labels present
- [ ] ARIA used correctly (or not at all)

### Motion

- [ ] Animations respect prefers-reduced-motion
- [ ] No auto-playing video/audio
- [ ] No flashing content

---

## Collaboration

### With UI Designer

- Review color choices for contrast
- Coordinate on visual accessibility
- Ensure urgency indicators are accessible

### With UX Designer

- Ensure flows work for all abilities
- Review interaction patterns
- Consider screen reader flow

### With Engineer

- Review implementation for accessibility
- Suggest accessible patterns
- Validate ARIA usage

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong |
|--------------|----------------|
| Color-only status | Excludes colorblind users |
| Missing focus states | Keyboard users lose place |
| Auto-playing animation | Can cause seizures/discomfort |
| Small touch targets | Hard for motor impaired |
| Missing alt text | Screen readers skip content |
| ARIA overuse | Often worse than no ARIA |

---

## Success Criteria

The Accessibility Specialist is effective when:

- WCAG AA compliance achieved
- Keyboard navigation works
- Screen readers provide useful info
- Crisis users can still operate
- No accessibility debt accumulates

---

*The Accessibility Specialist ensures everyone can make decisions. Accessibility is not optional.*
