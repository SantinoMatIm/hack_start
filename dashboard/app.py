"""
Water Risk Platform - Decision Intelligence Dashboard
Main Streamlit application entry point
"""

import streamlit as st
from pathlib import Path
import sys

# Add utils to path for icon imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.icons import icon, icon_span

# Page configuration
st.set_page_config(
    page_title="Water Risk Platform",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Fix sidebar collapse/expand buttons - consistent styling for both
st.markdown("""
<style>
/* ==========================================
   UNIFIED SIDEBAR TOGGLE BUTTON STYLING
   ========================================== */

/* COLLAPSE BUTTON (<<) - when sidebar is open */
[data-testid="stSidebarCollapseButton"] {
    opacity: 1 !important;
    visibility: visible !important;
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06) !important;
    padding: 8px !important;
    outline: none !important;
}

[data-testid="stSidebarCollapseButton"]:hover {
    background: #F8FAFC !important;
    border-color: #CBD5E1 !important;
}

[data-testid="stSidebarCollapseButton"]:not(:hover) {
    opacity: 1 !important;
}

[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stSidebarCollapseButton"] svg * {
    stroke: #64748B !important;
    color: #64748B !important;
}

/* EXPAND BUTTON (>>) - when sidebar is collapsed */
[data-testid="collapsedControl"] {
    opacity: 1 !important;
    visibility: visible !important;
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06) !important;
    padding: 8px !important;
    outline: none !important;
}

[data-testid="collapsedControl"]:hover {
    background: #F8FAFC !important;
    border-color: #CBD5E1 !important;
}

[data-testid="collapsedControl"]:not(:hover) {
    opacity: 1 !important;
}

[data-testid="collapsedControl"] svg,
[data-testid="collapsedControl"] svg * {
    stroke: #64748B !important;
    color: #64748B !important;
}
</style>
""", unsafe_allow_html=True)

# Load custom CSS
def load_css():
    css_file = Path(__file__).parent / "assets" / "styles.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Fix sidebar toggle button icon - make it BLACK and visible
    # Using very broad selectors and invert filter as fallback
    st.markdown("""
    <style>
    /* NUCLEAR OPTION: Target ANY button with SVG near the top-left area */
    /* This targets the Streamlit sidebar toggle specifically */
    
    /* Method 1: Direct filter to invert light icons to dark */
    [data-testid="collapsedControl"] svg,
    [data-testid="baseButton-headerNoPadding"] svg,
    .stApp > div:first-child button svg,
    header button svg,
    [data-testid="stHeader"] button svg {
        filter: invert(1) brightness(0) !important;
    }
    
    /* Method 2: Style the button container */
    [data-testid="collapsedControl"],
    [data-testid="baseButton-headerNoPadding"] {
        background: #F1F5F9 !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }
    
    /* Method 3: Target by class patterns Streamlit uses */
    button[class*="emotion"][class*="header"] svg,
    div[class*="emotion"][class*="collapse"] svg {
        filter: invert(1) brightness(0) !important;
    }
    
    /* Method 4: Any SVG in header area */
    [data-testid="stHeader"] svg,
    [data-testid="stHeader"] svg * {
        stroke: #0F172A !important;
        fill: #0F172A !important;
        color: #0F172A !important;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

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


def render_sidebar():
    """Render the sidebar with zone/profile selection"""
    with st.sidebar:
        # Logo and title
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 24px; padding-bottom: 20px; border-bottom: 1px solid rgba(226, 232, 240, 0.6);">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 48px; height: 48px; background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(124, 58, 237, 0.08) 100%); border-radius: 12px; margin-bottom: 12px;">
                {icon("droplets", 24, "#2563EB")}
            </div>
            <div style="font-size: 15px; font-weight: 700; color: #0F172A; letter-spacing: -0.01em;">Water Risk</div>
            <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.1em;">Intelligence Platform</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Zone & Profile Selection
        st.markdown("""
        <div style="font-size: 10px; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px; font-weight: 600; padding-left: 4px;">Configuration</div>
        """, unsafe_allow_html=True)
        
        zones_list = ["cdmx", "monterrey", "baidoa"]
        zone_names = {
            "cdmx": "Mexico City",
            "monterrey": "Monterrey",
            "baidoa": "Baidoa (Somalia) 🌡️"
        }
        zone = st.selectbox(
            "Zone",
            zones_list,
            index=zones_list.index(st.session_state.selected_zone) if st.session_state.selected_zone in zones_list else 0,
            format_func=lambda x: zone_names.get(x, x),
            key="sidebar_zone"
        )
        if zone != st.session_state.selected_zone:
            st.session_state.selected_zone = zone
            st.session_state.current_risk = None
            st.rerun()
        
        profile = st.selectbox(
            "Profile",
            ["government", "industry"],
            index=0 if st.session_state.selected_profile == "government" else 1,
            format_func=lambda x: x.title(),
            key="sidebar_profile"
        )
        if profile != st.session_state.selected_profile:
            st.session_state.selected_profile = profile
            st.session_state.recommended_actions = None
            st.rerun()


def main():
    # Render sidebar
    render_sidebar()
    
    # Hero Section
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-content fade-in-up">
            <div class="hero-badge">
                {icon_span("droplets", 14, "#2563EB")}
                <span>Decision Intelligence</span>
            </div>
            <h1 class="display-text">Water Risk Intelligence</h1>
            <p class="body-large">Transform climate data into operational decisions. Prioritize actions. Simulate outcomes.</p>
            <div class="hero-stats">
                <div class="hero-stat">
                    <span class="hero-stat-value">7</span>
                    <span class="hero-stat-label">Heuristics</span>
                </div>
                <div class="hero-stat-divider"></div>
                <div class="hero-stat">
                    <span class="hero-stat-value">16</span>
                    <span class="hero-stat-label">Actions</span>
                </div>
                <div class="hero-stat-divider"></div>
                <div class="hero-stat">
                    <span class="hero-stat-value">3</span>
                    <span class="hero-stat-label">Zones</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Decision Workflow - Cards with integrated buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid rgba(226, 232, 240, 0.8); border-radius: 16px 16px 0 0; padding: 24px; text-align: center;">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 52px; height: 52px; background: #DBEAFE; border-radius: 14px; margin-bottom: 16px;">
                {icon("bar-chart-3", 24, "#2563EB")}
            </div>
            <h3 style="font-size: 16px; font-weight: 600; color: #0F172A; margin: 0 0 8px 0;">Risk Overview</h3>
            <p style="font-size: 13px; color: #64748B; margin: 0; line-height: 1.5;">Current SPI, risk level, and time to critical threshold</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Risk →", key="nav_risk", use_container_width=True):
            st.switch_page("pages/1_risk_overview.py")
    
    with col2:
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid rgba(226, 232, 240, 0.8); border-radius: 16px 16px 0 0; padding: 24px; text-align: center;">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 52px; height: 52px; background: #DBEAFE; border-radius: 14px; margin-bottom: 16px;">
                {icon("zap", 24, "#2563EB")}
            </div>
            <h3 style="font-size: 16px; font-weight: 600; color: #0F172A; margin: 0 0 8px 0;">Actions</h3>
            <p style="font-size: 13px; color: #64748B; margin: 0; line-height: 1.5;">AI-parameterized interventions based on conditions</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Actions →", key="nav_actions", use_container_width=True):
            st.switch_page("pages/2_actions.py")
    
    with col3:
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid rgba(226, 232, 240, 0.8); border-radius: 16px 16px 0 0; padding: 24px; text-align: center;">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 52px; height: 52px; background: #DBEAFE; border-radius: 14px; margin-bottom: 16px;">
                {icon("git-compare", 24, "#2563EB")}
            </div>
            <h3 style="font-size: 16px; font-weight: 600; color: #0F172A; margin: 0 0 8px 0;">Simulation</h3>
            <p style="font-size: 13px; color: #64748B; margin: 0; line-height: 1.5;">Compare scenarios with quantified projections</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Run Simulation →", key="nav_sim", use_container_width=True):
            st.switch_page("pages/3_simulation.py")

    # Footer - Light theme to match page
    st.markdown(f"""
    <div style="margin-top: 64px; padding: 32px 24px; text-align: center; border-top: 1px solid rgba(226, 232, 240, 0.8);">
        <div style="display: flex; justify-content: center; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(124, 58, 237, 0.08) 100%); border-radius: 10px;">
                {icon("droplets", 18, "#2563EB")}
            </div>
        </div>
        <p style="font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: #64748B; margin: 0 0 4px 0;">Decision Intelligence for Water Risk</p>
        <p style="font-size: 13px; color: #94A3B8; margin: 0;">Mexico City • Monterrey • Baidoa</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
