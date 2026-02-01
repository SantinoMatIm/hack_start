"""
Simulation Page
Compare act vs. not-act scenarios with quantified outcomes.
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from components.header import render_header, render_zone_selector, render_back_button
from components.simulation_chart import (
    render_simulation_comparison,
    render_projection_chart,
    render_impact_breakdown,
    render_decision_summary
)
from components.risk_display import render_risk_metrics
from utils.api_client import get_api_client
from utils.icons import icon, icon_span

# Page config
st.set_page_config(
    page_title="Simulation | Water Risk Platform",
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
if "selected_actions" not in st.session_state:
    st.session_state.selected_actions = []
if "simulation_result" not in st.session_state:
    st.session_state.simulation_result = None


def main():
    # Sidebar with navigation
    zone_id, profile = render_zone_selector(current_page="simulation")

    # Additional simulation settings in sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size: 10px; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; font-weight: 600; padding-left: 4px;">Settings</div>
        """, unsafe_allow_html=True)
        projection_days = st.slider(
            "Projection (days)",
            min_value=30,
            max_value=180,
            value=90,
            step=15
        )

    # Header
    render_header(
        "Scenario Simulation",
        "Compare outcomes: Act vs. Not Act"
    )

    # Get API client
    api = get_api_client()

    # Show current context
    col1, col2 = st.columns(2)

    zone_icons = {"cdmx": "building-2", "monterrey": "factory", "baidoa": "sun"}
    zone_names = {"cdmx": "Mexico City", "monterrey": "Monterrey", "baidoa": "Baidoa (Somalia)"}
    zone_icon = zone_icons.get(zone_id, "map-pin")
    profile_icon = "landmark" if profile == "government" else "briefcase"
    zone_display = zone_names.get(zone_id, zone_id.title())

    with col1:
        st.markdown(f"""
        <div class="stat-card fade-in">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; background: var(--bg-muted); border-radius: 8px;">
                    {icon(zone_icon, 20, "#475569")}
                </div>
                <div>
                    <div class="stat-label">Zone</div>
                    <div style="font-size: 20px; font-weight: 600; color: var(--text-primary);">{zone_display}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card fade-in" style="animation-delay: 50ms;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; background: var(--bg-muted); border-radius: 8px;">
                    {icon(profile_icon, 20, "#475569")}
                </div>
                <div>
                    <div class="stat-label">Profile</div>
                    <div style="font-size: 20px; font-weight: 600; color: var(--text-primary);">{profile.title()}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Current risk context
    if st.session_state.current_risk:
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
            {icon_span("activity", 18, "#2563EB")}
            <h3 style="margin: 0;">Current Risk Status</h3>
        </div>
        """, unsafe_allow_html=True)
        render_risk_metrics(st.session_state.current_risk)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Selected actions summary
    selected_actions = st.session_state.selected_actions or []

    if selected_actions:
        st.markdown(f"""
        <div class="card fade-in" style="margin-bottom: 24px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; background: var(--accent-primary-light); border-radius: 8px;">
                    {icon("zap", 20, "#2563EB")}
                </div>
                <div>
                    <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted);">
                        Selected Actions for Simulation
                    </div>
                    <div style="font-size: 16px; font-weight: 600; color: var(--text-primary); margin-top: 2px;">
                        {len(selected_actions)} action{'s' if len(selected_actions) != 1 else ''}: {', '.join(selected_actions[:3])}{'...' if len(selected_actions) > 3 else ''}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="alert info" style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
            {icon_span("info", 18, "#2563EB")}
            <span>No specific actions selected. Simulation will use all recommended actions.</span>
        </div>
        """, unsafe_allow_html=True)

    # Run simulation button
    run_simulation = st.button(
        "Run Simulation",
        type="primary",
        use_container_width=True
    )

    if run_simulation:
        with st.spinner("Running simulation..."):
            result = api.run_simulation(
                zone_id=zone_id,
                profile=profile,
                action_codes=selected_actions if selected_actions else None,
                projection_days=projection_days
            )

            if result and "error" not in result:
                st.session_state.simulation_result = result
            else:
                # Demo fallback
                st.markdown(f"""
                <div class="alert warning" style="display: flex; align-items: center; gap: 12px; margin-top: 16px;">
                    {icon_span("alert-circle", 18, "#D97706")}
                    <span>Could not connect to API. Showing demo simulation.</span>
                </div>
                """, unsafe_allow_html=True)
                current_spi = st.session_state.current_risk.get("spi_6m", -1.72) if st.session_state.current_risk else -1.72

                st.session_state.simulation_result = {
                    "zone_id": zone_id,
                    "profile": profile,
                    "current_spi": current_spi,
                    "no_action_scenario": {
                        "projected_spi": current_spi - 0.4,
                        "projected_risk_level": "CRITICAL",
                        "days_to_critical": 24,
                        "description": "Without intervention, conditions will deteriorate to critical levels."
                    },
                    "with_action_scenario": {
                        "projected_spi": current_spi - 0.15,
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
                    "projection_days": projection_days
                }

    # Display simulation results
    simulation = st.session_state.simulation_result

    if simulation:
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
            {icon_span("git-compare", 20, "#2563EB")}
            <h2 style="margin: 0;">Simulation Results</h2>
        </div>
        """, unsafe_allow_html=True)

        # Comparison cards
        render_simulation_comparison(simulation)

        # Projection chart
        st.markdown('<div style="margin-top: 48px;">', unsafe_allow_html=True)
        render_projection_chart(simulation, projection_days)
        st.markdown('</div>', unsafe_allow_html=True)

        # Impact breakdown
        if simulation.get("actions_applied"):
            st.markdown('<div style="margin-top: 48px;">', unsafe_allow_html=True)
            render_impact_breakdown(simulation)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Decision summary
        render_decision_summary(simulation, zone_id, profile)

        # Detailed results expander
        with st.expander("Detailed Simulation Data"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    {icon_span("x-circle", 16, "#DC2626")}
                    <strong>No-Action Scenario</strong>
                </div>
                """, unsafe_allow_html=True)
                no_action = simulation.get("no_action_scenario", {})
                st.json(no_action)

            with col2:
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    {icon_span("check-circle", 16, "#059669")}
                    <strong>With-Action Scenario</strong>
                </div>
                """, unsafe_allow_html=True)
                with_action = simulation.get("with_action_scenario", {})
                st.json(with_action)

            if simulation.get("actions_applied"):
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 8px; margin: 24px 0 12px;">
                    {icon_span("zap", 16, "#2563EB")}
                    <strong>Actions Applied</strong>
                </div>
                """, unsafe_allow_html=True)
                st.json(simulation["actions_applied"])

        # Decision prompt
        st.markdown(f"""
        <div class="section fade-in" style="text-align: center; padding: 48px 0;">
            <div style="display: flex; justify-content: center; margin-bottom: 16px;">
                {icon_span("check-circle", 32, "#2563EB")}
            </div>
            <h2>Make Your Decision</h2>
            <p style="color: var(--text-muted); max-width: 600px; margin: 16px auto 32px;">
                Based on the simulation results, you can proceed with implementing the recommended actions
                or adjust the selection and re-run the simulation.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button("Modify Actions", use_container_width=True, type="secondary"):
                st.switch_page("pages/2_actions.py")

        with col2:
            if st.button("Re-run Simulation", use_container_width=True, type="secondary"):
                st.session_state.simulation_result = None
                st.rerun()

        with col3:
            if st.button("Confirm Decision", use_container_width=True, type="primary"):
                st.success("Decision confirmed! Actions have been logged for implementation tracking.")
                st.balloons()

    else:
        # No simulation yet
        st.markdown(f"""
        <div style="text-align: center; padding: 64px 0; color: var(--text-muted);">
            <div style="display: flex; justify-content: center; margin-bottom: 16px;">
                {icon_span("play-circle", 48, "#94A3B8")}
            </div>
            <p style="font-size: 17px;">Click "Run Simulation" to compare scenarios</p>
        </div>
        """, unsafe_allow_html=True)

    # Methodology reference
    with st.expander("Simulation Methodology"):
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
            {icon_span("info", 18, "#2563EB")}
            <strong>How Simulations Work</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **No-Action Scenario:**
        - Projects SPI based on current trend
        - Uses historical decline rates
        - Estimates days to critical threshold (-2.0)

        **With-Action Scenario:**
        - Applies impact formulas from each action
        - Calculates combined effect on water availability
        - Estimates extended days to critical
        """)
        
        st.markdown(f"""
        <div style="margin-top: 24px; display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
            {icon_span("bar-chart-3", 18, "#2563EB")}
            <strong>Impact Calculation</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        Each action has a defined impact formula:

        | Action Type | Impact Formula |
        |-------------|----------------|
        | Industrial reduction | 5% reduction → +3 days |
        | Pressure management | 10% reduction → +4 days |
        | Public communication | 3% reduction → +2 days |
        | Non-essential restriction | 1% removed → +1.3 days |
        | Source reallocation | 5% increase → +5 days |

        **Escalation Rule (H6):**
        When multiple actions are combined under severity escalation,
        effects are summed with a 20% efficiency penalty:
        `(Effect A + Effect B) × 0.8`
        """)
        
        st.markdown(f"""
        <div style="margin-top: 24px; display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
            {icon_span("alert-circle", 18, "#D97706")}
            <strong>Important Notes</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        - Simulations are projections based on historical patterns
        - Actual results may vary based on implementation effectiveness
        - Regular re-assessment is recommended as conditions change
        """)

    # Footer navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("View Actions", type="secondary"):
            st.switch_page("pages/2_actions.py")
    with col2:
        if st.button("Back to Home", type="secondary"):
            st.switch_page("app.py")
    with col3:
        if st.button("Risk Overview", type="secondary"):
            st.switch_page("pages/1_risk_overview.py")


if __name__ == "__main__":
    main()
