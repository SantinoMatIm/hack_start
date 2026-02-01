"""
Action card components for displaying recommended actions
"""

import streamlit as st
from typing import Optional
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.icons import icon, icon_span


def get_priority_class(priority: str) -> str:
    """Get CSS class for priority level"""
    priority_map = {
        "HIGH": "high",
        "MEDIUM": "medium",
        "LOW": "low",
        "CRITICAL": "high"
    }
    return priority_map.get(priority.upper() if priority else "MEDIUM", "medium")


def get_priority_color(priority: str) -> tuple:
    """Get background and text color for priority"""
    colors = {
        "HIGH": ("#FFF7ED", "#EA580C"),
        "MEDIUM": ("#FFFBEB", "#D97706"),
        "LOW": ("#ECFDF5", "#059669"),
        "CRITICAL": ("#FEF2F2", "#DC2626")
    }
    return colors.get(priority.upper() if priority else "MEDIUM", ("#F1F5F9", "#475569"))


def get_action_icon(code: str) -> str:
    """Get icon name for action type"""
    if "PRESSURE" in code.upper():
        return "gauge"
    elif "LAWN" in code.upper() or "GARDEN" in code.upper():
        return "sun"
    elif "AWARENESS" in code.upper() or "CAMPAIGN" in code.upper():
        return "users"
    elif "INDUSTRIAL" in code.upper():
        return "factory"
    elif "SOURCE" in code.upper() or "REALLOCATION" in code.upper():
        return "refresh-cw"
    elif "RESTRICTION" in code.upper():
        return "shield"
    else:
        return "zap"


def render_action_card(action: dict, index: int = 0):
    """Render a single action card"""
    if not action:
        return

    title = action.get("title", action.get("base_action_id", "Unknown Action"))
    code = action.get("code", action.get("base_action_id", ""))
    parameters = action.get("parameters", {})
    justification = action.get("justification", "")
    raw_effect = action.get("expected_effect", "")
    
    # Handle both dict and string formats for expected_effect
    if isinstance(raw_effect, dict):
        days = raw_effect.get("days_gained", 0)
        confidence = raw_effect.get("confidence", "")
        expected_effect = f"+{days} days" + (f" ({confidence})" if confidence else "")
    else:
        expected_effect = raw_effect
    
    priority = parameters.get("priority_level", "MEDIUM") if parameters else "MEDIUM"
    priority_class = get_priority_class(priority)
    bg_color, text_color = get_priority_color(priority)
    action_icon = get_action_icon(code)

    # Build parameters display
    params_html = ""
    if parameters:
        param_items = []
        for key, value in parameters.items():
            if key != "priority_level":
                formatted_key = key.replace("_", " ").title()
                if isinstance(value, float):
                    value = f"{value:.1f}"
                elif isinstance(value, list):
                    value = ", ".join(str(v) for v in value)
                param_items.append(f'<span style="color: var(--text-muted);">{formatted_key}:</span> <strong>{value}</strong>')
        
        if param_items:
            params_html = f'''
            <div style="margin-top: 16px; padding: 12px; background: var(--bg-surface); border-radius: 6px;">
                <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); margin-bottom: 8px;">Parameters</div>
                <div style="display: flex; flex-wrap: wrap; gap: 12px; font-size: 13px;">
                    {" · ".join(param_items)}
                </div>
            </div>
            '''

    st.markdown(f"""
    <div class="action-card fade-in" style="animation-delay: {index * 50}ms;">
        <div class="action-header">
            <div style="display: flex; align-items: flex-start; gap: 12px;">
                <div style="display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; background: var(--bg-surface); border-radius: 8px; flex-shrink: 0;">
                    {icon(action_icon, 18, "#475569")}
                </div>
                <div>
                    <div style="font-size: 11px; font-weight: 500; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em;">{code}</div>
                    <h3 style="margin: 2px 0 0 0; font-size: 17px; font-weight: 600;">{title}</h3>
                </div>
            </div>
            <span class="action-priority {priority_class}">{priority}</span>
        </div>

        {params_html}

        {f'''
        <div style="margin-top: 16px; padding: 12px; background: #ECFDF5; border-radius: 6px; display: flex; align-items: center; gap: 12px;">
            {icon_span("trending-up", 18, "#059669")}
            <div>
                <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #059669;">Expected Effect</div>
                <div style="font-size: 15px; font-weight: 600; color: #059669; margin-top: 2px;">{expected_effect}</div>
            </div>
        </div>
        ''' if expected_effect else ''}

        {f'''
        <div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border-default);">
            <div style="display: flex; align-items: flex-start; gap: 8px;">
                {icon_span("info", 14, "#94A3B8")}
                <p style="font-size: 13px; color: var(--text-muted); margin: 0; line-height: 1.5;">{justification}</p>
            </div>
        </div>
        ''' if justification else ''}
    </div>
    """, unsafe_allow_html=True)


