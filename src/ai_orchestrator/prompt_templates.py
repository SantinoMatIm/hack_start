"""Prompt templates for AI orchestrator."""

from typing import Optional


class PromptTemplates:
    """Templates for AI prompts used in action parameterization."""

    SYSTEM_PROMPT = """You are a water resource management expert AI assistant.
Your role is to help parameterize drought response actions based on current conditions.

IMPORTANT RULES:
1. Only adjust parameters within the allowed ranges specified
2. Provide numeric values, not descriptive terms
3. Be conservative - err on the side of caution for public health
4. Consider the user profile (government vs industry) when making recommendations
5. Always return valid JSON

You will receive:
- Current risk context (SPI, trend, days to critical)
- An action to parameterize with its allowed parameter ranges
- User profile

You must return a JSON object with optimized parameters and a brief justification."""

    ACTION_PARAMETERIZATION_TEMPLATE = """
Current Risk Context:
- Zone: {zone}
- SPI-6: {spi} ({risk_level})
- Trend: {trend}
- Days to Critical: {days_to_critical}
- Profile: {profile}

Action to Parameterize:
- Code: {action_code}
- Title: {action_title}
- Description: {action_description}
- Impact Formula: {impact_formula}
- Default Urgency: {default_urgency_days} days

Allowed Parameter Ranges:
{parameter_schema}

Default Parameters (from heuristics):
{default_parameters}

Please optimize the parameters for the current situation. Consider:
1. The severity of the drought (SPI = {spi})
2. The trend direction ({trend})
3. Time available ({days_to_critical} days to critical)
4. The user profile ({profile})

Return a JSON object with this exact structure:
{{
    "parameters": {{
        // optimized parameter values within allowed ranges
    }},
    "justification": "Brief explanation of parameter choices",
    "expected_effect": {{
        "days_gained": <number>,
        "confidence": "high|medium|low"
    }}
}}
"""

    MULTI_ACTION_TEMPLATE = """
Current Risk Context:
- Zone: {zone}
- SPI-6: {spi} ({risk_level})
- Trend: {trend}
- Days to Critical: {days_to_critical}
- Profile: {profile}

Actions to Parameterize:
{actions_list}

For each action, provide optimized parameters considering:
1. How actions might interact or compound
2. Resource constraints (don't over-allocate)
3. Implementation sequence (some actions are prerequisites)

Return a JSON object with this exact structure:
{{
    "actions": [
        {{
            "action_code": "<code>",
            "parameters": {{ ... }},
            "justification": "...",
            "expected_effect": {{ "days_gained": <number>, "confidence": "high|medium|low" }},
            "priority_order": <number>
        }}
    ],
    "combined_effect": {{
        "total_days_gained": <number>,
        "interaction_notes": "..."
    }}
}}
"""

    @classmethod
    def format_action_prompt(
        cls,
        zone: str,
        spi: float,
        risk_level: str,
        trend: str,
        days_to_critical: Optional[int],
        profile: str,
        action_code: str,
        action_title: str,
        action_description: str,
        impact_formula: str,
        default_urgency_days: int,
        parameter_schema: dict,
        default_parameters: dict,
    ) -> str:
        """Format the action parameterization prompt."""
        # Format parameter schema as readable text
        schema_text = "\n".join([
            f"  - {param}: {details}"
            for param, details in (parameter_schema or {}).items()
        ]) or "  No specific parameters"

        # Format default parameters
        defaults_text = "\n".join([
            f"  - {param}: {value}"
            for param, value in (default_parameters or {}).items()
        ]) or "  Using system defaults"

        return cls.ACTION_PARAMETERIZATION_TEMPLATE.format(
            zone=zone,
            spi=spi,
            risk_level=risk_level,
            trend=trend,
            days_to_critical=days_to_critical if days_to_critical else "N/A",
            profile=profile,
            action_code=action_code,
            action_title=action_title,
            action_description=action_description or "No description",
            impact_formula=impact_formula,
            default_urgency_days=default_urgency_days,
            parameter_schema=schema_text,
            default_parameters=defaults_text,
        )

    @classmethod
    def format_multi_action_prompt(
        cls,
        zone: str,
        spi: float,
        risk_level: str,
        trend: str,
        days_to_critical: Optional[int],
        profile: str,
        actions: list[dict],
    ) -> str:
        """Format prompt for multiple actions."""
        actions_text = ""
        for i, action in enumerate(actions, 1):
            actions_text += f"""
{i}. {action['action_code']} - {action.get('title', 'Unknown')}
   Description: {action.get('description', 'N/A')}
   Impact: {action.get('impact_formula', 'N/A')}
   Parameters: {action.get('parameter_schema', {})}
   Defaults: {action.get('default_parameters', {})}
"""

        return cls.MULTI_ACTION_TEMPLATE.format(
            zone=zone,
            spi=spi,
            risk_level=risk_level,
            trend=trend,
            days_to_critical=days_to_critical if days_to_critical else "N/A",
            profile=profile,
            actions_list=actions_text,
        )
