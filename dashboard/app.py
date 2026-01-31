"""
Water Risk Platform - Decision Intelligence Dashboard
Main Streamlit application entry point
"""

import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Water Risk Platform",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS
def load_css():
    css_file = Path(__file__).parent / "assets" / "styles.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Load animations
def load_animations():
    js_file = Path(__file__).parent / "assets" / "animations.js"
    if js_file.exists():
        with open(js_file) as f:
            st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)

# Inject animation observer
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
});
</script>
""", unsafe_allow_html=True)

# Session state initialization
if "selected_zone" not in st.session_state:
    st.session_state.selected_zone = "cdmx"
if "selected_profile" not in st.session_state:
    st.session_state.selected_profile = "government"
if "current_risk" not in st.session_state:
    st.session_state.current_risk = None
if "recommended_actions" not in st.session_state:
    st.session_state.recommended_actions = None
if "simulation_result" not in st.session_state:
    st.session_state.simulation_result = None


def main():
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content reveal fade-up">
            <h1 class="display-text">Water Risk<br/>Intelligence</h1>
            <p class="body-large">Transform climate data into operational decisions.<br/>
            Prioritize actions. Simulate outcomes. Act with confidence.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Zone Selection
    st.markdown('<div class="section reveal fade-up">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Select Zone</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        zone_selected = st.button(
            "🏙️ Mexico City (CDMX)",
            key="btn_cdmx",
            use_container_width=True,
            type="primary" if st.session_state.selected_zone == "cdmx" else "secondary"
        )
        if zone_selected:
            st.session_state.selected_zone = "cdmx"
            st.session_state.current_risk = None
            st.rerun()

    with col2:
        zone_selected = st.button(
            "🏭 Monterrey",
            key="btn_monterrey",
            use_container_width=True,
            type="primary" if st.session_state.selected_zone == "monterrey" else "secondary"
        )
        if zone_selected:
            st.session_state.selected_zone = "monterrey"
            st.session_state.current_risk = None
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Profile Selection
    st.markdown('<div class="section reveal fade-up">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Select Profile</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🏛️ Government",
            key="btn_gov",
            use_container_width=True,
            type="primary" if st.session_state.selected_profile == "government" else "secondary"
        ):
            st.session_state.selected_profile = "government"
            st.session_state.recommended_actions = None
            st.rerun()
        st.caption("Prioritizes: Impact + Urgency")

    with col2:
        if st.button(
            "🏢 Industry",
            key="btn_industry",
            use_container_width=True,
            type="primary" if st.session_state.selected_profile == "industry" else "secondary"
        ):
            st.session_state.selected_profile = "industry"
            st.session_state.recommended_actions = None
            st.rerun()
        st.caption("Prioritizes: Impact + Cost")

    st.markdown('</div>', unsafe_allow_html=True)

    # Current Selection Display
    st.markdown(f"""
    <div class="selection-badge reveal fade-up">
        <span class="badge-item">Zone: <strong>{st.session_state.selected_zone.upper()}</strong></span>
        <span class="badge-divider">|</span>
        <span class="badge-item">Profile: <strong>{st.session_state.selected_profile.title()}</strong></span>
    </div>
    """, unsafe_allow_html=True)

    # Navigation Cards
    st.markdown('<div class="section reveal fade-up">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Decision Workflow</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-card-number">01</div>
            <h3>Risk Overview</h3>
            <p>View current SPI, risk level, trend, and days to critical threshold.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Risk →", key="nav_risk", use_container_width=True):
            st.switch_page("pages/1_risk_overview.py")

    with col2:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-card-number">02</div>
            <h3>Recommended Actions</h3>
            <p>AI-parameterized actions based on current conditions and profile.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Actions →", key="nav_actions", use_container_width=True):
            st.switch_page("pages/2_actions.py")

    with col3:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-card-number">03</div>
            <h3>Simulation</h3>
            <p>Compare act vs. not-act scenarios with quantified outcomes.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Run Simulation →", key="nav_sim", use_container_width=True):
            st.switch_page("pages/3_simulation.py")

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer-section">
        <div class="footer-content reveal fade-up">
            <p class="footer-tagline">Decision Intelligence for Water Risk</p>
            <p class="footer-subtitle">Pilot zones: Mexico City • Monterrey</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
