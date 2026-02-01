# INTENT

## Session: 2026-01-31-ui-redesign

## Current State

The Water Risk Platform dashboard uses:
- Warm cream background (#F2EDE9)
- Orange accent color (#E76237)
- Emoji-based icons throughout
- Sharp edges (0 border-radius)
- Dramatic scroll-reveal animations
- System fonts

The aesthetic is functional but appears dated and less professional than modern B2B SaaS applications.

## Identified Gaps

| Gap | Impact on Decision-Making | Severity |
|-----|---------------------------|----------|
| Emoji icons lack professionalism | Reduces perceived authority of risk data | Major |
| Warm color palette feels casual | May not convey seriousness of decisions | Medium |
| Sharp edges feel dated | Reduces trust in platform modernity | Minor |
| Heavy animations distract | Slows information absorption | Medium |

## Hypotheses

1. If we adopt a cool, minimal color palette (slate grays, blue accents), then the platform will feel more authoritative and trustworthy because it aligns with established enterprise design patterns (Stripe, Bloomberg).

2. If we replace emojis with professional SVG icons (Lucide), then users will perceive the data as more credible because iconography matches enterprise expectations.

3. If we implement subtle micro-interactions instead of dramatic reveals, then users can focus on decision-making rather than waiting for animations because information appears instantly.

4. If we add subtle border-radius and refined shadows, then the interface will feel more modern and polished because these are current design conventions.

## Proposed Changes

| Change | Create/Modify/Delete | Rationale |
|--------|---------------------|-----------|
| `utils/icons.py` | Create | Centralized icon system with Lucide SVGs |
| `assets/styles.css` | Modify | Complete color palette and spacing overhaul |
| `app.py` | Modify | Update hero, selectors, nav cards |
| All pages | Modify | Replace emojis, update styling |
| All components | Modify | Icon integration, refined layouts |

## Risks

- Font loading delay (mitigated: Inter via Google Fonts with system fallback)
- Color contrast accessibility (mitigated: all colors checked for WCAG AA)
- Breaking existing layouts (mitigated: tested core flows)

## Approval

- [x] Human approval received to proceed to Phase 2
