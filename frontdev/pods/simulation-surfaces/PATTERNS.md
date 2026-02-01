# Simulation Surfaces Pod - Patterns

**Frontend Decision Intelligence Engineering Organization**

---

## Comparison Card Pattern

### No-Action Card

```python
def render_no_action_card(scenario: dict) -> None:
    """Render the no-action scenario card."""
    st.markdown(f"""
    <div class="comparison-card no-action">
        <div class="comparison-label">NO ACTION</div>
        
        <div class="scenario-metrics">
            <div class="metric">
                <div class="metric-value">{scenario.get('projected_spi', 'N/A')}</div>
                <div class="metric-label">Projected SPI</div>
            </div>
            <div class="metric">
                <div class="metric-value critical">{scenario.get('projected_risk_level', 'N/A')}</div>
                <div class="metric-label">Risk Level</div>
            </div>
            <div class="metric">
                <div class="metric-value">{scenario.get('days_to_critical', 'N/A')}</div>
                <div class="metric-label">Days to Critical</div>
            </div>
        </div>
        
        <div class="scenario-description">
            {scenario.get('description', '')}
        </div>
    </div>
    """, unsafe_allow_html=True)
```

### With-Action Card

```python
def render_with_action_card(scenario: dict, total_days_gained: int) -> None:
    """Render the with-action scenario card."""
    st.markdown(f"""
    <div class="comparison-card with-action">
        <div class="comparison-label">WITH ACTION</div>
        
        <div class="scenario-metrics">
            <div class="metric">
                <div class="metric-value">{scenario.get('projected_spi', 'N/A')}</div>
                <div class="metric-label">Projected SPI</div>
            </div>
            <div class="metric">
                <div class="metric-value">{scenario.get('projected_risk_level', 'N/A')}</div>
                <div class="metric-label">Risk Level</div>
            </div>
            <div class="metric">
                <div class="metric-value">{scenario.get('days_to_critical', 'N/A')}</div>
                <div class="metric-label">Days to Critical</div>
            </div>
        </div>
        
        <div class="delta-indicator delta-positive">
            +{total_days_gained} DAYS GAINED
        </div>
        
        <div class="scenario-description">
            {scenario.get('description', '')}
        </div>
    </div>
    """, unsafe_allow_html=True)
```

---

## Projection Chart Pattern

### Chart Configuration

```python
def create_projection_chart(simulation: dict, projection_days: int) -> go.Figure:
    """Create projection chart showing both scenarios."""
    import plotly.graph_objects as go
    from datetime import datetime, timedelta
    
    fig = go.Figure()
    
    # Generate date range
    today = datetime.now()
    dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') 
             for i in range(projection_days + 1)]
    
    current_spi = simulation.get('current_spi', -1.72)
    no_action_spi = simulation.get('no_action_scenario', {}).get('projected_spi', -2.12)
    with_action_spi = simulation.get('with_action_scenario', {}).get('projected_spi', -1.87)
    
    # Simple linear projection (actual would use backend model)
    no_action_values = [current_spi + (no_action_spi - current_spi) * (i / projection_days) 
                        for i in range(projection_days + 1)]
    with_action_values = [current_spi + (with_action_spi - current_spi) * (i / projection_days) 
                          for i in range(projection_days + 1)]
    
    # Critical threshold line
    fig.add_hline(y=-2.0, line_dash="dash", line_color="#DC2626", 
                  annotation_text="Critical Threshold (-2.0)")
    
    # No-action scenario
    fig.add_trace(go.Scatter(
        x=dates, y=no_action_values,
        mode='lines',
        name='No Action',
        line=dict(color='#DC2626', width=2, dash='dot')
    ))
    
    # With-action scenario
    fig.add_trace(go.Scatter(
        x=dates, y=with_action_values,
        mode='lines',
        name='With Action',
        line=dict(color='#10B981', width=3)
    ))
    
    # Styling
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='#F2EDE9',
        font=dict(family="system-ui", color="#292929"),
        xaxis=dict(title="Date"),
        yaxis=dict(title="Projected SPI", range=[-3, 0]),
        legend=dict(x=0, y=1, bgcolor='rgba(255,255,255,0.8)'),
        margin=dict(l=60, r=40, t=40, b=60),
        height=350
    )
    
    return fig
```

---

## Impact Breakdown Pattern

### Table Render

