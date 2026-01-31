"""
Header and navigation components
"""

import streamlit as st


def render_header(title: str, subtitle: str = None):
    """Render a page header with optional subtitle"""
    st.markdown(f"""
    <div class="page-header reveal fade-up">
        <h1>{title}</h1>
        {f'<p class="body-large">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def render_zone_selector():
    """Render the zone and profile selector in the sidebar"""
    with st.sidebar:
        st.markdown("### Configuration")

        # Zone selection
        zone_options = {
            "cdmx": "Mexico City (CDMX)",
            "monterrey": "Monterrey"
        }

        selected_zone = st.selectbox(
            "Select Zone",
            options=list(zone_options.keys()),
            format_func=lambda x: zone_options[x],
            index=list(zone_options.keys()).index(st.session_state.get("selected_zone", "cdmx")),
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
            "Select Profile",
            options=list(profile_options.keys()),
            format_func=lambda x: profile_options[x],
            index=list(profile_options.keys()).index(st.session_state.get("selected_profile", "government")),
            key="profile_selector"
        )

        if selected_profile != st.session_state.get("selected_profile"):
            st.session_state.selected_profile = selected_profile
            st.session_state.recommended_actions = None

        st.markdown("---")

        # Current selection display
        st.markdown(f"""
        **Current Selection:**
        - Zone: `{selected_zone.upper()}`
        - Profile: `{selected_profile.title()}`
        """)

        return selected_zone, selected_profile


def render_breadcrumb(items: list):
    """Render a breadcrumb navigation"""
    breadcrumb_html = '<nav class="breadcrumb">'
    for i, item in enumerate(items):
        if i > 0:
            breadcrumb_html += ' <span class="breadcrumb-separator">→</span> '
        if item.get("link"):
            breadcrumb_html += f'<a href="{item["link"]}">{item["label"]}</a>'
        else:
            breadcrumb_html += f'<span class="breadcrumb-current">{item["label"]}</span>'
    breadcrumb_html += '</nav>'

    st.markdown(breadcrumb_html, unsafe_allow_html=True)


def render_back_button(label: str = "← Back to Home"):
    """Render a back navigation button"""
    if st.button(label, key="back_btn"):
        st.switch_page("app.py")
