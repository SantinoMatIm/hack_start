"""
Simulation and comparison visualization components
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Optional


def render_simulation_comparison(simulation_data: dict):
    """Render the act vs. not-act comparison cards"""
    if not simulation_data:
        st.warning("No simulation data available")
        return

    no_action = simulation_data.get("no_action_scenario", {})
    with_action = simulation_data.get("with_action_scenario", {})

    # Calculate deltas
    days_delta = 0
    risk_delta = ""

    no_action_days = no_action.get("days_to_critical", 0)
    with_action_days = with_action.get("days_to_critical", 0)

    if isinstance(no_action_days, (int, float)) and isinstance(with_action_days, (int, float)):
        days_delta = with_action_days - no_action_days

    no_action_risk = no_action.get("projected_risk_level", "")
    with_action_risk = with_action.get("projected_risk_level", "")

    st.markdown(f"""
    <div class="comparison-container reveal fade-up">
        <div class="comparison-card no-action">
            <div class="comparison-label">Without Action</div>
            <div style="margin-bottom: 24px;">
                <span style="font-size: 14px; color: var(--text-muted);">Projected Risk</span>
                <div style="font-size: 36px; font-weight: 800; color: #DC2626;">{no_action_risk}</div>
            </div>
            <div style="margin-bottom: 24px;">
                <span style="font-size: 14px; color: var(--text-muted);">Days to Critical</span>
                <div style="font-size: 48px; font-weight: 800;">{no_action_days}</div>
            </div>
            <div>
                <span style="font-size: 14px; color: var(--text-muted);">Projected SPI</span>
                <div style="font-size: 24px; font-weight: 700;">{no_action.get('projected_spi', 'N/A')}</div>
            </div>
        </div>

        <div class="comparison-card with-action">
            <div class="comparison-label">With Action</div>
            <div style="margin-bottom: 24px;">
                <span style="font-size: 14px; color: var(--accent-dark);">Projected Risk</span>
                <div style="font-size: 36px; font-weight: 800; color: #10B981;">{with_action_risk}</div>
            </div>
            <div style="margin-bottom: 24px;">
                <span style="font-size: 14px; color: var(--accent-dark);">Days to Critical</span>
                <div style="font-size: 48px; font-weight: 800;">{with_action_days}</div>
                <span class="delta-positive" style="font-size: 18px;">+{days_delta:.0f} days gained</span>
            </div>
            <div>
                <span style="font-size: 14px; color: var(--accent-dark);">Projected SPI</span>
                <div style="font-size: 24px; font-weight: 700;">{with_action.get('projected_spi', 'N/A')}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_projection_chart(simulation_data: dict, projection_days: int = 90):
    """Render a line chart showing SPI projections"""
    if not simulation_data:
        return

    no_action = simulation_data.get("no_action_scenario", {})
    with_action = simulation_data.get("with_action_scenario", {})

    # Get projection data or create synthetic data for visualization
    no_action_projection = no_action.get("spi_projection", [])
    with_action_projection = with_action.get("spi_projection", [])

    # If no projection data, create synthetic visualization
    if not no_action_projection:
        current_spi = simulation_data.get("current_spi", -1.5)
        no_action_final = no_action.get("projected_spi", current_spi - 0.5)
        with_action_final = with_action.get("projected_spi", current_spi - 0.2)

        # Create linear projections
        days = list(range(0, projection_days + 1, 10))
        no_action_projection = [
            current_spi + (no_action_final - current_spi) * (d / projection_days)
            for d in days
        ]
        with_action_projection = [
            current_spi + (with_action_final - current_spi) * (d / projection_days)
            for d in days
        ]
    else:
        days = list(range(len(no_action_projection)))

    # Create the figure
    fig = go.Figure()

    # Add threshold lines
    fig.add_hline(y=-1.5, line_dash="dash", line_color="#F59E0B",
                  annotation_text="High Risk Threshold", annotation_position="right")
    fig.add_hline(y=-2.0, line_dash="dash", line_color="#DC2626",
                  annotation_text="Critical Threshold", annotation_position="right")

    # Add no-action projection
    fig.add_trace(go.Scatter(
        x=days,
        y=no_action_projection,
        mode='lines',
        name='Without Action',
        line=dict(color='#DC2626', width=3),
        fill='tozeroy',
        fillcolor='rgba(220, 38, 38, 0.1)'
    ))

    # Add with-action projection
    fig.add_trace(go.Scatter(
        x=days,
        y=with_action_projection,
        mode='lines',
        name='With Action',
        line=dict(color='#10B981', width=3),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.1)'
    ))

    # Update layout
    fig.update_layout(
        title=dict(
            text="SPI Projection Over Time",
            font=dict(size=24, family="system-ui", color="#292929"),
            x=0
        ),
        xaxis=dict(
            title="Days",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            zeroline=False
        ),
        yaxis=dict(
            title="SPI-6 Month",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            zeroline=False,
            range=[-3, 0.5]
        ),
        plot_bgcolor='white',
        paper_bgcolor='#F2EDE9',
        font=dict(family="system-ui", color="#292929"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=60, r=40, t=80, b=60),
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)


