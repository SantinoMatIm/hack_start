"""
Risk display components
"""

import streamlit as st


def get_risk_color_class(risk_level: str) -> str:
    """Get CSS class for risk level"""
    return risk_level.lower() if risk_level else "low"


def get_trend_icon(trend: str) -> str:
    """Get icon for trend direction"""
    icons = {
        "IMPROVING": "📈",
        "STABLE": "➡️",
        "WORSENING": "📉"
    }
    return icons.get(trend, "➡️")


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
    trend_icon = get_trend_icon(trend)

    st.markdown(f"""
    <div class="risk-card {risk_class} reveal fade-up">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;">
            <div>
                <span class="metric-label">Current Risk Level</span>
                <div class="metric-value {risk_class}" style="font-size: 48px;">{risk_level}</div>
            </div>
            <div style="text-align: right;">
                <span class="metric-label">Zone</span>
                <div style="font-size: 24px; font-weight: 700;">{zone_id.upper()}</div>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; margin-top: 32px;">
            <div class="metric-container" style="text-align: left; padding: 0;">
                <span class="metric-label">SPI-6 Month</span>
                <div class="metric-value {risk_class}">{spi:.2f}</div>
            </div>
            <div class="metric-container" style="text-align: center; padding: 0;">
                <span class="metric-label">Trend</span>
                <div style="font-size: 32px; font-weight: 700;">{trend_icon} {trend}</div>
            </div>
            <div class="metric-container" style="text-align: right; padding: 0;">
                <span class="metric-label">Days to Critical</span>
                <div class="metric-value {risk_class}">{days_to_critical}</div>
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
    <div class="reveal fade-up">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="font-size: 12px; color: var(--text-muted);">Exceptionally Dry</span>
            <span style="font-size: 12px; color: var(--text-muted);">Normal</span>
        </div>
        <div class="spi-gauge">
            <div class="spi-marker" style="left: {position}%;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 8px;">
            <span style="font-size: 12px; font-weight: 600;">-3.0</span>
            <span style="font-size: 12px; font-weight: 600;">-2.0</span>
            <span style="font-size: 12px; font-weight: 600;">-1.5</span>
            <span style="font-size: 12px; font-weight: 600;">-1.0</span>
            <span style="font-size: 12px; font-weight: 600;">0</span>
        </div>
        <div style="text-align: center; margin-top: 16px;">
            <span style="font-size: 14px; color: var(--text-muted);">Current SPI: </span>
            <span style="font-size: 18px; font-weight: 700;">{spi_value:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_risk_metrics(risk_data: dict):
    """Render individual risk metrics as Streamlit columns"""
    if not risk_data:
        return

    col1, col2, col3, col4 = st.columns(4)

    risk_level = risk_data.get("risk_level", "UNKNOWN")
    risk_class = get_risk_color_class(risk_level)

    with col1:
        st.markdown(f"""
        <div class="metric-container reveal fade-up">
            <div class="metric-value {risk_class}">{risk_data.get('spi_6m', 0):.2f}</div>
            <div class="metric-label">SPI-6 Month</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-container reveal fade-up" style="transition-delay: 100ms;">
            <div class="metric-value {risk_class}">{risk_level}</div>
            <div class="metric-label">Risk Level</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        trend = risk_data.get("trend", "STABLE")
        trend_icon = get_trend_icon(trend)
        st.markdown(f"""
        <div class="metric-container reveal fade-up" style="transition-delay: 200ms;">
            <div class="metric-value">{trend_icon}</div>
            <div class="metric-label">{trend}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        days = risk_data.get("days_to_critical", "N/A")
        st.markdown(f"""
        <div class="metric-container reveal fade-up" style="transition-delay: 300ms;">
            <div class="metric-value {risk_class}">{days}</div>
            <div class="metric-label">Days to Critical</div>
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

    st.markdown(f"""
    <div class="risk-explanation reveal fade-up" style="background: var(--bg-surface); padding: 24px; border: 1px solid var(--border-default); margin-top: 24px;">
        <h3 style="margin-bottom: 16px;">Assessment Summary</h3>
        <p>{explanations.get(risk_level, "Risk level unknown.")}</p>
        <p style="margin-top: 12px; color: var(--text-muted);">{trend_explanations.get(trend, "")}</p>
    </div>
    """, unsafe_allow_html=True)
