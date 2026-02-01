# Risk Surfaces Pod - Patterns

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This document captures patterns and conventions specific to the Risk Surfaces Pod.

---

## Risk Level Mapping

### Standard Mapping

```python
RISK_LEVEL_CONFIG = {
    "CRITICAL": {
        "color": "#DC2626",
        "css_class": "critical",
        "icon": "🔴",
        "urgency": "immediate",
        "spi_range": "≤ -1.5"
    },
    "HIGH": {
        "color": "#E76237",
        "css_class": "high", 
        "icon": "🟠",
        "urgency": "action_recommended",
        "spi_range": "-1.5 to -1.0"
    },
    "MEDIUM": {
        "color": "#F59E0B",
        "css_class": "medium",
        "icon": "🟡",
        "urgency": "monitoring",
        "spi_range": "-1.0 to -0.5"
    },
    "LOW": {
        "color": "#10B981",
        "css_class": "low",
        "icon": "🟢",
        "urgency": "normal",
        "spi_range": "> -0.5"
    }
}
```

### Usage Pattern

```python
def get_risk_config(risk_level: str) -> dict:
    """Get configuration for a risk level."""
    return RISK_LEVEL_CONFIG.get(risk_level.upper(), RISK_LEVEL_CONFIG["LOW"])

# Example usage
config = get_risk_config(risk_data["risk_level"])
st.markdown(f'<div class="risk-card {config["css_class"]}">')
```

---

## Trend Display Pattern

### Trend Indicators

```python
TREND_CONFIG = {
    "IMPROVING": {
        "icon": "📈",
        "label": "Improving",
        "color": "#10B981",
        "description": "Conditions getting better"
    },
    "STABLE": {
        "icon": "➡️",
        "label": "Stable",
        "color": "#7E8076",
        "description": "Conditions holding steady"
    },
    "WORSENING": {
        "icon": "📉",
        "label": "Worsening",
        "color": "#DC2626",
        "description": "Conditions deteriorating"
    }
}
```

### Trend + Risk Combination

When displaying trend with risk, consider the combination:

| Risk | Trend | Urgency Amplification |
|------|-------|----------------------|
| HIGH | WORSENING | Maximum urgency |
| HIGH | STABLE | High urgency |
| HIGH | IMPROVING | Cautious optimism |
| CRITICAL | Any | Maximum urgency always |

---

## Days-to-Critical Display Pattern

### Current Pattern

```python
def format_days_to_critical(days: int) -> str:
    """Format days to critical with appropriate labeling."""
    if days < 0:
        return "Critical threshold reached"
    elif days < 15:
        return f"~{days} days (URGENT)"
    elif days < 30:
        return f"~{days} days"
    else:
        return f"~{days} days (estimated)"
```

### Proposed Urgency Escalation Pattern (GAP-001)

```python
def get_urgency_tier(days: int) -> dict:
    """Get urgency tier configuration."""
    if days < 15:
        return {
            "tier": "critical",
            "css_class": "urgency-critical",
            "animate": True,
            "size_multiplier": 1.2
        }
    elif days < 30:
        return {
            "tier": "high",
            "css_class": "urgency-high",
            "animate": False,
            "size_multiplier": 1.1
        }
    elif days < 45:
        return {
            "tier": "medium",
            "css_class": "urgency-medium",
            "animate": False,
            "size_multiplier": 1.0
        }
    else:
        return {
            "tier": "low",
            "css_class": "urgency-low",
            "animate": False,
            "size_multiplier": 1.0
        }
```

---

## Risk Card Pattern

### Structure

```html
<div class="risk-card {risk_level}">
    <!-- Header: Zone + Profile context -->
    <div class="risk-card-header">
        <span>Zone: {zone_id}</span>
        <span>{profile}</span>
    </div>
    
    <!-- Metrics Row -->
    <div class="metrics-row">
        <div class="metric">
            <div class="metric-value {risk_class}">{spi}</div>
            <div class="metric-label">SPI-6m</div>
        </div>
        <div class="metric">
            <div class="metric-value {risk_class}">{risk_level}</div>
            <div class="metric-label">Risk Level</div>
        </div>
        <div class="metric">
            <div class="metric-value">{trend_icon} {trend}</div>
            <div class="metric-label">Trend</div>
        </div>
        <div class="metric">
            <div class="metric-value {urgency_class}">{days}</div>
            <div class="metric-label">Days to Critical</div>
        </div>
    </div>
</div>
```

### Accessibility Pattern