def render_impact_breakdown(simulation_data: dict):
    """Render a breakdown of impact by action"""
    actions = simulation_data.get("actions_applied", [])
    if not actions:
        return

    st.markdown("""
    <div class="section reveal fade-up">
        <h3>Impact Breakdown by Action</h3>
    </div>
    """, unsafe_allow_html=True)

    # Create horizontal bar chart
    action_names = []
    days_gained = []

    for action in actions:
        name = action.get("title", action.get("code", "Unknown"))
        effect = action.get("days_gained", 0)
        if isinstance(effect, str):
            import re
            match = re.search(r'(\d+(?:\.\d+)?)', effect)
            effect = float(match.group(1)) if match else 0
        action_names.append(name)
        days_gained.append(effect)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=days_gained,
        y=action_names,
        orientation='h',
        marker=dict(
            color='#E76237',
            line=dict(color='#292929', width=1)
        ),
        text=[f"+{d:.0f} days" for d in days_gained],
        textposition='outside'
    ))

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='#F2EDE9',
        font=dict(family="system-ui", color="#292929"),
        xaxis=dict(
            title="Days Gained",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)'
        ),
        yaxis=dict(
            showgrid=False,
            automargin=True
        ),
        margin=dict(l=20, r=100, t=20, b=60),
        height=max(200, len(actions) * 50)
    )

    st.plotly_chart(fig, use_container_width=True)


def render_decision_summary(simulation_data: dict, zone_id: str, profile: str):
    """Render the final decision summary section"""
    if not simulation_data:
        return

    no_action = simulation_data.get("no_action_scenario", {})
    with_action = simulation_data.get("with_action_scenario", {})

    days_gained = 0
    no_days = no_action.get("days_to_critical", 0)
    with_days = with_action.get("days_to_critical", 0)
    if isinstance(no_days, (int, float)) and isinstance(with_days, (int, float)):
        days_gained = with_days - no_days

    st.markdown(f"""
    <div class="dark-section reveal fade-up">
        <div style="max-width: 900px; margin: 0 auto; text-align: center;">
            <h2 style="margin-bottom: 16px;">Decision Summary</h2>
            <p style="font-size: 20px; color: var(--accent-dark); margin-bottom: 48px;">
                {zone_id.upper()} • {profile.title()} Profile
            </p>

            <div style="background: rgba(255,255,255,0.1); padding: 48px; margin-bottom: 32px;">
                <div style="font-size: 72px; font-weight: 800; color: #10B981; margin-bottom: 16px;">
                    +{days_gained:.0f}
                </div>
                <div style="font-size: 18px; text-transform: uppercase; letter-spacing: 0.15em;">
                    Days Gained to Critical Threshold
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 32px; text-align: left;">
                <div>
                    <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--accent-dark); margin-bottom: 8px;">Without Action</div>
                    <div style="font-size: 24px;">Risk: <span style="color: #DC2626;">{no_action.get('projected_risk_level', 'N/A')}</span></div>
                    <div style="font-size: 18px; color: var(--accent-dark);">Critical in {no_days} days</div>
                </div>
                <div>
                    <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--accent-dark); margin-bottom: 8px;">With Action</div>
                    <div style="font-size: 24px;">Risk: <span style="color: #10B981;">{with_action.get('projected_risk_level', 'N/A')}</span></div>
                    <div style="font-size: 18px; color: var(--accent-dark);">Critical in {with_days} days</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
