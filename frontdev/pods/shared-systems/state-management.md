# State Management Guide

**Shared Systems Pod — Frontend Decision Intelligence Organization**

---

## Purpose

This document defines patterns for session state management in the frontend.

---

## Session State Overview

Streamlit's `st.session_state` persists data across reruns within a session.

```python
# Initialize
if "key" not in st.session_state:
    st.session_state.key = default_value

# Read
value = st.session_state.key

# Write
st.session_state.key = new_value
```

---

## Registered State Keys

### Shared Systems (Global)

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `selected_zone` | str | "cdmx" | Currently selected zone ID |
| `selected_profile` | str | "government" | User profile type |

### Risk Surfaces Pod

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `current_risk` | dict \| None | None | Latest risk data from API |

### Action Surfaces Pod

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `recommended_actions` | list \| None | None | Actions from API |
| `selected_actions` | list | [] | Action codes selected for simulation |

### Simulation Surfaces Pod

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `simulation_result` | dict \| None | None | Latest simulation result |

---

## State Dependencies

```
selected_zone ──────┬──────▶ current_risk
                    │
                    └──────▶ recommended_actions ──▶ selected_actions
                                                            │
selected_profile ──────────▶ recommended_actions            │
                                                            │
                                                            ▼
                                                    simulation_result
```

### Dependency Reset Pattern

When a parent state changes, dependent states should reset:

```python
def on_zone_change():
    """Reset dependent state when zone changes."""
    st.session_state.current_risk = None
    st.session_state.recommended_actions = None
    st.session_state.selected_actions = []
    st.session_state.simulation_result = None

def on_profile_change():
    """Reset dependent state when profile changes."""
    st.session_state.recommended_actions = None
    st.session_state.selected_actions = []
    st.session_state.simulation_result = None
```

---

## Initialization Pattern

### Per-Page Initialization

Each page should initialize keys it needs:

```python
# Risk Overview page
if "selected_zone" not in st.session_state:
    st.session_state.selected_zone = "cdmx"
if "selected_profile" not in st.session_state:
    st.session_state.selected_profile = "government"
if "current_risk" not in st.session_state:
    st.session_state.current_risk = None
```

### Centralized Initialization (Proposed)

```python
# utils/state.py

def init_session_state():
    """Initialize all session state with defaults."""
    defaults = {
        "selected_zone": "cdmx",
        "selected_profile": "government",
        "current_risk": None,
        "recommended_actions": None,
        "selected_actions": [],
        "simulation_result": None,
    }
    
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default
```

---

## State Access Patterns

### Reading State

```python
# Direct access
zone = st.session_state.selected_zone

# With default
zone = st.session_state.get("selected_zone", "cdmx")

# Check existence
if st.session_state.get("current_risk"):
    display_risk()
```

### Writing State

```python
# Direct assignment
st.session_state.selected_zone = "monterrey"

# Update and rerun
st.session_state.selected_zone = "monterrey"
st.rerun()
```

### Conditional Update

```python
# Only update if different
if st.session_state.selected_zone != new_zone:
    st.session_state.selected_zone = new_zone
    on_zone_change()
    st.rerun()
```

---

## Cross-Page State Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│     app.py      │────▶│  1_risk_overview │────▶│   2_actions     │
│                 │     │                 │     │                 │
│ Sets:           │     │ Reads:          │     │ Reads:          │
│ - selected_zone │     │ - selected_zone │     │ - selected_zone │
│ - selected_     │     │ - selected_     │     │ - selected_     │
│   profile       │     │   profile       │     │   profile       │
│                 │     │ Sets:           │     │ - current_risk  │
│                 │     │ - current_risk  │     │ Sets:           │
│                 │     │                 │     │ - recommended_  │
│                 │     │                 │     │   actions       │
│                 │     │                 │     │ - selected_     │
│                 │     │                 │     │   actions       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │  3_simulation   │
                                                │                 │
                                                │ Reads:          │
                                                │ - All above     │
                                                │ Sets:           │
                                                │ - simulation_   │
                                                │   result        │
                                                └─────────────────┘
```

---

## Debugging State

### Log Current State

```python
import streamlit as st

with st.expander("Debug: Session State"):
    st.json(dict(st.session_state))
```

### State Snapshot

```python
def get_state_snapshot() -> dict:
    """Get snapshot of relevant state for debugging."""
    return {
        "zone": st.session_state.get("selected_zone"),
        "profile": st.session_state.get("selected_profile"),
        "has_risk": st.session_state.get("current_risk") is not None,
        "has_actions": st.session_state.get("recommended_actions") is not None,
        "selected_count": len(st.session_state.get("selected_actions", [])),
        "has_simulation": st.session_state.get("simulation_result") is not None,
    }
```

---

## State Persistence Limitations

### What Persists

- Within single browser session
- Across page navigation
- Across Streamlit reruns

### What Does NOT Persist

- Browser refresh (full page reload)
- New browser session
- Server restart

### For Persistent Storage

If decision history needs persistence:
- Use backend API to store decisions
- Consider browser localStorage (via JS injection)
- This is a future enhancement (GAP-003)

---

*State management is the nervous system of the frontend. Handle with care.*
