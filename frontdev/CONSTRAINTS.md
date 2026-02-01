# Frontend Constraints

**Frontend Decision Intelligence Engineering Organization**

---

This document defines the technical, governance, and accessibility constraints that bound all frontend work. Constraints are non-negotiable unless explicitly amended through governance process.

---

## Technical Constraints

### Platform Stack

| Layer | Technology | Constraint |
|-------|------------|------------|
| Framework | Next.js 16+ | All UI must use React Server/Client Components as appropriate |
| Language | TypeScript | Strict mode enabled; no `any` types without justification |
| Styling | Tailwind CSS + shadcn/ui | Use design tokens; no arbitrary values without approval |
| Visualization | Recharts | Charts and graphs use Recharts; no external charting libraries without approval |
| State | React hooks + localStorage | Client state via useState/useEffect; persistence via localStorage |
| API | FastAPI backend | All data fetched via API client in `src/lib/api/client.ts` |

### Performance Boundaries

| Metric | Constraint | Rationale |
|--------|------------|-----------|
| Initial page load | < 2 seconds (LCP) | Crisis users cannot wait |
| Interaction response | < 100ms (INP) | Stress degrades patience |
| API call timeout | 10 seconds max | Fail fast, show fallback |
| Bundle size | < 200KB initial JS | Fast load on all networks |
| Core Web Vitals | Pass all metrics | Essential for user experience |

### Integration Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND BOUNDARY                       │
│                                                              │
│  frontend/src/                                               │
│  ├── app/               ← Next.js App Router pages          │
│  ├── components/        ← React components                   │
│  │   └── ui/            ← shadcn/ui base components         │
│  ├── lib/               ← Utilities and API client           │
│  │   └── api/           ← FastAPI client + types            │
│  └── styles/            ← Global CSS, design tokens          │
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
| New pages | Must go in `frontend/src/app/{route}/page.tsx` |
| Shared components | Must go in `frontend/src/components/` |
| UI primitives | Must use shadcn/ui from `frontend/src/components/ui/` |
| API calls | Must go through `frontend/src/lib/api/client.ts` |
| Styles | Must use Tailwind classes + CSS variables from `globals.css` |
| Types | Must be defined in `frontend/src/lib/api/types.ts` |

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
| Label clearly | "Demo Mode" Alert component visible |
| Use realistic values | Based on documented pilot zone profiles |
| Don't mix with live | Never blend demo and live data |

---

## Design System Constraints

### Design Tokens (from globals.css)

```css
/* Colors - Use Tailwind classes, not raw values */
--background: #FAFBFC;
--foreground: #0F172A;
--primary: #2563EB;
--muted-foreground: #64748B;

/* Risk Level Colors */
--risk-critical: #DC2626;  /* red-600 */
--risk-high: #EA580C;      /* orange-600 */
--risk-medium: #D97706;    /* amber-600 */
--risk-low: #059669;       /* emerald-600 */
```

### Typography

Use Tailwind typography utilities:

| Element | Tailwind Class | Weight |
|---------|----------------|--------|
| Display | `text-5xl md:text-6xl` | font-extrabold |
| H1 | `text-3xl md:text-4xl` | font-bold |
| H2 | `text-2xl md:text-3xl` | font-bold |
| H3 | `text-lg md:text-xl` | font-semibold |
| Body | `text-base` | font-normal |
| Caption | `text-sm` | font-medium |

### Shapes

| Constraint | Value |
|------------|-------|
| Border radius | Use shadcn/ui defaults (--radius) |
| Borders | `border` class with default color |
| Shadows | `shadow-sm`, `shadow-md`, `shadow-lg` |

### Motion

| Constraint | Value |
|------------|-------|
| Default duration | 200ms |
| Slow duration | 400ms |
| Easing | Tailwind defaults |
| Reduced motion | Must be respected with `motion-safe:` prefix |

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
