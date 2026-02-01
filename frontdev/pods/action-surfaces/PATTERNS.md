# Action Surfaces Pod - Patterns

**Frontend Decision Intelligence Engineering Organization**

---

## Heuristic Reference

### Heuristic Definitions

```python
HEURISTICS = {
    "H1": {
        "name": "Moderate Industrial Reduction",
        "trigger": "SPI -1.0 to -1.5, Stable/Worsening, Days > 45",
        "impact": "5% reduction → +3 days to critical",
        "actions": ["H1_INDUSTRIAL_AUDIT", "H1_RECYCLING_MANDATE"]
    },
    "H2": {
        "name": "Urban Network Pressure Management",
        "trigger": "SPI -1.2 to -1.8, Worsening, Days 30-45",
        "impact": "10% pressure reduction → +4 days",
        "actions": ["H2_PRESSURE_REDUCTION", "H2_LEAK_DETECTION"]
    },
    "H3": {
        "name": "Targeted Public Communication",
        "trigger": "SPI -1.0 to -2.0, Worsening, Days > 30",
        "impact": "3% domestic reduction → +2 days",
        "actions": ["H3_AWARENESS_CAMPAIGN", "H3_SCHOOL_PROGRAM", "H3_HOTLINE_LAUNCH"]
    },
    "H4": {
        "name": "Restriction of Non-Essential Uses",
        "trigger": "SPI ≤ -1.8, Worsening, Days < 30",
        "impact": "1% removed → +1.3 days",
        "actions": ["H4_LAWN_BAN", "H4_CARWASH_RESTRICTION", "H4_POOL_RESTRICTION", "H4_FOUNTAIN_SHUTDOWN"]
    },
    "H5": {
        "name": "Operational Source Reallocation",
        "trigger": "SPI ≤ -2.0, Stable/Worsening, Days 15-30",
        "impact": "5% supply increase → +5 days",
        "actions": ["H5_EMERGENCY_WELLS", "H5_TANKER_DEPLOYMENT", "H5_INTERBASIN_TRANSFER"]
    },
    "H6": {
        "name": "Automatic Severity Escalation",
        "trigger": "SPI crosses threshold, Days drop >20% in 2 weeks",
        "impact": "Combined effects × 0.8 (20% penalty)",
        "actions": ["H6_EMERGENCY_DECLARATION"]
    }
}
```

### Get Heuristic Pattern

```python
def get_heuristic_for_action(action_code: str) -> Optional[dict]:
    """Get heuristic info for an action code."""
    heuristic_id = action_code.split("_")[0] if "_" in action_code else None
    return HEURISTICS.get(heuristic_id)
```

---

## Priority Badge Pattern

### Priority Configuration

```python
PRIORITY_CONFIG = {
    "HIGH": {
        "css_class": "high",
        "color": "#E76237",
        "text_color": "#FFFFFF",
        "label": "HIGH"
    },
    "MEDIUM": {
        "css_class": "medium",
        "color": "#F59E0B",
        "text_color": "#292929",
        "label": "MEDIUM"
    },
    "LOW": {
        "css_class": "low",
        "color": "#D9D7CC",
        "text_color": "#292929",
        "label": "LOW"
    }
}
```

### Render Pattern

```python
def render_priority_badge(priority: str) -> None:
    """Render priority badge."""
    config = PRIORITY_CONFIG.get(priority.upper(), PRIORITY_CONFIG["MEDIUM"])
    st.markdown(f"""
    <span class="action-priority {config['css_class']}">
        {config['label']}
    </span>
    """, unsafe_allow_html=True)
```

---

## Action Card Pattern

### Full Card Render

