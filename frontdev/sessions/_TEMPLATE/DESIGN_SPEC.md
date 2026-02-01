# DESIGN SPECIFICATION

## Session

**Session ID**: {session-id}  
**Surface**: {page/component being designed}

---

## UX Specification

### User Flow

```
[Start State] → [Trigger/Action] → [Intermediate State] → [End State]
```

Detailed flow:

1. User arrives at {starting point}
2. User sees {what they see}
3. User does {action}
4. System responds with {response}
5. User reaches {end state}

### Interaction Map

| User Action | System Response | Cognitive Load | Notes |
|-------------|-----------------|----------------|-------|
| {action} | {response} | Low / Med / High | {notes} |
| | | | |

### Decision Path

What decisions does this surface support?

| Decision Point | Information Needed | Action Enabled |
|----------------|-------------------|----------------|
| {decision} | {info required} | {what user can do} |
| | | |

### Profile-Specific Adaptations

| Aspect | Government | Industry |
|--------|------------|----------|
| Information priority | {what's emphasized} | {what's emphasized} |
| Language | {tone/terms} | {tone/terms} |
| Metrics shown | {which metrics} | {which metrics} |

### Friction Points Identified

| Point | Cause | Resolution |
|-------|-------|------------|
| {friction} | {why it's friction} | {how to resolve} |
| | | |

---

## UI Specification

### Visual Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│ [PRIMARY] ─────────────────────────────────────────────────────│
│                                                                 │
│     [SECONDARY] ────────────────────────────────               │
│                                                                 │
│          [TERTIARY] ─────────────                              │
└─────────────────────────────────────────────────────────────────┘
```

What gets most visual weight and why.

### Component Specifications

| Component | State | Visual Treatment | Token Reference |
|-----------|-------|------------------|-----------------|
| {component} | default | {description} | {CSS class/token} |
| {component} | hover | {description} | {CSS class/token} |
| {component} | active | {description} | {CSS class/token} |
| {component} | disabled | {description} | {CSS class/token} |
| {component} | error | {description} | {CSS class/token} |

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                            Header                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────┐  ┌────────────────────────┐         │
│  │                        │  │                        │         │
│  │     Component A        │  │     Component B        │         │
│  │                        │  │                        │         │
│  └────────────────────────┘  └────────────────────────┘         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                     Component C                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Motion Specifications

| Trigger | Animation | Duration | Easing | Purpose |
|---------|-----------|----------|--------|---------|
| {trigger} | {what animates} | {ms} | {easing} | {why} |
| | | | | |

### Urgency Escalation (if applicable)

| Condition | Visual Change |
|-----------|---------------|
| Days > 45 | {treatment} |
| Days 30-45 | {treatment} |
| Days 15-30 | {treatment} |
| Days < 15 | {treatment} |

---

## Responsive Behavior

| Breakpoint | Layout Change |
|------------|---------------|
| Desktop (>1024px) | {layout} |
| Tablet (768-1024px) | {layout} |
| Mobile (<768px) | {layout} |

---

## Accessibility Checklist

- [ ] Color contrast meets WCAG AA (4.5:1 normal text)
- [ ] Information not conveyed by color alone
- [ ] Motion respects `prefers-reduced-motion`
- [ ] Focus states visible on all interactive elements
- [ ] Screen reader flow is logical
- [ ] Touch targets are at least 44x44px
- [ ] Error states are perceivable

---

## Open Design Questions

Questions for Design Council or human input:

1. {question}
2. {question}

---

## Sign-off

- [ ] UI Designer review
- [ ] UX Designer review
- [ ] Accessibility review

**Notes**: 