```python
def render_risk_card_accessible(risk_data: dict) -> None:
    """Render risk card with accessibility considerations."""
    risk_level = risk_data.get("risk_level", "LOW")
    
    # Always include text label with color
    # Use aria-label for screen readers
    st.markdown(f"""
    <div class="risk-card {risk_level.lower()}" 
         role="region" 
         aria-label="Risk assessment for {risk_data.get('zone_id', 'zone')}">
        <span class="sr-only">
            Current risk level is {risk_level}. 
            SPI is {risk_data.get('spi_6m')}. 
            Trend is {risk_data.get('trend')}.
            Approximately {risk_data.get('days_to_critical')} days to critical threshold.
        </span>
        <!-- Visual content -->
    </div>
    """, unsafe_allow_html=True)
```

---

## SPI Gauge Pattern

### Gauge Configuration

```python
SPI_GAUGE_CONFIG = {
    "min": -3.0,
    "max": 0.5,
    "thresholds": {
        "critical": -1.5,
        "high": -1.0,
        "medium": -0.5,
        "low": 0.0
    },
    "colors": {
        "critical_zone": "#DC2626",
        "high_zone": "#E76237",
        "medium_zone": "#F59E0B",
        "low_zone": "#10B981"
    }
}
```

### Gauge Rendering Pattern

```python
def render_spi_gauge(spi_value: float) -> None:
    """Render SPI gauge with current value marker."""
    # Normalize value to 0-100 percentage
    min_val = SPI_GAUGE_CONFIG["min"]
    max_val = SPI_GAUGE_CONFIG["max"]
    percentage = ((spi_value - min_val) / (max_val - min_val)) * 100
    percentage = max(0, min(100, percentage))  # Clamp
    
    st.markdown(f"""
    <div class="spi-gauge" role="meter" 
         aria-valuenow="{spi_value}" 
         aria-valuemin="{min_val}" 
         aria-valuemax="{max_val}"
         aria-label="SPI gauge showing current value of {spi_value}">
        <div class="spi-marker" style="left: {percentage}%;"></div>
    </div>
    <div class="spi-labels">
        <span>Critical (-3.0)</span>
        <span>Low (0.5)</span>
    </div>
    """, unsafe_allow_html=True)
```

---

## History Chart Pattern

### Chart Configuration

```python
def create_risk_history_chart(history: list) -> go.Figure:
    """Create risk history chart with threshold areas."""
    fig = go.Figure()
    
    # Add threshold areas (background)
    fig.add_hrect(y0=-3, y1=-1.5, fillcolor="rgba(220, 38, 38, 0.1)", line_width=0)
    fig.add_hrect(y0=-1.5, y1=-1.0, fillcolor="rgba(231, 98, 55, 0.1)", line_width=0)
    fig.add_hrect(y0=-1.0, y1=-0.5, fillcolor="rgba(245, 158, 11, 0.1)", line_width=0)
    
    # Add data line
    dates = [h.get("date") for h in history]
    values = [h.get("spi_6m") for h in history]
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines+markers',
        name='SPI-6m',
        line=dict(color='#292929', width=2),
        marker=dict(size=6)
    ))
    
    # Styling
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='#F2EDE9',
        font=dict(family="system-ui", color="#292929"),
        xaxis=dict(title="Date", showgrid=True, gridcolor='rgba(0,0,0,0.05)'),
        yaxis=dict(title="SPI-6 Month", showgrid=True, gridcolor='rgba(0,0,0,0.05)', range=[-3, 0.5]),
        margin=dict(l=60, r=40, t=40, b=60),
        showlegend=False,
        height=300
    )
    
    return fig
```

---

## Error Handling Pattern

### API Error Pattern

```python
def fetch_and_display_risk(zone_id: str) -> Optional[dict]:
    """Fetch risk data with proper error handling."""
    api = get_api_client()
    
    with st.spinner("Loading risk data..."):
        risk_data = api.get_current_risk(zone_id)
    
    if not risk_data or "error" in risk_data:
        st.error("Unable to fetch risk data. Please ensure the API server is running.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Retry"):
                st.rerun()
        with col2:
            if st.button("Show Demo Data"):
                return get_demo_risk_data(zone_id)
        return None
    
    return risk_data
```

### Demo Data Pattern

```python
DEMO_RISK_DATA = {
    "cdmx": {
        "zone_id": "cdmx",
        "spi_6m": -1.72,
        "risk_level": "HIGH",
        "trend": "WORSENING",
        "days_to_critical": 24,
        "calculated_at": "2024-01-15T10:30:00Z"
    },
    "monterrey": {
        "zone_id": "monterrey",
        "spi_6m": -1.45,
        "risk_level": "HIGH",
        "trend": "STABLE",
        "days_to_critical": 38,
        "calculated_at": "2024-01-15T10:30:00Z"
    }
}

def get_demo_risk_data(zone_id: str) -> dict:
    """Get demo risk data for a zone."""
    return DEMO_RISK_DATA.get(zone_id, DEMO_RISK_DATA["cdmx"])
```

---

*Patterns ensure consistency within the pod. Follow them or propose changes.*
