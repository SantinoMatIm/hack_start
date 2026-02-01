# INTENT

## Session: 2026-01-31-design-density

---

## Current State

The landing page has a clean, professional aesthetic established in the previous session. However, the visual execution creates a **sparse, undersized appearance**:

### Hero Section
- Height: `min-height: 50vh` — occupies half the viewport
- Content: Small centered text with large empty margins
- Display text: `clamp(48px, 6vw, 64px)` — appears small on larger screens
- Body text: `17px` — adequate but gets lost in the space

### Zone/Profile Selectors  
- Card padding: `16px 20px` — minimal for touch targets
- Icon containers: `32px × 32px` — undersized
- Text: `13px` subtitles — too small
- Overall: Cards appear cramped within their space

### Navigation Cards
- Padding: `24px` — adequate but cards feel small
- Icon containers: `40px × 40px` — could be larger
- Card descriptions: `13px` — too small to read comfortably
- Step numbers: `12px` — decorative but undersized

### Typography Scale
- Base: `15px` — on the small side for a decision interface
- Section titles: `24px` — could be more prominent
- Overall: Interface reads as "webapp" not "decision platform"

---

## Identified Gaps

| Gap | Impact on Decision-Making | Severity |
|-----|---------------------------|----------|
| Elements undersized for viewport | Users must focus harder to read; doesn't command attention | Major |
| Excessive whitespace without purpose | Feels unfinished; doesn't communicate seriousness | Medium |
| Touch targets too small | Under stress, users may misclick | Medium |
| Insufficient visual hierarchy | Primary actions don't stand out enough | Medium |

---

## Hypotheses

1. **If we increase the hero typography by 20-30%**, then the platform will immediately communicate authority and seriousness
2. **If we enlarge selector cards with bigger icons and more padding**, then users will find selections easier and the interface will feel more substantial
3. **If we increase navigation card size and prominence**, then the decision workflow will feel more important
4. **If we reduce the hero height and add more content density**, then the page will feel purposeful rather than empty
5. **If we increase base font size to 16-17px**, then readability improves across the interface

---

## Proposed Changes

### 1. Hero Section Refinement
| Change | Current | Proposed | Rationale |
|--------|---------|----------|-----------|
| Hero height | 50vh | 40vh | Less empty space, content above fold |
| Display text size | clamp(48px, 6vw, 64px) | clamp(56px, 8vw, 80px) | +30% larger, more impactful |
| Body text size | 17px | 20px | Easier to read, more prominent |
| Badge size | 13px | 14px | More readable |

### 2. Selector Cards Enhancement
| Change | Current | Proposed | Rationale |
|--------|---------|----------|-----------|
| Card padding | 16px 20px | 20px 24px | More comfortable spacing |
| Icon size | 32px × 32px | 48px × 48px | +50% larger, more prominent |
| Icon internal size | 20px | 24px | Proportional increase |
| Subtitle text | 13px | 14px | More readable |
| Card min-height | auto | 80px | Consistent, substantial feel |

### 3. Navigation Cards Enhancement
| Change | Current | Proposed | Rationale |
|--------|---------|----------|-----------|
| Card padding | 24px | 32px | More spacious feel |
| Icon container | 40px × 40px | 56px × 56px | +40% larger |
| Icon size | 20px | 28px | Proportional |
| Card title | 17px | 20px | More prominent |
| Card description | 13px | 15px | More readable |
| Step number | 12px | 14px | More visible |

### 4. Typography Scale Increase
| Token | Current | Proposed | Change |
|-------|---------|----------|--------|
| --text-base | 15px | 16px | +1px |
| --text-lg | 17px | 18px | +1px |
| --text-xl | 20px | 22px | +2px |
| --text-2xl | 24px | 28px | +4px |

### 5. Section Spacing Optimization
| Change | Current | Proposed | Rationale |
|--------|---------|----------|-----------|
| Section padding | 40px 0 | 48px 0 | Slightly more breathing room |
| Section header margin | 32px | 24px | Tighter connection to content |

---

## Visual Direction

**Before**: Sparse, undersized, lots of empty space
**After**: Substantial, confident, intentional density

The goal is to transform from "minimal webapp" to "premium decision platform" — elements should feel weighty and important without being heavy or cluttered.

---

## Risks

1. **Over-correction**: Making elements too large could feel clunky
2. **Mobile regression**: Larger elements may not scale down gracefully
3. **Streamlit constraints**: Some sizing may fight Streamlit defaults

**Mitigation**: Test at multiple viewport sizes, use clamp() for responsive scaling

---

## Files to Modify

1. `dashboard/assets/styles.css` — Typography scale, spacing, component sizes
2. `dashboard/app.py` — Hero section markup, card markup

---

## Approval

- [x] **Human approval received to proceed to Phase 2** (2026-01-31)

---

*Proceeding to implementation.*
