"""
Header and navigation components
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.icons import icon, icon_span


def render_header(title: str, subtitle: str = None):
    """Render a page header with optional subtitle"""
    st.markdown(f"""
    <div class="page-header fade-in" style="margin-bottom: var(--space-6);">
        <h1 style="margin-bottom: var(--space-1); font-size: 28px;">{title}</h1>
        {f'<p style="color: var(--text-muted); font-size: 15px; margin: 0;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def render_zone_selector(current_page: str = None):
    """Render the zone and profile selector in the sidebar with navigation"""
    with st.sidebar:
        # Logo and title
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid rgba(226, 232, 240, 0.6);">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(124, 58, 237, 0.08) 100%); border-radius: 11px; margin-bottom: 10px;">
                {icon("droplets", 22, "#2563EB")}
            </div>
            <div style="font-size: 14px; font-weight: 700; color: #0F172A; letter-spacing: -0.01em;">Water Risk</div>
            <div style="font-size: 10px; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.1em;">Intelligence</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation links
        st.markdown("""
        <div style="font-size: 10px; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 10px; font-weight: 600; padding-left: 4px;">Navigation</div>
        """, unsafe_allow_html=True)
        
        if st.button("Home", key="nav_home_sb", use_container_width=True, type="secondary" if current_page != "home" else "primary"):
            st.switch_page("app.py")
        
        if st.button("Risk Overview", key="nav_risk_sb", use_container_width=True, type="secondary" if current_page != "risk" else "primary"):
            st.switch_page("pages/1_risk_overview.py")
        
        if st.button("Actions", key="nav_actions_sb", use_container_width=True, type="secondary" if current_page != "actions" else "primary"):
            st.switch_page("pages/2_actions.py")
        
        if st.button("Simulation", key="nav_sim_sb", use_container_width=True, type="secondary" if current_page != "simulation" else "primary"):
            st.switch_page("pages/3_simulation.py")
        
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

        # Context section
        st.markdown("""
        <div style="font-size: 10px; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; font-weight: 600; padding-left: 4px;">Context</div>
        """, unsafe_allow_html=True)

        # Zone selection
        zone_options = {
            "cdmx": "Mexico City",
            "monterrey": "Monterrey",
            "baidoa": "Baidoa (Somalia) 🌡️"
        }

        current_zone = st.session_state.get("selected_zone", "cdmx")
        zone_index = list(zone_options.keys()).index(current_zone) if current_zone in zone_options else 0

        selected_zone = st.selectbox(
            "Zone",
            options=list(zone_options.keys()),
            format_func=lambda x: zone_options[x],
            index=zone_index,
            key="zone_selector"
        )

        if selected_zone != st.session_state.get("selected_zone"):
            st.session_state.selected_zone = selected_zone
            st.session_state.current_risk = None
            st.session_state.recommended_actions = None

        # Profile selection
        profile_options = {
            "government": "Government",
            "industry": "Industry"
        }

        selected_profile = st.selectbox(
            "Profile",
            options=list(profile_options.keys()),
            format_func=lambda x: profile_options[x],
            index=list(profile_options.keys()).index(st.session_state.get("selected_profile", "government")),
            key="profile_selector"
        )

        if selected_profile != st.session_state.get("selected_profile"):
            st.session_state.selected_profile = selected_profile
            st.session_state.recommended_actions = None

        # Current selection display
        zone_icons = {"cdmx": "building-2", "monterrey": "factory", "baidoa": "sun"}
        zone_icon = zone_icons.get(selected_zone, "map-pin")
        profile_icon = "landmark" if selected_profile == "government" else "briefcase"
        
        st.markdown(f"""
        <div class="sidebar-context" style="margin-top: 12px;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                {icon_span(zone_icon, 14, "#2563EB")}
                <span style="font-size: 13px; font-weight: 500; color: #0F172A;">{zone_options[selected_zone]}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                {icon_span(profile_icon, 14, "#2563EB")}
                <span style="font-size: 13px; font-weight: 500; color: #0F172A;">{selected_profile.title()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        return selected_zone, selected_profile


def render_breadcrumb(items: list):
    """Render a breadcrumb navigation"""
    breadcrumb_items = []
    for i, item in enumerate(items):
        if item.get("link"):
            breadcrumb_items.append(f'<a href="{item["link"]}" style="color: var(--text-muted); text-decoration: none;">{item["label"]}</a>')
        else:
            breadcrumb_items.append(f'<span style="color: var(--text-primary); font-weight: 500;">{item["label"]}</span>')
    
    separator = f' {icon("chevron-right", 14, "#94A3B8")} '
    breadcrumb_html = f'''
    <nav style="display: flex; align-items: center; gap: 4px; font-size: 13px; margin-bottom: 16px;">
        {separator.join(breadcrumb_items)}
    </nav>
    '''
    st.markdown(breadcrumb_html, unsafe_allow_html=True)


def render_back_button(label: str = "Back to Home"):
    """Render a back navigation button"""
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 4px; color: var(--text-muted); font-size: 14px; cursor: pointer;">
            {icon("arrow-left", 16, "#94A3B8")}
        </div>
        """, unsafe_allow_html=True)
        if st.button(label, key="back_btn", type="secondary"):
            st.switch_page("app.py")


def render_page_nav(prev_page: dict = None, next_page: dict = None):
    """Render previous/next page navigation"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    if prev_page:
        with col1:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 8px; color: var(--text-muted); font-size: 14px;">
                {icon("arrow-left", 16, "#94A3B8")}
                <span>{prev_page.get('label', 'Previous')}</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button(prev_page.get('label', 'Previous'), key="nav_prev", type="secondary"):
                st.switch_page(prev_page.get('page', 'app.py'))
    
    if next_page:
        with col3:
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: flex-end; gap: 8px; color: var(--accent-primary); font-size: 14px;">
                <span>{next_page.get('label', 'Next')}</span>
                {icon("arrow-right", 16, "#2563EB")}
            </div>
            """, unsafe_allow_html=True)
            if st.button(next_page.get('label', 'Next'), key="nav_next", type="primary"):
                st.switch_page(next_page.get('page', 'app.py'))
