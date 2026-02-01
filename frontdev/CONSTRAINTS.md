# Frontend Constraints

**Frontend Decision Intelligence Engineering Organization**

---

This document defines the technical, governance, and accessibility constraints that bound all frontend work. Constraints are non-negotiable unless explicitly amended through governance process.

---

## Technical Constraints

### Platform Stack

| Layer | Technology | Constraint |
|-------|------------|------------|
| Framework | Streamlit | All UI must be implementable within Streamlit capabilities |
| Visualization | Plotly | Charts and graphs use Plotly; no external charting libraries without approval |
| Styling | CSS (custom) | Design system defined in `dashboard/assets/styles.css` |
| State | Streamlit session_state | All client state managed through session_state |
| API | FastAPI backend | All data fetched via API client in `dashboard/utils/api_client.py` |

### Performance Boundaries

| Metric | Constraint | Rationale |
|--------|------------|-----------|
| Initial page load | < 3 seconds | Crisis users cannot wait |
| Interaction response | < 100ms perceived | Stress degrades patience |
| API call timeout | 10 seconds max | Fail fast, show fallback |
| Bundle size | Minimize JS injection | Streamlit adds overhead; don't compound it |

### Integration Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND BOUNDARY                       │
│                                                              │
│  dashboard/                                                  │
│  ├── app.py              ← Main entry                       │
│  ├── pages/              ← Page implementations              │
│  ├── components/         ← Reusable UI components           │
│  ├── assets/             ← CSS, static assets               │
│  └── utils/              ← API client, helpers              │
│                                                              │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ HTTP/REST
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND BOUNDARY                        │
│                                                              │
│  src/api/                ← FastAPI endpoints                 │
│  src/risk_engine/        ← Risk calculations                 │
│  src/heuristics/         ← Decision heuristics               │
│  src/actions/            ← Action catalog                    │
│  src/simulation/         ← Scenario projection               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Frontend does NOT:**
- Directly access database
- Perform risk calculations
- Execute heuristic logic
- Run simulations

**Frontend DOES:**
- Call API endpoints
- Present results
- Manage UI state
- Handle user interactions

### Code Organization

| Constraint | Requirement |
|------------|-------------|
| New pages | Must go in `dashboard/pages/` with numeric prefix |
| Shared components | Must go in `dashboard/components/` |
| API calls | Must go through `utils/api_client.py` |
| Styles | Must use design tokens from `assets/styles.css` |
| State | Must use `st.session_state` keys documented in code |

---

## Governance Constraints

### Decision Heuristics Are Fixed

The platform uses 6 fixed numeric heuristics:

| Heuristic | Trigger | Impact |
|-----------|---------|--------|
| H1 | SPI -1.0 to -1.5, Days > 45 | 5% → +3 days |
| H2 | SPI -1.2 to -1.8, Days 30-45 | 10% → +4 days |
| H3 | SPI -1.0 to -2.0, Days > 30 | 3% → +2 days |
| H4 | SPI ≤ -1.8, Days < 30 | 1% → +1.3 days |
| H5 | SPI ≤ -2.0, Days 15-30 | 5% → +5 days |
| H6 | Threshold crossed | Combined × 0.8 |

**Frontend constraint:** Display heuristic logic accurately. Never simplify in ways that misrepresent triggers or impacts.

### Action Catalog Is Fixed

15 actions exist. The AI orchestrator parameterizes them but does not invent new ones.

**Frontend constraint:** Never display actions not in the catalog. Never suggest the system can create custom actions.

### AI Transparency

| AI Does | AI Does Not |
|---------|-------------|
| Parameterize actions within ranges | Invent new policies |
| Adjust percentages, durations | Create actions outside catalog |
| Justify with numeric rationale | Generate predictions beyond formulas |
| Fall back to defaults if unavailable | Operate as black box |

**Frontend constraint:** All AI-generated content must be labeled as such and traceable to inputs.

---

## Accessibility Constraints

### WCAG Compliance

