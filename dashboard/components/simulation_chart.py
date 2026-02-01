"""
Simulation and comparison visualization components
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Optional
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.icons import icon, icon_span


def render_simulation_comparison(simulation_data: dict):
    """Render the act vs. not-act comparison cards"""
    if not simulation_data:
        st.warning("No simulation data available")
        return

    no_action = simulation_data.get("no_action_scenario", {})
    with_action = simulation_data.get("with_action_scenario", {})

    # Calculate deltas
    days_delta = 0
    no_action_days = no_action.get("days_to_critical", 0)
    with_action_days = with_action.get("days_to_critical", 0)

    if isinstance(no_action_days, (int, float)) and isinstance(with_action_days, (int, float)):
        days_delta = with_action_days - no_action_days

    no_action_risk = no_action.get("projected_risk_level", "")
    with_action_risk = with_action.get("projected_risk_level", "")

    # Get risk colors
    risk_colors = {
        "CRITICAL": "#DC2626",
        "HIGH": "#EA580C",
        "MEDIUM": "#D97706",
        "LOW": "#059669"
    }
    
    no_action_color = risk_colors.get(no_action_risk.upper(), "#475569")
    with_action_color = risk_colors.get(with_action_risk.upper(), "#059669")

    st.markdown(f"""
    <div class="comparison-container fade-in">
        <div class="comparison-card no-action">
            <div class="comparison-label">
                {icon_span("x-circle", 14, "#DC2626")}
                <span style="margin-left: 6px;">Without Action</span>
            </div>
            <div style="margin-bottom: 24px;">
                <span style="font-size: 12px; color: var(--text-muted);">Projected Risk</span>
                <div style="font-size: 32px; font-weight: 700; color: {no_action_color};">{no_action_risk}</div>
            </div>
            <div style="margin-bottom: 24px;">
                <span style="font-size: 12px; color: var(--text-muted);">Days to Critical</span>
                <div style="font-size: 48px; font-weight: 700; color: var(--text-primary);">{no_action_days}</div>
            </div>
            <div>
                <span style="font-size: 12px; color: var(--text-muted);">Projected SPI</span>
                <div style="font-size: 20px; font-weight: 600; color: var(--text-primary);">{no_action.get('projected_spi', 'N/A')}</div>
            </div>
        </div>

        <div class="comparison-card with-action">
            <div class="comparison-label" style="color: #059669;">
                {icon_span("check-circle", 14, "#059669")}
                <span style="margin-left: 6px;">With Action</span>
            </div>
            <div style="margin-bottom: 24px;">
                <span style="font-size: 12px; color: var(--text-muted);">Projected Risk</span>
                <div style="font-size: 32px; font-weight: 700; color: {with_action_color};">{with_action_risk}</div>
            </div>
            <div style="margin-bottom: 24px;">
                <span style="font-size: 12px; color: var(--text-muted);">Days to Critical</span>
                <div style="font-size: 48px; font-weight: 700;">{with_action_days}</div>
                <div class="delta-highlight" style="margin-top: 8px;">
                    {icon_span("trending-up", 14, "#059669")}
                    <span>+{days_delta:.0f} days gained</span>
                </div>
            </div>
            <div>
                <span style="font-size: 12px; color: var(--text-muted);">Projected SPI</span>
                <div style="font-size: 20px; font-weight: 600;">{with_action.get('projected_spi', 'N/A')}</div>
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
    fig.add_hline(y=-1.5, line_dash="dash", line_color="#EA580C", line_width=1,
                  annotation_text="High Risk", annotation_position="right",
                  annotation_font_color="#EA580C", annotation_font_size=11)
    fig.add_hline(y=-2.0, line_dash="dash", line_color="#DC2626", line_width=1,
                  annotation_text="Critical", annotation_position="right",
                  annotation_font_color="#DC2626", annotation_font_size=11)

    # Add no-action projection
    fig.add_trace(go.Scatter(
        x=days,
        y=no_action_projection,
        mode='lines',
        name='Without Action',
        line=dict(color='#DC2626', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(220, 38, 38, 0.08)'
    ))

    # Add with-action projection
    fig.add_trace(go.Scatter(
        x=days,
        y=with_action_projection,
        mode='lines',
        name='With Action',
        line=dict(color='#059669', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(5, 150, 105, 0.08)'
    ))

    # Update layout
    fig.update_layout(
        title=dict(
            text="SPI Projection Over Time",
            font=dict(size=18, family="Inter, system-ui, sans-serif", color="#0F172A"),
            x=0
        ),
        xaxis=dict(
            title="Days",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            zeroline=False,
            linecolor='#E2E8F0',
            tickfont=dict(size=12, color="#475569")
        ),
        yaxis=dict(
            title="SPI-6 Month",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            zeroline=False,
            range=[-3, 0.5],
            linecolor='#E2E8F0',
            tickfont=dict(size=12, color="#475569")
        ),
        plot_bgcolor='white',
        paper_bgcolor='#FFFFFF',
        font=dict(family="Inter, system-ui, sans-serif", color="#0F172A"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12)
        ),
        margin=dict(l=60, r=40, t=80, b=60),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Inter, system-ui, sans-serif"
        )
    )

    st.plotly_chart(fig, use_container_width=True)


