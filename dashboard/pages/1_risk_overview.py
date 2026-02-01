"""
Risk Overview Page
View current SPI, risk level, trend, and days to critical threshold.
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from components.header import render_header, render_zone_selector, render_back_button
from components.risk_display import (
    render_risk_card,
    render_risk_gauge,
    render_risk_metrics,
    render_risk_explanation,
    get_risk_color
)
from utils.api_client import get_api_client
from utils.icons import icon, icon_span

# Page config
st.set_page_config(
    page_title="Risk Overview | Water Risk Platform",
    page_icon="💧",
    layout="wide",
)

# Load CSS
css_file = Path(__file__).parent.parent / "assets" / "styles.css"
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if "selected_zone" not in st.session_state:
    st.session_state.selected_zone = "cdmx"
if "selected_profile" not in st.session_state:
    st.session_state.selected_profile = "government"
if "current_risk" not in st.session_state:
    st.session_state.current_risk = None


def main():
    # Sidebar with navigation
    zone_id, profile = render_zone_selector(current_page="risk")

    # Header
    render_header(
        "Risk Overview",
        "Current drought risk assessment and trend analysis"
    )

    # Get API client
    api = get_api_client()

    # Fetch current risk data
    with st.spinner("Loading risk data..."):
        risk_data = api.get_current_risk(zone_id)

    if not risk_data or "error" in risk_data:
        st.markdown(f"""
        <div class="alert warning" style="display: flex; align-items: center; gap: 12px;">
            {icon_span("alert-circle", 20, "#D97706")}
            <span>Unable to fetch risk data. Please ensure the API server is running.</span>
        </div>
        """, unsafe_allow_html=True)

        # Show demo data option
        if st.button("Show Demo Data", type="primary"):
            risk_data = {
                "zone_id": zone_id,
                "spi_6m": -1.72,
                "risk_level": "HIGH",
                "trend": "WORSENING",
                "days_to_critical": 24,
                "calculated_at": "2024-01-15T10:30:00Z"
            }
        else:
            return

    # Store in session state
    st.session_state.current_risk = risk_data

    # Main risk card
    st.markdown('<div class="section">', unsafe_allow_html=True)
    render_risk_card(risk_data)
    st.markdown('</div>', unsafe_allow_html=True)

    # SPI Gauge visualization
    st.markdown('<div class="section fade-in">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
        {icon_span("gauge", 20, "#2563EB")}
        <h2 style="margin: 0;">SPI Index</h2>
    </div>
    """, unsafe_allow_html=True)
    render_risk_gauge(risk_data.get("spi_6m", 0))
    st.markdown('</div>', unsafe_allow_html=True)

    # Risk explanation
    render_risk_explanation(risk_data)

    # Risk thresholds reference
    with st.expander("Understanding Risk Levels"):
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
            {icon_span("info", 18, "#2563EB")}
            <strong>SPI-6 Month Risk Classification</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        | Risk Level | SPI Range | Description |
        |------------|-----------|-------------|
        | **LOW** | > -0.5 | Normal to near-normal conditions |
        | **MEDIUM** | -1.0 to -0.5 | Moderate drought, monitoring advised |
        | **HIGH** | -1.5 to -1.0 | Severe drought, action recommended |
        | **CRITICAL** | ≤ -1.5 | Extreme drought, immediate action required |
        """)
        
        st.markdown(f"""
        <div style="margin-top: 24px; display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
            {icon_span("activity", 18, "#2563EB")}
            <strong>Trend Indicators</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="display: flex; flex-direction: column; gap: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                {icon_span("trending-up", 16, "#059669")}
                <span><strong>IMPROVING</strong>: SPI increasing by more than 0.1 over recent period</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                {icon_span("minus", 16, "#94A3B8")}
                <span><strong>STABLE</strong>: SPI change within ±0.1</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                {icon_span("trending-down", 16, "#DC2626")}
                <span><strong>WORSENING</strong>: SPI decreasing by more than 0.1 over recent period</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="margin-top: 24px; display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
            {icon_span("clock", 18, "#2563EB")}
            <strong>Days to Critical</strong>
        </div>
        <p style="color: var(--text-secondary);">
            Estimated number of days until SPI reaches the critical threshold (-2.0),
            based on current trend and historical decline rates.
        </p>
        """, unsafe_allow_html=True)

    # Action prompt
    risk_level = risk_data.get("risk_level", "LOW")
    if risk_level in ["HIGH", "CRITICAL"]:
        risk_color = get_risk_color(risk_level)
        st.markdown(f"""
        <div class="dark-section fade-in">
            <div style="text-align: center; max-width: 600px; margin: 0 auto;">
                <div style="display: flex; justify-content: center; margin-bottom: 16px;">
                    {icon_span("alert-triangle", 32, risk_color)}
                </div>
                <h2 style="margin-bottom: 12px;">Action Required</h2>
                <p style="color: var(--text-muted); margin-bottom: 24px;">
                    Current conditions require intervention. Review recommended actions to extend the time to critical threshold.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("View Recommended Actions", use_container_width=True, type="primary"):
                st.switch_page("pages/2_actions.py")

    # History section (if available)
    st.markdown('<div class="section fade-in">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
        {icon_span("line-chart", 20, "#2563EB")}
        <h2 style="margin: 0;">Recent History</h2>
    </div>
    """, unsafe_allow_html=True)

    history_data = api.get_risk_history(zone_id, days=30)
    if history_data and "history" in history_data:
        history = history_data["history"]
        if history:
            import plotly.graph_objects as go

            dates = [h.get("date", h.get("calculated_at", "")) for h in history]
            spi_values = [h.get("spi_6m", 0) for h in history]

            fig = go.Figure()

            # Add threshold areas
            fig.add_hrect(y0=-3, y1=-1.5, fillcolor="rgba(220, 38, 38, 0.08)",
                          line_width=0)
            fig.add_hrect(y0=-1.5, y1=-1.0, fillcolor="rgba(234, 88, 12, 0.08)",
                          line_width=0)
            fig.add_hrect(y0=-1.0, y1=-0.5, fillcolor="rgba(217, 119, 6, 0.08)",
                          line_width=0)

            # Add SPI line
            fig.add_trace(go.Scatter(
                x=dates,
                y=spi_values,
                mode='lines+markers',
                name='SPI-6m',
                line=dict(color='#2563EB', width=2),
                marker=dict(size=6, color='#2563EB')
            ))

            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='#FFFFFF',
                font=dict(family="Inter, system-ui, sans-serif", color="#0F172A", size=13),
                xaxis=dict(
                    title="Date",
                    showgrid=True,
                    gridcolor='rgba(0,0,0,0.05)',
                    linecolor='#E2E8F0'
                ),
                yaxis=dict(
                    title="SPI-6 Month",
                    showgrid=True,
                    gridcolor='rgba(0,0,0,0.05)',
                    range=[-3, 0.5],
                    linecolor='#E2E8F0'
                ),
                margin=dict(l=60, r=40, t=40, b=60),
                showlegend=False,
                height=300
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown(f"""
            <div class="alert info" style="display: flex; align-items: center; gap: 12px;">
                {icon_span("info", 18, "#2563EB")}
                <span>No historical data available for the selected period.</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="alert info" style="display: flex; align-items: center; gap: 12px;">
            {icon_span("info", 18, "#2563EB")}
            <span>Historical data not available. Connect to the API to view trends.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Back to Home", type="secondary"):
            st.switch_page("app.py")
    with col3:
        if st.button("View Actions", type="primary"):
            st.switch_page("pages/2_actions.py")


if __name__ == "__main__":
    main()
