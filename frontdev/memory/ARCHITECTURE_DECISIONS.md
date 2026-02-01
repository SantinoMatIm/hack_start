# Architecture Decision Records

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This document records significant architectural decisions affecting the frontend. Each decision is logged with context, options considered, outcome, and rationale.

---

## ADR Format

```
## ADR-{number}: {Title}

**Date**: YYYY-MM-DD
**Status**: Proposed | Accepted | Deprecated | Superseded by ADR-{n}
**Context**: [Why this decision was needed]
**Options Considered**:
1. [Option A]
2. [Option B]
**Decision**: [What was decided]
**Rationale**: [Why this option]
**Consequences**: [What this means going forward]
```

---

## Current ADRs

### ADR-007: Migration to Next.js

**Date**: 2026-01-31
**Status**: Accepted

**Context**: 
The Streamlit-based frontend (ADR-001) served well for rapid prototyping but showed significant limitations as requirements evolved:
- Limited UI/UX customization capabilities
- Full page re-renders on every interaction
- Difficulty implementing complex interactivity
- Professional B2B/B2G users expect premium interfaces
- Streamlit's component model constrains design possibilities

**Options Considered**:
1. Continue with Streamlit + more CSS hacks
2. Vue.js 3 + Nuxt
3. React + Next.js + shadcn/ui
4. SvelteKit

**Decision**: Next.js 16 + TypeScript + Tailwind CSS + shadcn/ui + Recharts

**Rationale**:
- **Full UI control**: Pixel-perfect customization without framework constraints
- **shadcn/ui**: Premium component library inspired by Linear/Vercel/Stripe aesthetic
- **TypeScript**: Type safety reduces bugs and improves developer experience
- **Tailwind CSS**: Rapid styling with design token system
- **Recharts**: React-native charting that integrates seamlessly
- **Large ecosystem**: Easier to find solutions, components, and developers
- **Backend unchanged**: FastAPI REST API works identically with any frontend

**Consequences**:
- Supersedes ADR-001 (Streamlit)
- Updates ADR-003 (CSS system now Tailwind + CSS variables)
- Updates ADR-004 (API client now TypeScript in `src/lib/api/`)
- Updates ADR-005 (State now React hooks + localStorage)
- Frontend code now in `frontend/` directory
- Streamlit code in `dashboard/` kept for reference but deprecated
- All frontend governance documents updated for new stack

---

### ADR-002: Multi-Page Application Structure

**Date**: 2024-01-01
**Status**: Accepted (Updated for Next.js)

**Context**:
The decision workflow has distinct phases: view risk → review actions → run simulation. Needed to determine single-page vs multi-page approach.

**Options Considered**:
1. Single page with tabs/sections
2. Multi-page with distinct routes
3. Hybrid with conditional rendering

**Decision**: Multi-page with Next.js App Router

**Rationale**:
- Clear separation of decision phases
- URL-based navigation for bookmarking/sharing
- Better code organization
- Aligns with user mental model (sequential workflow)

**Consequences** (Updated):
- Routes: `/`, `/risk`, `/actions`, `/simulation`
- State shared via localStorage for cross-page persistence
- Each page is a separate entry point (handles missing context gracefully)

---

### ADR-003: Design Token System

**Date**: 2024-01-01
**Status**: Accepted (Updated for Tailwind)

**Context**:
Enterprise/government users expect premium visual treatment. Need consistent design language.

**Options Considered**:
1. Raw CSS values
2. CSS variables with custom file
3. Tailwind CSS with CSS variables
4. CSS-in-JS (styled-components, emotion)

**Decision**: Tailwind CSS + CSS variables in `globals.css`

**Rationale**:
- Tailwind provides rapid development with utility classes
- CSS variables enable theming (dark mode ready)
- shadcn/ui uses this pattern (consistency)
- Design tokens defined once, used everywhere

**Consequences** (Updated):
- All colors, spacing, typography via Tailwind utilities
- Custom values in CSS variables (`--risk-critical`, etc.)
- No inline styles; use `className` with Tailwind
- Use `cn()` utility for conditional classes

---

### ADR-004: API Client Abstraction

**Date**: 2024-01-01
**Status**: Accepted (Updated for TypeScript)

**Context**:
Frontend needs to communicate with FastAPI backend. Needed to determine how API calls are structured.

**Options Considered**:
1. Direct fetch calls in each component
2. Centralized API client module
3. React Query / SWR
4. GraphQL client

**Decision**: Centralized TypeScript API client in `src/lib/api/`

**Rationale**:
- Single place for API logic
- TypeScript types match backend schemas
- Consistent error handling
- Demo mode fallback centralized
- Easy to add caching later (React Query compatible)

**Consequences** (Updated):
- API client in `frontend/src/lib/api/client.ts`
- Types in `frontend/src/lib/api/types.ts`
- All components import from `@/lib/api`
- Demo data included for offline development

---

### ADR-005: Client State Management

**Date**: 2024-01-01
**Status**: Accepted (Updated for React)

**Context**:
Need to manage client state across components and pages.

**Options Considered**:
1. React Context
2. Zustand
3. Redux
4. React hooks + localStorage

**Decision**: React hooks (useState, useEffect) + localStorage

**Rationale**:
- Simple approach sufficient for current complexity
- localStorage enables cross-page state (selected actions → simulation)
- No additional dependencies
- Can evolve to Zustand if needed later

**Consequences** (Updated):
- Component state via useState
- Cross-page state via localStorage
- Shareable state via URL searchParams where appropriate
- No global state management library (yet)

---

## Pending Decisions

### ADR-006: Uncertainty Visualization Approach

**Date**: Pending
**Status**: Proposed

**Context**:
Current implementation shows point estimates (e.g., "24 days to critical"). Decision fidelity principles require visible uncertainty.

**Options Considered**:
1. Confidence intervals in text (e.g., "24 ± 5 days")
2. Range visualization (e.g., progress bar with range)
3. Fan charts for projections
4. Qualitative confidence labels (High/Medium/Low confidence)

**Decision**: Pending session work

**Rationale**: TBD

**Consequences**: TBD

---

## Superseded Decisions

### ADR-001: Streamlit as Frontend Framework

**Date**: 2024-01-01 (Project inception)
**Status**: Superseded by ADR-007

**Context**: 
The platform needed a rapid-development frontend capable of displaying climate data, risk assessments, and interactive simulations for enterprise/government users.

**Options Considered**:
1. React with custom components
2. Streamlit with Python
3. Dash (Plotly)
4. Gradio

**Decision**: Streamlit with Python

**Rationale**:
- Python ecosystem alignment with backend (FastAPI, pandas, numpy)
- Rapid prototyping for pilot phase
- Built-in components for data display
- Lower frontend specialization barrier
- Acceptable for B2B/B2G internal tools

**Consequences**:
- ~~Limited customization compared to React~~ → **Superseded: Now using Next.js**
- ~~Constrained by Streamlit component model~~ → **Superseded**
- ~~Custom interactivity requires workarounds~~ → **Superseded**

**Supersession Note**: As the platform matured, Streamlit's limitations became blockers for professional UI/UX. See ADR-007 for migration to Next.js.

---

## How to Add an ADR

1. Assign next sequential number
2. Fill out all sections
3. Get approval during session Phase 1 or Phase 3
4. Update this file
5. Reference ADR number in code comments where relevant

---

*Architecture decisions persist beyond individual sessions. They are institutional memory.*