```python
def render_action_card(action: dict, index: int) -> None:
    """Render a single action card."""
    code = action.get("code", action.get("base_action_id", f"action_{index}"))
    title = action.get("title", "Untitled Action")
    params = action.get("parameters", {})
    justification = action.get("justification", "")
    effect = action.get("expected_effect", "")
    priority = params.get("priority_level", "MEDIUM")
    
    st.markdown(f"""
    <div class="action-card">
        <span class="action-priority {priority.lower()}">{priority}</span>
        <h3 style="margin: 16px 0 4px;">{title}</h3>
        <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 16px;">
            {code}
        </div>
        
        <div style="margin-bottom: 16px;">
            <strong>Parameters:</strong>
            <ul style="margin: 8px 0; padding-left: 20px;">
                {render_params_list(params)}
            </ul>
        </div>
        
        <div style="font-weight: 600; color: var(--action-primary); margin-bottom: 16px;">
            Expected Effect: {effect}
        </div>
        
        <div style="background: var(--bg-primary); padding: 12px; font-size: 14px;">
            {justification}
        </div>
    </div>
    """, unsafe_allow_html=True)
```

---

## Selection Pattern

### Current Pattern (With Friction)

```python
# Current: Separate checkbox column
col1, col2 = st.columns([0.05, 0.95])
with col1:
    selected = st.checkbox("", value=True, key=f"select_{code}")
with col2:
    render_action_card(action, i)
```

### Improved Pattern (Proposed)

```python
# Improved: Integrated selection with visual feedback
def render_selectable_action_card(action: dict, index: int, selected: bool) -> bool:
    """Render action card with integrated selection."""
    code = action.get("code")
    
    # Card with selection state
    selected_class = "selected" if selected else ""
    
    st.markdown(f"""
    <div class="action-card {selected_class}" data-action="{code}">
        <div class="selection-indicator">
            {'✓' if selected else '○'}
        </div>
        <!-- Rest of card content -->
    </div>
    """, unsafe_allow_html=True)
    
    return st.checkbox(
        f"Select {code}",
        value=selected,
        key=f"select_{code}",
        label_visibility="collapsed"
    )
```

---

## Parameter Display Pattern

### Parameter Formatting

```python
def format_parameter(key: str, value: any) -> str:
    """Format a parameter for display."""
    # Human-readable key names
    key_labels = {
        "reduction_percentage": "Reduction",
        "duration_days": "Duration",
        "priority_level": "Priority",
        "hours_per_day": "Hours/Day",
        "enforcement_level": "Enforcement",
        "target_reduction_percent": "Target Reduction",
        "pressure_reduction_percent": "Pressure Reduction"
    }
    
    label = key_labels.get(key, key.replace("_", " ").title())
    
    # Format value based on type
    if isinstance(value, float) and "percent" in key.lower():
        formatted = f"{value:.1f}%"
    elif isinstance(value, list):
        formatted = ", ".join(str(v) for v in value)
    elif key == "duration_days":
        formatted = f"{value} days"
    else:
        formatted = str(value)
    
    return f"<li><strong>{label}:</strong> {formatted}</li>"
```

---

## Heuristic Explanation Pattern

### Expander Pattern

```python
def render_heuristic_explanation(heuristic_id: str) -> None:
    """Render heuristic explanation."""
    heuristic = HEURISTICS.get(heuristic_id)
    if not heuristic:
        return
    
    st.markdown(f"""
    ### {heuristic['name']}
    
    **Trigger Condition:**  
    {heuristic['trigger']}
    
    **Impact Formula:**  
    {heuristic['impact']}
    
    **Associated Actions:**  
    {', '.join(heuristic['actions'])}
    
    ---
    
    This heuristic is part of the platform's fixed decision logic. 
    The AI does not invent new heuristics — it parameterizes actions 
    within these defined rules.
    """)
```

---

## Demo Data Pattern

```python
DEMO_ACTIONS = [
    {
        "base_action_id": "H4_LAWN_BAN",
        "code": "H4_LAWN_BAN",
        "title": "Lawn/Garden Irrigation Restriction",
        "parameters": {
            "reduction_percentage": 15.0,
            "duration_days": 30,
            "priority_level": "HIGH",
            "enforcement_level": "mandatory"
        },
        "justification": "SPI -1.72, WORSENING trend, 24 days to critical. Non-essential restrictions provide immediate impact.",
        "expected_effect": "+19 days to critical threshold"
    },
    # ... more demo actions
]
```

---

*Patterns ensure consistency. Propose changes through sessions.*
