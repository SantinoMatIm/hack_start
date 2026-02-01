# Code Standards

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This document defines the code quality standards for all frontend work. These standards ensure consistency, maintainability, and alignment with the platform's decision-support mission.

---

## Language & Framework Standards

### Python (Streamlit)

| Standard | Requirement |
|----------|-------------|
| Python version | 3.10+ |
| Type hints | Required for function signatures |
| Docstrings | Required for modules, classes, and public functions |
| Line length | 88 characters (Black default) |
| Imports | Sorted, grouped (stdlib, third-party, local) |

### Code Style

```python
# Good: Clear, typed, documented
def render_risk_card(risk_data: dict, show_trend: bool = True) -> None:
    """
    Render the primary risk card component.
    
    Args:
        risk_data: Risk assessment from API containing spi_6m, risk_level, etc.
        show_trend: Whether to display trend indicator. Defaults to True.
    
    Returns:
        None. Renders directly to Streamlit.
    """
    ...

# Bad: Unclear, untyped, undocumented
def render_card(data, flag=True):
    ...
```

---

## File Organization

### Page Structure

```python
"""
{Page Name}
{Brief description of the page's decision-support purpose}
"""

import streamlit as st
from pathlib import Path
import sys

# Path setup for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Local imports
from components.header import render_header
from utils.api_client import get_api_client

# Page configuration
st.set_page_config(
    page_title="{Page Title} | Water Risk Platform",
    page_icon="{emoji}",
    layout="wide",
)

# CSS loading
css_file = Path(__file__).parent.parent / "assets" / "styles.css"
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session state initialization
if "key" not in st.session_state:
    st.session_state.key = default_value

def main():
    """Main page logic."""
    ...

if __name__ == "__main__":
    main()
```

### Component Structure

```python
"""
{Component Name}
{Brief description of the component's role in decision-support}
"""

import streamlit as st
from typing import Optional, Dict, Any

def render_{component_name}(
    data: Dict[str, Any],
    variant: str = "default",
    **kwargs
) -> None:
    """
    Render {component description}.
    
    Args:
        data: {description}
        variant: Visual variant. Options: "default", "compact", "expanded"
        **kwargs: Additional customization options
    
    Returns:
        None. Renders directly to Streamlit.
    """
    ...
```

---

## Naming Conventions

### Files

| Type | Convention | Example |
|------|------------|---------|
| Pages | `{n}_{snake_case}.py` | `1_risk_overview.py` |
| Components | `{snake_case}.py` | `risk_display.py` |
| Utilities | `{snake_case}.py` | `api_client.py` |

### Functions

| Type | Convention | Example |
|------|------------|---------|
| Render functions | `render_{component}()` | `render_risk_card()` |
| Data fetching | `get_{resource}()` | `get_current_risk()` |
| Data processing | `process_{action}()` | `process_simulation_result()` |
| Validation | `validate_{target}()` | `validate_zone_selection()` |
| Event handlers | `handle_{event}()` | `handle_action_selection()` |

### Variables

| Type | Convention | Example |
|------|------------|---------|
| Session state keys | `snake_case` | `selected_zone` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_PROJECTION_DAYS` |
| Component props | `snake_case` | `show_trend` |

### CSS Classes

| Type | Convention | Example |
|------|------------|---------|
| Components | `{component-name}` | `risk-card` |
| Modifiers | `{component}.{modifier}` | `risk-card.critical` |
| States | `{component}.{state}` | `action-card.selected` |
| Utilities | `{property}-{value}` | `text-muted` |

---

## Session State Management

### Initialization Pattern

```python
# Always check before setting
if "key" not in st.session_state:
    st.session_state.key = default_value
```

### Documented Keys

All session state keys must be documented:

```python
# Session State Keys:
# - selected_zone: str - Currently selected zone ID ("cdmx" | "monterrey")
# - selected_profile: str - User profile ("government" | "industry")
# - current_risk: dict | None - Latest risk data from API
# - recommended_actions: list | None - Actions from API
# - selected_actions: list - Action codes selected for simulation
# - simulation_result: dict | None - Latest simulation result
```

### State Reset Pattern

```python
def reset_dependent_state():
    """Reset state that depends on zone/profile selection."""
    st.session_state.current_risk = None
    st.session_state.recommended_actions = None
    st.session_state.simulation_result = None
```

---

## API Integration

### Client Usage

```python
from utils.api_client import get_api_client

api = get_api_client()

