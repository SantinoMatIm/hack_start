"""
Action card components for displaying recommended actions
"""

import streamlit as st
from typing import Optional


def get_priority_class(priority: str) -> str:
    """Get CSS class for priority level"""
    priority_map = {
        "HIGH": "high",
        "MEDIUM": "medium",
        "LOW": "low",
        "CRITICAL": "high"
    }
    return priority_map.get(priority.upper() if priority else "MEDIUM", "medium")


def render_action_card(action: dict, index: int = 0):
    """Render a single action card"""
    if not action:
        return

    title = action.get("title", action.get("base_action_id", "Unknown Action"))
    code = action.get("code", action.get("base_action_id", ""))
    parameters = action.get("parameters", {})
    justification = action.get("justification", "")
    expected_effect = action.get("expected_effect", "")
    priority = parameters.get("priority_level", "MEDIUM") if parameters else "MEDIUM"
    priority_class = get_priority_class(priority)

    # Build parameters display
    params_html = ""
    if parameters:
        params_html = '<div style="margin-top: 16px;"><strong style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted);">Parameters</strong><ul style="margin-top: 8px; padding-left: 20px;">'
        for key, value in parameters.items():
            if key != "priority_level":
                formatted_key = key.replace("_", " ").title()
                if isinstance(value, float):
                    value = f"{value:.1f}"
                params_html += f'<li style="margin-bottom: 4px;"><span style="color: var(--text-muted);">{formatted_key}:</span> <strong>{value}</strong></li>'
        params_html += '</ul></div>'

    delay = index * 100

    st.markdown(f"""
    <div class="action-card reveal fade-up" style="transition-delay: {delay}ms;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
            <div>
                <span style="font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em;">{code}</span>
                <h3 style="margin: 4px 0 0 0; font-size: 20px;">{title}</h3>
            </div>
            <span class="action-priority {priority_class}">{priority}</span>
        </div>

        {params_html}

        {f'<div style="margin-top: 16px; padding: 16px; background: var(--bg-primary);"><strong style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--action-primary);">Expected Effect</strong><p style="margin: 8px 0 0 0; font-size: 16px;">{expected_effect}</p></div>' if expected_effect else ''}

        {f'<div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--accent-light);"><p style="font-size: 14px; color: var(--text-muted); margin: 0;"><strong>Justification:</strong> {justification}</p></div>' if justification else ''}
    </div>
    """, unsafe_allow_html=True)


def render_action_list(actions: list, title: str = "Recommended Actions"):
    """Render a list of action cards"""
    if not actions:
        st.info("No actions recommended for the current conditions.")
        return

    st.markdown(f"""
    <div class="section reveal fade-up">
        <h2 class="section-title">{title}</h2>
        <p style="color: var(--text-muted); margin-bottom: 32px;">
            {len(actions)} action{'s' if len(actions) != 1 else ''} recommended based on current risk assessment
        </p>
    </div>
    """, unsafe_allow_html=True)

    for i, action in enumerate(actions):
        render_action_card(action, i)


def render_action_summary(actions: list):
    """Render a summary of actions with total expected impact"""
    if not actions:
        return

    total_days = 0
    for action in actions:
        effect = action.get("expected_effect", "")
        # Try to extract days from effect string (e.g., "+6 days" or "~+6 days")
        import re
        match = re.search(r'\+?\~?(\d+(?:\.\d+)?)\s*days?', effect, re.IGNORECASE)
        if match:
            total_days += float(match.group(1))

    high_priority = sum(1 for a in actions if a.get("parameters", {}).get("priority_level", "").upper() == "HIGH")

    st.markdown(f"""
    <div class="dark-section reveal fade-up">
        <div style="max-width: 800px; margin: 0 auto; text-align: center;">
            <h2 style="margin-bottom: 32px;">Action Summary</h2>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 48px;">
                <div>
                    <div style="font-size: 48px; font-weight: 800;">{len(actions)}</div>
                    <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--accent-dark);">Total Actions</div>
                </div>
                <div>
                    <div style="font-size: 48px; font-weight: 800; color: var(--action-primary);">{high_priority}</div>
                    <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--accent-dark);">High Priority</div>
                </div>
                <div>
                    <div style="font-size: 48px; font-weight: 800; color: #10B981;">+{total_days:.0f}</div>
                    <div style="font-size: 14px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--accent-dark);">Est. Days Gained</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_heuristic_explanation(heuristic_id: str):
    """Render explanation for a specific heuristic"""
    heuristics = {
        "H1": {
            "name": "Moderate Industrial Reduction",
            "trigger": "SPI between -1.0 and -1.5, Trend STABLE/WORSENING, Days to critical > 45",
            "impact": "Each 5% reduction → +3 days to critical"
        },
        "H2": {
            "name": "Urban Network Pressure Management",
            "trigger": "SPI between -1.2 and -1.8, Trend WORSENING, Days to critical 30-45",
            "impact": "Each 10% pressure reduction → +4 days"
        },
        "H3": {
            "name": "Targeted Public Communication",
            "trigger": "SPI between -1.0 and -2.0, Trend WORSENING, Days to critical > 30",
            "impact": "3% domestic reduction → +2 days"
        },
        "H4": {
            "name": "Restriction of Non-Essential Uses",
            "trigger": "SPI ≤ -1.8, Trend WORSENING, Days to critical < 30",
            "impact": "1% removed → +1.3 days"
        },
        "H5": {
            "name": "Operational Source Reallocation",
            "trigger": "SPI ≤ -2.0, Trend STABLE/WORSENING, Days to critical 15-30",
            "impact": "5% supply increase → +5 days"
        },
        "H6": {
            "name": "Automatic Severity Escalation",
            "trigger": "SPI crosses threshold, Trend worsening, Days drop >20% in 2 weeks",
            "impact": "Combined actions with 20% penalty"
        }
    }

    h = heuristics.get(heuristic_id)
    if not h:
        return

    st.markdown(f"""
    <div style="background: var(--bg-surface); padding: 16px; border-left: 3px solid var(--action-primary); margin-top: 8px;">
        <strong>{h['name']}</strong>
        <p style="font-size: 14px; color: var(--text-muted); margin: 8px 0 0 0;">
            <strong>Trigger:</strong> {h['trigger']}<br/>
            <strong>Impact:</strong> {h['impact']}
        </p>
    </div>
    """, unsafe_allow_html=True)
