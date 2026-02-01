"""
Risk display components
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.icons import icon, icon_span


def get_risk_color_class(risk_level: str) -> str:
    """Get CSS class for risk level"""
    return risk_level.lower() if risk_level else "low"


def get_risk_color(risk_level: str) -> str:
    """Get color for risk level"""
    colors = {
        "CRITICAL": "#DC2626",
        "HIGH": "#EA580C",
        "MEDIUM": "#D97706",
        "LOW": "#059669"
    }
    return colors.get(risk_level.upper() if risk_level else "LOW", "#059669")


def get_trend_icon(trend: str) -> str:
    """Get icon name for trend direction"""
    icons = {
        "IMPROVING": "trending-up",
        "STABLE": "minus",
        "WORSENING": "trending-down"
    }
    return icons.get(trend, "minus")


def get_trend_color(trend: str) -> str:
    """Get color for trend"""
    colors = {
        "IMPROVING": "#059669",
        "STABLE": "#94A3B8",
        "WORSENING": "#DC2626"
    }
    return colors.get(trend, "#94A3B8")


def render_risk_card(risk_data: dict):
    """Render a comprehensive risk card"""
    if not risk_data:
        st.warning("No risk data available")
        return

    risk_level = risk_data.get("risk_level", "UNKNOWN")
    spi = risk_data.get("spi_6m", 0)
    trend = risk_data.get("trend", "STABLE")
    days_to_critical = risk_data.get("days_to_critical", "N/A")
    zone_id = risk_data.get("zone_id", "unknown")

    risk_class = get_risk_color_class(risk_level)
    risk_color = get_risk_color(risk_level)
    trend_icon_name = get_trend_icon(trend)
    trend_color = get_trend_color(trend)

    st.markdown(f"""
    <div class="risk-card {risk_class} fade-in">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;">
            <div>
                <span class="label">Current Risk Level</span>
                <div style="font-size: 42px; font-weight: 700; color: {risk_color}; margin-top: 4px;">{risk_level}</div>
            </div>
            <div style="text-align: right;">
                <span class="label">Zone</span>
                <div style="display: flex; align-items: center; gap: 8px; margin-top: 4px;">
                    {icon_span("map-pin", 18, "#475569")}
                    <span style="font-size: 20px; font-weight: 600; color: var(--text-primary);">{zone_id.upper()}</span>
                </div>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; padding-top: 24px; border-top: 1px solid var(--border-default);">
            <div>
                <span class="label">SPI-6 Month</span>
                <div style="font-size: 32px; font-weight: 700; color: {risk_color}; margin-top: 4px;">{spi:.2f}</div>
            </div>
            <div style="text-align: center;">
                <span class="label">Trend</span>
                <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 8px;">
                    {icon_span(trend_icon_name, 24, trend_color)}
                    <span style="font-size: 18px; font-weight: 600; color: {trend_color};">{trend}</span>
                </div>
            </div>
            <div style="text-align: right;">
                <span class="label">Days to Critical</span>
                <div style="font-size: 32px; font-weight: 700; color: {risk_color}; margin-top: 4px;">{days_to_critical}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_risk_gauge(spi_value: float):
    """Render an SPI gauge visualization"""
    # SPI typically ranges from -3 to +3
    # Map to percentage (0-100) for positioning
    # -3 = 0%, 0 = 50%, +3 = 100%
    position = ((spi_value + 3) / 6) * 100
    position = max(0, min(100, position))  # Clamp to 0-100

    st.markdown(f"""
    <div class="spi-gauge-container fade-in">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="font-size: 12px; color: var(--text-muted);">Extreme Drought</span>
            <span style="font-size: 12px; color: var(--text-muted);">Normal</span>
        </div>
        <div class="spi-gauge">
            <div class="spi-marker" style="left: {position}%;"></div>
        </div>
        <div class="spi-labels">
            <span>-3.0</span>
            <span>-2.0</span>
            <span>-1.5</span>
            <span>-1.0</span>
            <span>0</span>
        </div>
        <div style="text-align: center; margin-top: 16px;">
            <span style="font-size: 13px; color: var(--text-muted);">Current SPI: </span>
            <span style="font-size: 17px; font-weight: 600; color: var(--text-primary);">{spi_value:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_risk_metrics(risk_data: dict):
    """Render individual risk metrics as Streamlit columns"""
    if not risk_data:
        return

    col1, col2, col3, col4 = st.columns(4)

    risk_level = risk_data.get("risk_level", "UNKNOWN")
    risk_color = get_risk_color(risk_level)
    trend = risk_data.get("trend", "STABLE")
    trend_icon_name = get_trend_icon(trend)
    trend_color = get_trend_color(trend)

    with col1:
        st.markdown(f"""
        <div class="stat-card fade-in">
            <div class="stat-label">SPI-6 Month</div>
            <div class="stat-value" style="color: {risk_color};">{risk_data.get('spi_6m', 0):.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card fade-in" style="animation-delay: 50ms;">
            <div class="stat-label">Risk Level</div>
            <div class="stat-value" style="color: {risk_color};">{risk_level}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card fade-in" style="animation-delay: 100ms;">
            <div class="stat-label">Trend</div>
            <div style="display: flex; align-items: center; gap: 8px; margin-top: 4px;">
                {icon_span(trend_icon_name, 20, trend_color)}
                <span style="font-size: 18px; font-weight: 600; color: {trend_color};">{trend}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        days = risk_data.get("days_to_critical", "N/A")
        st.markdown(f"""
        <div class="stat-card fade-in" style="animation-delay: 150ms;">
            <div class="stat-label">Days to Critical</div>
            <div class="stat-value" style="color: {risk_color};">{days}</div>
        </div>
        """, unsafe_allow_html=True)


def render_risk_explanation(risk_data: dict):
    """Render an explanation of the current risk status"""
    if not risk_data:
        return

    risk_level = risk_data.get("risk_level", "UNKNOWN")
    spi = risk_data.get("spi_6m", 0)
    trend = risk_data.get("trend", "STABLE")
    days = risk_data.get("days_to_critical", "N/A")

    explanations = {
        "CRITICAL": f"The zone is experiencing severe drought conditions (SPI: {spi:.2f}). Immediate action is required. Critical threshold may be reached in {days} days.",
        "HIGH": f"Drought conditions are significant (SPI: {spi:.2f}). Proactive measures are strongly recommended. Estimated {days} days to critical threshold.",
        "MEDIUM": f"Moderate drought stress detected (SPI: {spi:.2f}). Monitoring and preparatory actions advised. Approximately {days} days to critical if conditions worsen.",
        "LOW": f"Water conditions are within normal parameters (SPI: {spi:.2f}). Continue standard monitoring. No immediate action required."
    }

    trend_explanations = {
        "WORSENING": "Conditions are deteriorating. The trend indicates increasing drought severity.",
        "STABLE": "Conditions are stable. No significant change in drought severity detected.",
        "IMPROVING": "Conditions are improving. Drought severity is decreasing."
    }

    risk_color = get_risk_color(risk_level)
    trend_icon_name = get_trend_icon(trend)
    trend_color = get_trend_color(trend)

    st.markdown(f"""
    <div class="card fade-in" style="margin-top: 24px;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
            {icon_span("info", 18, "#2563EB")}
            <h3 style="margin: 0; font-size: 16px;">Assessment Summary</h3>
        </div>
        <p style="color: var(--text-secondary); margin-bottom: 12px;">{explanations.get(risk_level, "Risk level unknown.")}</p>
        <div style="display: flex; align-items: center; gap: 8px; padding-top: 12px; border-top: 1px solid var(--border-default);">
            {icon_span(trend_icon_name, 16, trend_color)}
            <span style="font-size: 14px; color: {trend_color};">{trend_explanations.get(trend, "")}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