# Always handle potential errors
risk_data = api.get_current_risk(zone_id)
if not risk_data or "error" in risk_data:
    st.error("Unable to fetch risk data.")
    # Provide fallback or demo mode option
    return
```

### Error Handling

```python
# Good: Graceful degradation with user feedback
try:
    result = api.get_recommended_actions(zone_id, profile)
    if result and "actions" in result:
        display_actions(result["actions"])
    else:
        st.warning("No actions available. Showing defaults.")
        display_demo_actions()
except Exception as e:
    st.error(f"API error: {str(e)}")
    log_error(e)  # If logging available
```

### Demo Mode

```python
# When API unavailable, provide clear demo mode
if st.button("Show Demo Data"):
    st.info("📊 Displaying demo data. Connect to API for live results.")
    demo_data = get_demo_data()
    display_data(demo_data)
```

---

## HTML/CSS in Streamlit

### Markdown with HTML

```python
# Good: Semantic, accessible, using design tokens
st.markdown("""
<div class="risk-card high">
    <div class="metric-label">Risk Level</div>
    <div class="metric-value high">HIGH</div>
</div>
""", unsafe_allow_html=True)

# Bad: Inline styles, no semantic structure
st.markdown("""
<div style="background: red; padding: 10px;">
    <span style="font-size: 24px;">HIGH</span>
</div>
""", unsafe_allow_html=True)
```

### CSS Class Usage

Always use classes from `styles.css`:

```python
# Good: Using design system classes
st.markdown('<div class="section reveal fade-up">', unsafe_allow_html=True)

# Bad: Creating one-off styles
st.markdown('<div style="padding: 48px 0; margin-bottom: 48px;">', unsafe_allow_html=True)
```

---

## Comments & Documentation

### When to Comment

```python
# Comment on WHY, not WHAT
# Bad: Increment counter
counter += 1

# Good: Track iterations for rate limiting (API allows max 10 calls/minute)
counter += 1
```

### Decision Documentation

```python
# DECISION: Using gamma distribution for SPI calculation
# Rationale: Industry standard per WMO guidelines
# See: ARCHITECTURE_DECISIONS.md #ADR-003
def calculate_spi(...):
    ...
```

### TODO Comments

```python
# TODO(session-id): Brief description of needed work
# Example:
# TODO(2026-01-31-urgency): Add animation for days-to-critical countdown
```

---

## Testing Considerations

### Component Testability

```python
# Good: Logic separated from rendering
def calculate_urgency_level(days_to_critical: int) -> str:
    """Determine urgency level from days remaining."""
    if days_to_critical < 15:
        return "critical"
    elif days_to_critical < 30:
        return "high"
    elif days_to_critical < 45:
        return "medium"
    return "low"

def render_urgency_indicator(days: int) -> None:
    """Render urgency indicator."""
    level = calculate_urgency_level(days)
    st.markdown(f'<div class="urgency-{level}">...</div>', unsafe_allow_html=True)
```

### Data Validation

```python
def validate_risk_data(data: dict) -> bool:
    """Validate risk data has required fields."""
    required = ["zone_id", "spi_6m", "risk_level", "trend", "days_to_critical"]
    return all(key in data for key in required)
```

---

## Performance Guidelines

### Avoid Redundant Computation

```python
# Bad: Recomputing on every interaction
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_risk_history(zone_id: str, days: int) -> dict:
    """Fetch and cache risk history."""
    return api.get_risk_history(zone_id, days)
```

### Minimize Re-renders

```python
# Use st.empty() for dynamic updates
placeholder = st.empty()
with placeholder.container():
    render_dynamic_content()
```

### Lazy Loading

```python
# Load heavy content only when needed
if st.button("Show detailed analysis"):
    with st.spinner("Loading..."):
        detailed_data = fetch_detailed_data()
        render_detailed_analysis(detailed_data)
```

---

## Code Review Checklist

Before Phase 3 Fidelity Review, verify:

- [ ] Type hints on all function signatures
- [ ] Docstrings on modules and public functions
- [ ] Session state keys documented
- [ ] Error handling for all API calls
- [ ] CSS classes from design system (no inline styles)
- [ ] Accessibility considerations (alt text, ARIA, focus)
- [ ] No hardcoded values (use constants or config)
- [ ] Comments explain WHY, not WHAT
- [ ] Performance considerations (caching, lazy loading)

---

*Code standards ensure maintainable, consistent frontend code that serves the decision-support mission.*