```python
def render_impact_breakdown(simulation: dict) -> None:
    """Render per-action impact breakdown."""
    actions = simulation.get('actions_applied', [])
    total = simulation.get('total_days_gained', 0)
    
    st.markdown("""
    <h3>Impact Breakdown</h3>
    <p class="text-muted">Contribution of each action to total days gained</p>
    """, unsafe_allow_html=True)
    
    for action in actions:
        code = action.get('code', '')
        title = action.get('title', '')
        days = action.get('days_gained', 0)
        percentage = (days / total * 100) if total > 0 else 0
        
        st.markdown(f"""
        <div class="impact-row">
            <div class="impact-action">
                <strong>{title}</strong>
                <span class="text-muted">{code}</span>
            </div>
            <div class="impact-bar-container">
                <div class="impact-bar" style="width: {percentage}%"></div>
            </div>
            <div class="impact-value">+{days} days</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Total row
    st.markdown(f"""
    <div class="impact-total">
        <strong>Total Impact:</strong>
        <span class="delta-positive">+{total} days</span>
    </div>
    """, unsafe_allow_html=True)
```

---

## Decision Summary Pattern

### CTA Section

```python
def render_decision_summary(simulation: dict, zone_id: str, profile: str) -> None:
    """Render decision summary and confirmation CTA."""
    total_gained = simulation.get('total_days_gained', 0)
    no_action_days = simulation.get('no_action_scenario', {}).get('days_to_critical', 0)
    with_action_days = simulation.get('with_action_scenario', {}).get('days_to_critical', 0)
    
    st.markdown(f"""
    <div class="decision-summary">
        <h2>Decision Summary</h2>
        
        <div class="summary-grid">
            <div class="summary-item">
                <div class="summary-label">Zone</div>
                <div class="summary-value">{zone_id.upper()}</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Profile</div>
                <div class="summary-value">{profile.title()}</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Actions Selected</div>
                <div class="summary-value">{len(simulation.get('actions_applied', []))}</div>
            </div>
            <div class="summary-item highlight">
                <div class="summary-label">Days Gained</div>
                <div class="summary-value delta-positive">+{total_gained}</div>
            </div>
        </div>
        
        <div class="summary-comparison">
            <p>
                <strong>Without action:</strong> Critical in {no_action_days} days<br/>
                <strong>With action:</strong> Critical in {with_action_days} days
            </p>
        </div>
        
        <p class="summary-disclaimer">
            <em>Note: Projections are estimates based on historical patterns and heuristic formulas. 
            Actual results may vary based on implementation effectiveness and external factors.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
```

---

## Decision Confirmation Pattern

### Current (Basic)

```python
if st.button("✅ Confirm Decision", type="primary"):
    st.success("Decision confirmed! Actions have been logged.")
    st.balloons()
```

### Improved (Proposed)

```python
def render_decision_confirmation(simulation: dict) -> bool:
    """Render decision confirmation with proper weight."""
    
    st.markdown("""
    <div class="confirmation-section">
        <h3>Confirm Your Decision</h3>
        <p>By confirming, you acknowledge:</p>
        <ul>
            <li>You have reviewed the recommended actions</li>
            <li>You understand the projected impact</li>
            <li>You are ready to proceed with implementation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Require acknowledgment
    acknowledged = st.checkbox(
        "I have reviewed the simulation and understand the projected outcomes",
        key="confirm_acknowledgment"
    )
    
    if acknowledged:
        if st.button("Confirm and Log Decision", type="primary"):
            # Log decision
            decision_record = {
                "timestamp": datetime.now().isoformat(),
                "zone_id": simulation.get("zone_id"),
                "profile": simulation.get("profile"),
                "actions": [a["code"] for a in simulation.get("actions_applied", [])],
                "projected_impact": simulation.get("total_days_gained")
            }
            
            # Store decision (future: persist to backend)
            if "decision_history" not in st.session_state:
                st.session_state.decision_history = []
            st.session_state.decision_history.append(decision_record)
            
            st.success("Decision confirmed and logged.")
            return True
    
    return False
```

---

## Demo Data Pattern

```python
DEMO_SIMULATION = {
    "zone_id": "cdmx",
    "profile": "government",
    "current_spi": -1.72,
    "no_action_scenario": {
        "projected_spi": -2.12,
        "projected_risk_level": "CRITICAL",
        "days_to_critical": 24,
        "description": "Without intervention, conditions deteriorate to critical levels."
    },
    "with_action_scenario": {
        "projected_spi": -1.87,
        "projected_risk_level": "HIGH",
        "days_to_critical": 52,
        "description": "With selected actions, critical threshold is extended significantly."
    },
    "actions_applied": [
        {"code": "H4_LAWN_BAN", "title": "Lawn/Garden Restriction", "days_gained": 19},
        {"code": "H2_PRESSURE_REDUCTION", "title": "Pressure Management", "days_gained": 6},
        {"code": "H3_AWARENESS_CAMPAIGN", "title": "Public Awareness", "days_gained": 3}
    ],
    "total_days_gained": 28,
    "projection_days": 90
}
```

---

*Patterns ensure consistency. Propose changes through sessions.*
