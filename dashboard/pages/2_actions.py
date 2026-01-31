"""
Recommended Actions Page
AI-parameterized actions based on current conditions and profile.
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from components.header import render_header, render_zone_selector, render_back_button
from components.action_card import (
    render_action_card,
    render_action_list,
    render_action_summary,
    render_heuristic_explanation
)
from components.risk_display import render_risk_metrics
from utils.api_client import get_api_client

# Page config
st.set_page_config(
    page_title="Recommended Actions | Water Risk Platform",
    page_icon="⚡",
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
if "recommended_actions" not in st.session_state:
    st.session_state.recommended_actions = None
if "selected_actions" not in st.session_state:
    st.session_state.selected_actions = []


def main():
    # Sidebar
    zone_id, profile = render_zone_selector()

    # Back button
    render_back_button()

    # Header
    render_header(
        "Recommended Actions",
        f"AI-parameterized drought response actions for {zone_id.upper()}"
    )

    # Get API client
    api = get_api_client()

    # Show current risk context
    if st.session_state.current_risk:
        st.markdown('<div class="section reveal fade-up">', unsafe_allow_html=True)
        st.markdown('<h3>Current Risk Context</h3>', unsafe_allow_html=True)
        render_risk_metrics(st.session_state.current_risk)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Fetch current risk if not in session
        with st.spinner("Loading risk context..."):
            risk_data = api.get_current_risk(zone_id)
            if risk_data and "error" not in risk_data:
                st.session_state.current_risk = risk_data
                render_risk_metrics(risk_data)

    st.markdown("---")

    # Profile explanation
    profile_info = {
        "government": {
            "icon": "🏛️",
            "priorities": "Impact + Urgency",
            "description": "Prioritizes public welfare and rapid response"
        },
        "industry": {
            "icon": "🏢",
            "priorities": "Impact + Cost",
            "description": "Prioritizes cost-effective solutions with high impact"
        }
    }

    info = profile_info.get(profile, profile_info["government"])
    st.markdown(f"""
    <div style="background: var(--bg-surface); padding: 20px; border: 1px solid var(--border-default); margin-bottom: 32px;">
        <div style="display: flex; align-items: center; gap: 16px;">
            <span style="font-size: 32px;">{info['icon']}</span>
            <div>
                <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted);">{profile.title()} Profile</div>
                <div style="font-size: 18px; font-weight: 600;">{info['description']}</div>
                <div style="font-size: 14px; color: var(--action-primary);">Prioritizes: {info['priorities']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Fetch recommended actions
    fetch_actions = st.button("🔄 Get Recommended Actions", type="primary", use_container_width=True)

    if fetch_actions or st.session_state.recommended_actions is None:
        with st.spinner("AI is analyzing conditions and parameterizing actions..."):
            result = api.get_recommended_actions(zone_id, profile)

            if result and "actions" in result:
                st.session_state.recommended_actions = result["actions"]
            elif result and "error" not in result:
                st.session_state.recommended_actions = result.get("actions", [])
            else:
                # Demo data fallback
                st.warning("Could not fetch from API. Showing demo actions.")
                st.session_state.recommended_actions = [
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
                    {
                        "base_action_id": "H2_PRESSURE_REDUCTION",
                        "code": "H2_PRESSURE_REDUCTION",
                        "title": "Network Pressure Reduction",
                        "parameters": {
                            "pressure_reduction_percent": 15.0,
                            "hours_per_day": 8,
                            "priority_level": "HIGH"
                        },
                        "justification": "SPI in range -1.2 to -1.8, worsening conditions warrant pressure management.",
                        "expected_effect": "+6 days to critical threshold"
                    },
                    {
                        "base_action_id": "H3_AWARENESS_CAMPAIGN",
                        "code": "H3_AWARENESS_CAMPAIGN",
                        "title": "Public Awareness Campaign",
                        "parameters": {
                            "target_reduction_percent": 5.0,
                            "duration_days": 45,
                            "priority_level": "MEDIUM",
                            "channels": ["social_media", "radio", "billboards"]
                        },
                        "justification": "SPI below -1.0 with worsening trend. Public communication supports other measures.",
                        "expected_effect": "+3 days to critical threshold"
                    }
                ]

    # Display actions
    actions = st.session_state.recommended_actions or []

    if actions:
        # Action summary
        render_action_summary(actions)

        # Individual action cards
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Action Details</h2>', unsafe_allow_html=True)

        # Selection for simulation
        st.markdown("""
        <p style="color: var(--text-muted); margin-bottom: 24px;">
            Select actions to include in scenario simulation. All actions are selected by default.
        </p>
        """, unsafe_allow_html=True)

        selected_codes = []

        for i, action in enumerate(actions):
            code = action.get("code", action.get("base_action_id", f"action_{i}"))

            col1, col2 = st.columns([0.05, 0.95])
            with col1:
                selected = st.checkbox("", value=True, key=f"select_{code}", label_visibility="collapsed")
                if selected:
                    selected_codes.append(code)
            with col2:
                render_action_card(action, i)

            # Show heuristic explanation
            heuristic_id = code.split("_")[0] if "_" in code else ""
            if heuristic_id in ["H1", "H2", "H3", "H4", "H5", "H6"]:
                with st.expander(f"ℹ️ About {heuristic_id} Heuristic"):
                    render_heuristic_explanation(heuristic_id)

        st.session_state.selected_actions = selected_codes
        st.markdown('</div>', unsafe_allow_html=True)

        # Simulation CTA
        st.markdown("""
        <div class="dark-section reveal fade-up">
            <div style="text-align: center; max-width: 600px; margin: 0 auto;">
                <h2 style="margin-bottom: 16px;">Ready to Simulate</h2>
                <p style="color: var(--accent-dark); margin-bottom: 32px;">
                    Compare the impact of selected actions against taking no action.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"Run Simulation with {len(selected_codes)} Actions →",
                         use_container_width=True, type="primary"):
                st.switch_page("pages/3_simulation.py")

    else:
        st.info("No actions have been recommended yet. Click the button above to get AI recommendations.")

    # Heuristics reference
    with st.expander("📖 Decision Heuristics Reference"):
        st.markdown("""
        ### How Actions Are Selected

        The system uses 6 fixed numeric heuristics to determine which actions to activate:

        | Heuristic | Trigger Condition | Impact Formula |
        |-----------|-------------------|----------------|
        | **H1** Industrial Reduction | SPI -1.0 to -1.5, Days > 45 | 5% reduction → +3 days |
        | **H2** Pressure Management | SPI -1.2 to -1.8, Days 30-45 | 10% pressure → +4 days |
        | **H3** Public Communication | SPI -1.0 to -2.0, Days > 30 | 3% reduction → +2 days |
        | **H4** Non-Essential Restriction | SPI ≤ -1.8, Days < 30 | 1% removed → +1.3 days |
        | **H5** Source Reallocation | SPI ≤ -2.0, Days 15-30 | 5% increase → +5 days |
        | **H6** Severity Escalation | Threshold crossed | Combined × 0.8 |

        ### AI Parameterization

        The AI orchestrator:
        1. **Does NOT invent new actions** - only selects from the 15-action catalog
        2. **Adjusts parameters** within allowed ranges
        3. **Provides numeric justification** for each recommendation
        4. **Falls back to defaults** if AI is unavailable

        All logic remains **auditable, numeric, and explainable**.
        """)

    # Footer navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Risk Overview"):
            st.switch_page("pages/1_risk_overview.py")
    with col3:
        if st.button("Run Simulation →"):
            st.switch_page("pages/3_simulation.py")


if __name__ == "__main__":
    main()
