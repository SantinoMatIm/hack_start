# INTENT

## Session: 2026-01-31-redundancy-fix

## Current State

The landing page (app.py) and sidebar contain redundant controls:
- Zone selection appears twice (sidebar dropdown + main page cards)
- Profile selection appears twice (sidebar dropdown + main page cards)  
- Navigation appears twice (sidebar buttons + main page workflow cards)
- Streamlit's default page navigation is visible and poorly styled

Visual issues exist with selected states on cards - poor contrast between icon containers and selected card backgrounds.

## Identified Gaps

| Gap | Impact on Decision-Making | Severity |
|-----|---------------------------|----------|
| Redundant controls confuse users | Users unsure which control to use | High |
| Poor contrast on selected states | Users may not clearly see what's selected | High |
| Visible Streamlit page nav | Unprofessional appearance, confusion | Medium |
| Cluttered main page | Decision workflow obscured by selection UI | Medium |

## Hypotheses

1. If we **remove zone/profile cards from main page** and keep only sidebar dropdowns, then the main page becomes cleaner and focused on the decision workflow
2. If we **remove sidebar navigation buttons** and keep main page workflow cards, then we eliminate redundancy while maintaining clear workflow progression
3. If we **hide Streamlit's default page nav** via CSS, then the interface appears more polished
4. If we **fix selected state contrast**, then users can clearly see their current selection

## Proposed Changes

| Change | Create/Modify/Delete | Rationale |
|--------|---------------------|-----------|
| Remove zone/profile selection cards from main page | Modify app.py | Eliminate redundancy; sidebar handles this |
| Remove navigation buttons from sidebar | Modify app.py | Main page workflow cards serve this purpose |
| Add CSS to hide Streamlit page navigation | Modify styles.css | Professional appearance |
| Fix selected card styling in sidebar context display | Modify styles.css | Accessibility and clarity |
| Simplify main page to hero + workflow cards | Modify app.py | Focus on decision workflow |

## Risks

- Users may miss sidebar dropdowns if not prominent enough
- Reducing main page content may feel "empty" (but recent sessions addressed density)

## Approval

- [x] Human approval received to proceed to Phase 2