| Level | Requirement | Status |
|-------|-------------|--------|
| WCAG 2.1 Level A | Mandatory | Required |
| WCAG 2.1 Level AA | Mandatory | Required |
| WCAG 2.1 Level AAA | Aspirational | Where feasible |

### Specific Requirements

| Category | Constraint |
|----------|------------|
| Color contrast | Minimum 4.5:1 for normal text, 3:1 for large text |
| Color alone | Never convey information by color alone |
| Focus states | Visible focus indicator on all interactive elements |
| Motion | Respect `prefers-reduced-motion`; provide alternatives |
| Screen readers | Logical reading order; meaningful alt text; ARIA where needed |
| Keyboard | All functionality accessible via keyboard |
| Text sizing | Support 200% zoom without horizontal scrolling |

### Crisis Usability

Beyond WCAG, consider users under stress:

| Stressor | Accommodation |
|----------|---------------|
| Reduced attention | Clear visual hierarchy, minimal distraction |
| Decision fatigue | Obvious primary action, reduced choices |
| Time pressure | Fast load, instant feedback |
| Environmental factors | High contrast options, large touch targets |

---

## Data Integrity Constraints

### What Frontend May Display

| Data Type | Source | Constraint |
|-----------|--------|------------|
| Current SPI | API `/risk/current` | Display as-is with timestamp |
| Risk level | API `/risk/current` | Use exact level from API |
| Days to critical | API `/risk/current` | Label as "estimated" |
| Recommended actions | API `/actions/recommended` | Show all fields including justification |
| Simulation results | API `/scenarios/simulate` | Show both scenarios with methodology |

### What Frontend Must NOT Do

| Prohibited | Rationale |
|------------|-----------|
| Calculate risk levels client-side | Risk engine owns this logic |
| Modify action parameters | AI orchestrator owns parameterization |
| Extrapolate beyond API data | Backend owns projections |
| Cache stale data without indication | Users need current information |
| Hide uncertainty | Violates Truth Over Comfort principle |

### Demo Mode

When API is unavailable, demo mode may show sample data:

| Constraint | Requirement |
|------------|-------------|
| Label clearly | "Demo Data" badge visible |
| Use realistic values | Based on documented pilot zone profiles |
| Don't mix with live | Never blend demo and live data |

---

## Design System Constraints

### Design Tokens (from styles.css)

```css
/* Colors - Use these tokens, not raw values */
--bg-primary: #F2EDE9;
--bg-surface: #FFFFFF;
--bg-dark: #292929;
--text-primary: #292929;
--text-inverse: #FFFFFF;
--text-muted: #7E8076;
--action-primary: #E76237;
--action-secondary: #292929;

/* Risk Level Colors */
Critical: #DC2626
High: #E76237 (--action-primary)
Medium: #F59E0B
Low: #10B981
```

### Typography

| Element | Size | Weight |
|---------|------|--------|
| Display | clamp(48px, 8vw, 90px) | 800 |
| H1 | clamp(40px, 6vw, 70px) | 800 |
| H2 | clamp(32px, 4vw, 55px) | 800 |
| H3 | clamp(24px, 3vw, 38px) | 700 |
| Body | 18px | 450 |
| Caption | 14px | 600 |

### Shapes

| Constraint | Value |
|------------|-------|
| Border radius | 0 (sharp edges) |
| Borders | 1px solid --border-default |
| Shadows | None (flat design) |

### Motion

| Constraint | Value |
|------------|-------|
| Default duration | 800ms |
| Fast duration | 200ms |
| Easing | cubic-bezier(0.4, 0, 0.2, 1) |
| Reduced motion | Must be respected |

---

## Constraint Violations

When a constraint must be violated:

1. Document the constraint being violated
2. Provide rationale for exception
3. Get explicit approval from relevant council
4. Log in session artifacts
5. Flag for governance review

Constraints evolve through deliberate process, not silent workarounds.

---

*These constraints bound all frontend work. They may be amended through governance process, but never circumvented.*