def render_impact_breakdown(simulation_data: dict):
    """Render a breakdown of impact by action"""
    actions = simulation_data.get("actions_applied", [])
    if not actions:
        return

    st.markdown(f"""
    <div class="section fade-in">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
            {icon_span("bar-chart-3", 20, "#2563EB")}
            <h3 style="margin: 0;">Impact Breakdown by Action</h3>
        </div>
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
            color='#2563EB',
            line=dict(color='#1D4ED8', width=1)
        ),
        text=[f"+{d:.0f} days" for d in days_gained],
        textposition='outside',
        textfont=dict(size=12, color="#0F172A", family="Inter, system-ui, sans-serif")
    ))

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='#FFFFFF',
        font=dict(family="Inter, system-ui, sans-serif", color="#0F172A"),
        xaxis=dict(
            title="Days Gained",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)',
            linecolor='#E2E8F0',
            tickfont=dict(size=12, color="#475569")
        ),
        yaxis=dict(
            showgrid=False,
            automargin=True,
            tickfont=dict(size=12, color="#475569")
        ),
        margin=dict(l=20, r=100, t=20, b=60),
        height=max(200, len(actions) * 60)
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

    # Get risk colors
    risk_colors = {
        "CRITICAL": "#DC2626",
        "HIGH": "#EA580C",
        "MEDIUM": "#D97706",
        "LOW": "#059669"
    }
    
    no_action_risk = no_action.get('projected_risk_level', 'N/A')
    with_action_risk = with_action.get('projected_risk_level', 'N/A')
    no_action_color = risk_colors.get(no_action_risk.upper() if no_action_risk else "", "#475569")
    with_action_color = risk_colors.get(with_action_risk.upper() if with_action_risk else "", "#059669")

    st.markdown(f"""
    <div class="dark-section fade-in">
        <div style="max-width: 900px; margin: 0 auto; text-align: center;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 8px;">
                {icon_span("clipboard", 20, "#94A3B8")}
                <span style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted);">Decision Summary</span>
            </div>
            <h2 style="margin-bottom: 8px;">{zone_id.upper()}</h2>
            <p style="font-size: 14px; color: var(--text-muted); margin-bottom: 32px;">
                {profile.title()} Profile
            </p>

            <div style="background: rgba(255,255,255,0.08); padding: 40px; border-radius: 12px; margin-bottom: 32px;">
                <div style="display: flex; justify-content: center; margin-bottom: 12px;">
                    {icon_span("trending-up", 32, "#059669")}
                </div>
                <div style="font-size: 64px; font-weight: 700; color: #059669; margin-bottom: 8px;">
                    +{days_gained:.0f}
                </div>
                <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted);">
                    Days Gained to Critical Threshold
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; text-align: left;">
                <div style="padding: 20px; background: rgba(220, 38, 38, 0.1); border-radius: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                        {icon_span("x-circle", 16, "#DC2626")}
                        <span style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #DC2626;">Without Action</span>
                    </div>
                    <div style="font-size: 20px; margin-bottom: 4px;">Risk: <span style="color: {no_action_color}; font-weight: 600;">{no_action_risk}</span></div>
                    <div style="font-size: 14px; color: var(--text-muted);">Critical in {no_days} days</div>
                </div>
                <div style="padding: 20px; background: rgba(5, 150, 105, 0.1); border-radius: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                        {icon_span("check-circle", 16, "#059669")}
                        <span style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #059669;">With Action</span>
                    </div>
                    <div style="font-size: 20px; margin-bottom: 4px;">Risk: <span style="color: {with_action_color}; font-weight: 600;">{with_action_risk}</span></div>
                    <div style="font-size: 14px; color: var(--text-muted);">Critical in {with_days} days</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