def render_action_list(actions: list, title: str = "Recommended Actions"):
    """Render a list of action cards"""
    if not actions:
        st.markdown(f"""
        <div class="alert info" style="display: flex; align-items: center; gap: 12px;">
            {icon_span("info", 18, "#2563EB")}
            <span>No actions recommended for the current conditions.</span>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(f"""
    <div class="section fade-in">
        <h2 class="section-title">{title}</h2>
        <p style="color: var(--text-muted); margin-bottom: 24px;">
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
        # Handle both dict and string formats
        if isinstance(effect, dict):
            days_gained = effect.get("days_gained", 0)
            if days_gained:
                total_days += float(days_gained)
        elif isinstance(effect, str):
            import re
            match = re.search(r'\+?\~?(\d+(?:\.\d+)?)\s*days?', effect, re.IGNORECASE)
            if match:
                total_days += float(match.group(1))

    high_priority = sum(1 for a in actions if a.get("parameters", {}).get("priority_level", "").upper() == "HIGH")

    st.markdown(f"""
    <div class="dark-section fade-in">
        <div style="max-width: 800px; margin: 0 auto; text-align: center;">
            <h2 style="margin-bottom: 32px;">Action Summary</h2>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px;">
                <div>
                    <div style="display: flex; justify-content: center; margin-bottom: 8px;">
                        {icon_span("zap", 24, "#94A3B8")}
                    </div>
                    <div style="font-size: 42px; font-weight: 700;">{len(actions)}</div>
                    <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted);">Total Actions</div>
                </div>
                <div>
                    <div style="display: flex; justify-content: center; margin-bottom: 8px;">
                        {icon_span("alert-triangle", 24, "#EA580C")}
                    </div>
                    <div style="font-size: 42px; font-weight: 700; color: #EA580C;">{high_priority}</div>
                    <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted);">High Priority</div>
                </div>
                <div>
                    <div style="display: flex; justify-content: center; margin-bottom: 8px;">
                        {icon_span("trending-up", 24, "#059669")}
                    </div>
                    <div style="font-size: 42px; font-weight: 700; color: #059669;">+{total_days:.0f}</div>
                    <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted);">Est. Days Gained</div>
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
    <div style="background: var(--bg-surface); padding: 16px; border-left: 3px solid var(--accent-primary); border-radius: 0 8px 8px 0; margin-top: 8px;">
        <strong style="color: var(--text-primary);">{h['name']}</strong>
        <div style="font-size: 13px; color: var(--text-muted); margin-top: 8px; line-height: 1.6;">
            <div style="display: flex; align-items: flex-start; gap: 8px; margin-bottom: 4px;">
                {icon_span("target", 14, "#94A3B8")}
                <span><strong>Trigger:</strong> {h['trigger']}</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 8px;">
                {icon_span("trending-up", 14, "#059669")}
                <span><strong>Impact:</strong> {h['impact']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
