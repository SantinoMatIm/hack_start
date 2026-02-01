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

### ADR-001: Streamlit as Frontend Framework

**Date**: 2024-01-01 (Project inception)
**Status**: Accepted

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
- Limited customization compared to React
- Constrained by Streamlit component model
- Custom interactivity requires workarounds (HTML/JS injection)
- Acceptable trade-off for pilot phase; may revisit for scale

---

### ADR-002: Multi-Page Application Structure

**Date**: 2024-01-01
**Status**: Accepted

**Context**:
The decision workflow has distinct phases: view risk → review actions → run simulation. Needed to determine single-page vs multi-page approach.

**Options Considered**:
1. Single page with tabs/sections
2. Multi-page with Streamlit pages feature
3. Hybrid with conditional rendering

**Decision**: Multi-page with Streamlit pages

**Rationale**:
- Clear separation of decision phases
- URL-based navigation for bookmarking/sharing
- Simpler state management per page
- Aligns with user mental model (sequential workflow)

**Consequences**:
- Session state must be carefully managed across pages
- Navigation requires explicit handling
- Each page is a separate entry point (must handle missing context)

---

### ADR-003: CSS-Based Design System

**Date**: 2024-01-01
**Status**: Accepted

**Context**:
Streamlit's default styling is functional but generic. Enterprise/government users expect premium visual treatment.

**Options Considered**:
1. Streamlit default styling
2. Custom CSS file with design tokens
3. Third-party Streamlit themes
4. Component-level inline styles

**Decision**: Custom CSS file with design tokens

**Rationale**:
- Full control over visual language
- Design tokens enable consistency
- Single source of truth for styling
- Can evolve without changing component code

**Consequences**:
- Must maintain CSS file
- Streamlit version upgrades may break selectors
- HTML injection required for custom components
- Acceptable complexity for premium appearance

---

### ADR-004: API Client Abstraction

**Date**: 2024-01-01
**Status**: Accepted

**Context**:
Frontend needs to communicate with FastAPI backend. Needed to determine how API calls are structured.

**Options Considered**:
1. Direct httpx calls in each page
2. Centralized API client class
3. GraphQL client

**Decision**: Centralized API client class in `utils/api_client.py`

**Rationale**:
- Single place for API logic
- Consistent error handling
- Easy to mock for testing
- Demo mode fallback centralized

**Consequences**:
- All pages depend on API client
- Changes to API require client updates
- Good abstraction boundary maintained

---

### ADR-005: Session State for Client State

**Date**: 2024-01-01
**Status**: Accepted

**Context**:
Streamlit reruns scripts on each interaction. State must persist across reruns.

**Options Considered**:
1. URL query parameters
2. Streamlit session_state
3. Browser localStorage (via JS)
4. Server-side session storage

**Decision**: Streamlit session_state

**Rationale**:
- Native Streamlit feature
- Simple key-value API
- Persists across reruns
- Sufficient for current needs

**Consequences**:
- State lost on browser refresh (by design)
- State keys must be managed carefully
- No persistence across sessions (acceptable for decision tool)

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

*None yet. Decisions that are superseded will be marked and linked to their replacement.*

---

## How to Add an ADR

1. Assign next sequential number
2. Fill out all sections
3. Get approval during session Phase 1 or Phase 3
4. Update this file
5. Reference ADR number in code comments where relevant

---

*Architecture decisions persist beyond individual sessions. They are institutional memory.*
