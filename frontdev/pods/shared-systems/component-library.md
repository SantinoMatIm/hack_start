# Component Library

**Shared Systems Pod — Frontend Decision Intelligence Organization**

---

## Purpose

This document catalogs all shared components available for use across pods.

---

## Header Components

**Location**: `dashboard/components/header.py`

### render_header()

```python
def render_header(title: str, subtitle: str = "") -> None:
    """Render page header with title and optional subtitle."""
```

**Usage**:
```python
render_header("Risk Overview", "Current drought risk assessment")
```

### render_zone_selector()

```python
def render_zone_selector() -> tuple[str, str]:
    """Render sidebar zone and profile selectors. Returns (zone_id, profile)."""
```

**Usage**:
```python
zone_id, profile = render_zone_selector()
```

**Session State**: Updates `selected_zone` and `selected_profile`

### render_back_button()

```python
def render_back_button() -> None:
    """Render back navigation button."""
```

---

## Risk Display Components

**Location**: `dashboard/components/risk_display.py`  
**Owner**: Risk Surfaces Pod (shared for context display)

### render_risk_card()

```python
def render_risk_card(risk_data: dict) -> None:
    """Render full risk card with all metrics."""
```

**Props**:
- `risk_data`: API response from `/risk/current`

### render_risk_gauge()

```python
def render_risk_gauge(spi_value: float) -> None:
    """Render SPI gauge visualization."""
```

### render_risk_metrics()

```python
def render_risk_metrics(risk_data: dict) -> None:
    """Render compact risk metrics row (for use on other pages)."""
```

### render_risk_explanation()

```python
def render_risk_explanation(risk_data: dict) -> None:
    """Render contextual explanation of current risk."""
```

---

## Action Components

**Location**: `dashboard/components/action_card.py`  
**Owner**: Action Surfaces Pod

### render_action_card()

```python
def render_action_card(action: dict, index: int) -> None:
    """Render single action card."""
```

### render_action_list()

```python
def render_action_list(actions: list) -> None:
    """Render list of action cards."""
```

### render_action_summary()

```python
def render_action_summary(actions: list) -> None:
    """Render summary statistics for actions."""
```

### render_heuristic_explanation()

```python
def render_heuristic_explanation(heuristic_id: str) -> None:
    """Render explanation for H1-H6 heuristic."""
```

---

## Simulation Components

**Location**: `dashboard/components/simulation_chart.py`  
**Owner**: Simulation Surfaces Pod

### render_simulation_comparison()

```python
def render_simulation_comparison(simulation: dict) -> None:
    """Render side-by-side scenario comparison."""
```

### render_projection_chart()

```python
def render_projection_chart(simulation: dict, projection_days: int) -> None:
    """Render timeline projection chart."""
```

### render_impact_breakdown()

```python
def render_impact_breakdown(simulation: dict) -> None:
    """Render per-action impact breakdown."""
```

### render_decision_summary()

```python
def render_decision_summary(simulation: dict, zone_id: str, profile: str) -> None:
    """Render decision summary and CTA."""
```

---

## Common Patterns

### Loading State

```python
with st.spinner("Loading data..."):
    data = api.fetch_data()
```

### Error State

```python
if not data or "error" in data:
    st.error("Unable to fetch data. Please check the API connection.")
    if st.button("Show Demo Data"):
        data = get_demo_data()
```

### Section Wrapper

```python
st.markdown('<div class="section reveal fade-up">', unsafe_allow_html=True)
# Content
st.markdown('</div>', unsafe_allow_html=True)
```

### Dark Section

```python
st.markdown("""
<div class="dark-section reveal fade-up">
    <div style="text-align: center; max-width: 600px; margin: 0 auto;">
        <h2>Section Title</h2>
        <p style="color: var(--accent-dark);">Description text</p>
    </div>
</div>
""", unsafe_allow_html=True)
```

---

## Component Creation Guidelines

### When to Create Shared Component

- Used by 2+ pods
- Represents a reusable pattern
- Encapsulates complex logic

### Component Structure

```python
"""
Component Name
Brief description of component purpose.
"""

from typing import Optional, Dict, Any
import streamlit as st

def render_component_name(
    required_param: str,
    optional_param: str = "default",
    **kwargs
) -> Optional[Any]:
    """
    Render component description.
    
    Args:
        required_param: Description
        optional_param: Description. Defaults to "default".
        **kwargs: Additional options
    
    Returns:
        Description of return value, or None if renders directly.
    """
    # Implementation
```

### Adding to Library

1. Implement in appropriate file
2. Add docstring with Args/Returns
3. Update this document
4. Notify consuming pods

---

*Shared components enable consistency. Use them; don't reinvent them.*
