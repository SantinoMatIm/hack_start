# Review Criteria

**Decision Fidelity Review Board — Frontend Organization**

---

## Purpose

This document defines the criteria applied during Phase 3 Fidelity Review.

---

## Review Checklist

### 1. Accuracy

| Check | Question | Pass Criteria |
|-------|----------|---------------|
| Data accuracy | Does displayed data match API response? | Exact match |
| State accuracy | Does UI reflect system state? | No stale data |
| Label accuracy | Are labels correct? | Matches meaning |

**Failure Examples**:
- SPI shown as -1.7 when API returns -1.72
- Risk level shown as MEDIUM when API says HIGH
- Trend arrow opposite to trend direction

### 2. Uncertainty Communication

| Check | Question | Pass Criteria |
|-------|----------|---------------|
| Projections labeled | Are projections marked as estimates? | Clear labeling |
| Confidence visible | Are confidence levels shown where available? | Visible or accessible |
| Measured vs estimated | Is distinction clear? | Visual differentiation |

**Failure Examples**:
- "Days to critical: 24" without "estimated"
- Projection chart without noting it's a projection
- AI-generated text without AI attribution

### 3. Consequence Clarity

| Check | Question | Pass Criteria |
|-------|----------|---------------|
| No-action visible | Is no-action scenario clear? | Prominent display |
| With-action visible | Is with-action scenario clear? | Prominent display |
| Delta prominent | Is the difference highlighted? | Visually emphasized |
| Comparison enabled | Can user compare scenarios? | Side-by-side or clear contrast |

**Failure Examples**:
- Only showing with-action scenario
- Delta buried in text
- Comparison requires mental calculation

### 4. Decision Support Under Pressure

| Check | Question | Pass Criteria |
|-------|----------|---------------|
| Clear hierarchy | Is critical info prominent? | Visual hierarchy clear |
| Minimal cognitive load | Can stressed user understand? | Simple, clear |
| Primary action obvious | Is recommended path clear? | Stands out |
| Error recovery | Can user recover from mistakes? | Clear path |

**Failure Examples**:
- All information same visual weight
- Many competing calls to action
- No way to go back or undo

### 5. Accessibility

| Check | Question | Pass Criteria |
|-------|----------|---------------|
| Color contrast | Does text meet 4.5:1? | WCAG AA |
| Color independence | Info conveyed beyond color? | Yes |
| Focus visible | Can keyboard users see focus? | Clear indicator |
| Screen reader | Logical reading order? | Meaningful sequence |
| Reduced motion | Respects preference? | No forced animation |

**Failure Examples**:
- Risk level only shown by color
- Focus indicator invisible
- Animations ignore prefers-reduced-motion

### 6. Performance

| Check | Question | Pass Criteria |
|-------|----------|---------------|
| Load time | Page loads within limit? | < 3 seconds |
| Interaction response | Interactions feel responsive? | < 100ms perceived |
| No blocking | No blocking operations? | UI remains responsive |

**Failure Examples**:
- Page hangs during API call
- Buttons unresponsive
- Slow chart rendering

### 7. Integration

| Check | Question | Pass Criteria |
|-------|----------|---------------|
| No errors | Code runs without errors? | No console errors |
| Data flows | State passes between pages? | Correct values |
| API contracts | API calls use correct contracts? | Matches backend |

**Failure Examples**:
- JavaScript errors in console
- Selected actions not passed to simulation
- Wrong API endpoint called

### 8. Standards Compliance

| Check | Question | Pass Criteria |
|-------|----------|---------------|
| Code standards | Follows CODE_STANDARDS.md? | Compliant |
| Design standards | Follows DESIGN_STANDARDS.md? | Compliant |
| Naming conventions | Uses correct conventions? | Consistent |

**Failure Examples**:
- Inline styles instead of CSS classes
- Hardcoded colors instead of tokens
- Undocumented session state keys

---

## Severity Levels

| Severity | Definition | Action |
|----------|------------|--------|
| Critical | Could lead to wrong decision | Block, fix immediately |
| Major | Degrades decision quality | Fix before release |
| Minor | Suboptimal but functional | Fix in next iteration |

---

## Review Outcome

### APPROVED

All criteria pass, or only minor issues remain.

```
✅ APPROVED
- All critical criteria passed
- Minor issues logged for follow-up: [list]
```

### REVISION REQUIRED

Major issues that must be fixed.

```
⚠️ REVISION REQUIRED
- Issues found:
  - [Issue 1] (Major)
  - [Issue 2] (Major)
- Return to Phase 2
- Re-review after fixes
```

### ROLLBACK REQUIRED

Critical failures requiring code reversion.

```
🚫 ROLLBACK REQUIRED
- Critical failures:
  - [Failure 1]
- Changes must be reverted
- Root cause analysis required
```

---

*These criteria exist to protect users. Apply them consistently.*
