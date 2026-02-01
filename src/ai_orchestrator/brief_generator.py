"""AI brief generator for economic simulation results."""

from typing import Optional
from src.ai_orchestrator.openai_client import OpenAIClient


BRIEF_SYSTEM_PROMPT = """You are an expert energy infrastructure analyst. 
Your role is to provide clear, actionable insights on water stress impacts to power plants.
Be concise, specific, and focus on decision-relevant information.
Use professional but accessible language suitable for executive stakeholders."""


BRIEF_USER_PROMPT_TEMPLATE = """Analyze this economic simulation for water stress impact on power infrastructure:

**Current Conditions:**
- Zone: {zone_id}
- Current SPI (drought index): {spi} ({risk_level})
- Trend: {trend}
- Days to critical threshold: {days_to_critical}

**Infrastructure:**
- Power plants analyzed: {plants_count}
- Total capacity: {total_capacity_mw} MW
- Plant types: {plant_types}

**Economic Impact (over {projection_days} days):**
- Without action: ${no_action_cost:,.0f} total cost, {no_action_loss:.0%} average capacity loss
- With action: ${with_action_cost:,.0f} total cost, {with_action_loss:.0%} average capacity loss
- Potential savings: ${savings:,.0f} ({savings_pct:.1f}% reduction)

**Actions Selected:**
{actions_list}

Provide a brief analysis in this exact JSON format:
{{
  "executive_summary": "2-3 sentences summarizing the key finding and savings potential",
  "risk_context": "1-2 sentences on what the current drought conditions mean for power operations",
  "action_rationale": "1-2 sentences explaining why the selected actions are effective",
  "recommendation": "1-2 sentences with a clear, specific next step recommendation"
}}

Be specific with numbers and make recommendations actionable."""


def generate_ai_brief(
    zone_id: str,
    spi: float,
    risk_level: str,
    trend: str,
    days_to_critical: Optional[int],
    plants_count: int,
    total_capacity_mw: float,
    plant_types: list[str],
    projection_days: int,
    no_action_cost: float,
    no_action_loss: float,
    with_action_cost: float,
    with_action_loss: float,
    savings: float,
    savings_pct: float,
    actions: list[str],
) -> Optional[dict]:
    """Generate an AI brief for economic simulation results.
    
    Args:
        All simulation parameters and results
        
    Returns:
        Dict with executive_summary, risk_context, action_rationale, recommendation
        or None if generation fails
    """
    client = OpenAIClient()
    
    # Check if OpenAI is available
    if not client.api_key:
        return None
    
    # Format actions list
    if actions:
        actions_list = "\n".join(f"- {action}" for action in actions)
    else:
        actions_list = "- No specific actions selected (baseline scenario)"
    
    # Format plant types
    plant_types_str = ", ".join(set(plant_types)) if plant_types else "Mixed"
    
    prompt = BRIEF_USER_PROMPT_TEMPLATE.format(
        zone_id=zone_id,
        spi=spi,
        risk_level=risk_level,
        trend=trend,
        days_to_critical=days_to_critical or "N/A",
        plants_count=plants_count,
        total_capacity_mw=total_capacity_mw,
        plant_types=plant_types_str,
        projection_days=projection_days,
        no_action_cost=no_action_cost,
        no_action_loss=no_action_loss,
        with_action_cost=with_action_cost,
        with_action_loss=with_action_loss,
        savings=savings,
        savings_pct=savings_pct,
        actions_list=actions_list,
    )
    
    try:
        result = client.complete_json(
            system_prompt=BRIEF_SYSTEM_PROMPT,
            user_prompt=prompt,
            max_tokens=500,
            temperature=0.4,
        )
        
        if result and all(key in result for key in ["executive_summary", "risk_context", "action_rationale", "recommendation"]):
            return result
        
        return None
    except Exception as e:
        print(f"Failed to generate AI brief: {e}")
        return None


def get_fallback_brief(
    savings: float,
    savings_pct: float,
    risk_level: str,
    projection_days: int,
    actions: list[str],
) -> dict:
    """Generate a fallback brief when AI is unavailable.
    
    Returns a structured brief based on the simulation data.
    """
    if savings > 0:
        exec_summary = (
            f"Water conservation actions can save ${savings:,.0f} ({savings_pct:.1f}% cost reduction) "
            f"over the next {projection_days} days by reducing drought-related capacity losses."
        )
        recommendation = (
            f"Implement the selected actions immediately to capture these savings. "
            f"Monitor conditions and adjust as drought severity changes."
        )
    else:
        exec_summary = (
            f"Current analysis shows minimal economic benefit from water interventions "
            f"over the next {projection_days} days. Conditions may not warrant immediate action."
        )
        recommendation = (
            "Continue monitoring drought conditions. Re-run analysis if SPI worsens or "
            "consider preventive measures for long-term resilience."
        )
    
    risk_context = {
        "CRITICAL": "Extreme drought conditions require immediate attention. Power plant capacity is significantly impacted.",
        "HIGH": "Severe drought conditions are affecting power generation capacity. Proactive measures recommended.",
        "MEDIUM": "Moderate drought conditions present manageable risk. Monitoring and preventive actions advised.",
        "LOW": "Drought conditions are mild. Standard operations can continue with routine monitoring.",
    }.get(risk_level, "Drought conditions require assessment.")
    
    action_rationale = (
        f"The selected actions ({', '.join(actions[:2]) if actions else 'none'}) "
        f"help maintain water availability for power plant cooling systems, "
        f"reducing the need for capacity curtailment during drought periods."
    ) if actions else "No specific actions were selected for this simulation."
    
    return {
        "executive_summary": exec_summary,
        "risk_context": risk_context,
        "action_rationale": action_rationale,
        "recommendation": recommendation,
    }


# ============ SPI Simulation Brief ============

SPI_BRIEF_SYSTEM_PROMPT = """You are an expert water resource analyst specializing in drought risk assessment.
Your role is to provide clear, actionable insights on drought trajectory and water conservation actions.
Be concise, specific, and focus on decision-relevant information.
Use professional but accessible language suitable for water utility managers and government officials."""


SPI_BRIEF_USER_PROMPT_TEMPLATE = """Analyze this SPI (Standardized Precipitation Index) drought simulation:

**Current Conditions:**
- Zone: {zone_id}
- Current SPI: {current_spi} ({current_risk_level})
- Trend: {trend}
- Days to critical threshold: {days_to_critical_current}

**Projection Without Action ({projection_days} days):**
- Ending SPI: {ending_spi_no_action}
- Ending Risk Level: {ending_risk_no_action}
- Days to Critical: {days_to_critical_no_action}

**Projection With Action:**
- Ending SPI: {ending_spi_with_action}
- Ending Risk Level: {ending_risk_with_action}
- Days to Critical: {days_to_critical_with_action}

**Impact of Actions:**
- Days Gained: {days_gained}
- SPI Improvement: {spi_improvement}
- Risk Level Change: {risk_level_change}

**Actions Selected:**
{actions_list}

Provide a brief analysis in this exact JSON format:
{{
  "executive_summary": "2-3 sentences summarizing the drought trajectory and the value of taking action",
  "risk_context": "1-2 sentences on what the current and projected drought conditions mean for operations",
  "action_rationale": "1-2 sentences explaining why the selected actions help delay or mitigate the drought impact",
  "recommendation": "1-2 sentences with a clear, specific next step recommendation"
}}

Be specific with numbers and make recommendations actionable."""


def generate_spi_brief(
    zone_id: str,
    current_spi: float,
    current_risk_level: str,
    trend: str,
    days_to_critical_current: Optional[int],
    projection_days: int,
    ending_spi_no_action: float,
    ending_risk_no_action: str,
    days_to_critical_no_action: Optional[int],
    ending_spi_with_action: float,
    ending_risk_with_action: str,
    days_to_critical_with_action: Optional[int],
    days_gained: int,
    spi_improvement: float,
    risk_level_change: str,
    actions: list[str],
) -> Optional[dict]:
    """Generate an AI brief for SPI simulation results.
    
    Returns:
        Dict with executive_summary, risk_context, action_rationale, recommendation
        or None if generation fails
    """
    client = OpenAIClient()
    
    if not client.api_key:
        return None
    
    # Format actions list
    if actions:
        actions_list = "\n".join(f"- {action}" for action in actions)
    else:
        actions_list = "- No specific actions selected"
    
    prompt = SPI_BRIEF_USER_PROMPT_TEMPLATE.format(
        zone_id=zone_id,
        current_spi=current_spi,
        current_risk_level=current_risk_level,
        trend=trend,
        days_to_critical_current=days_to_critical_current or "N/A",
        projection_days=projection_days,
        ending_spi_no_action=ending_spi_no_action,
        ending_risk_no_action=ending_risk_no_action,
        days_to_critical_no_action=days_to_critical_no_action or "N/A",
        ending_spi_with_action=ending_spi_with_action,
        ending_risk_with_action=ending_risk_with_action,
        days_to_critical_with_action=days_to_critical_with_action or "N/A",
        days_gained=days_gained,
        spi_improvement=spi_improvement,
        risk_level_change=risk_level_change,
        actions_list=actions_list,
    )
    
    try:
        result = client.complete_json(
            system_prompt=SPI_BRIEF_SYSTEM_PROMPT,
            user_prompt=prompt,
            max_tokens=500,
            temperature=0.4,
        )
        
        if result and all(key in result for key in ["executive_summary", "risk_context", "action_rationale", "recommendation"]):
            return result
        
        return None
    except Exception as e:
        print(f"Failed to generate SPI brief: {e}")
        return None


def get_spi_fallback_brief(
    days_gained: int,
    spi_improvement: float,
    current_risk_level: str,
    ending_risk_no_action: str,
    ending_risk_with_action: str,
    projection_days: int,
    actions: list[str],
) -> dict:
    """Generate a fallback brief for SPI simulation when AI is unavailable."""
    
    if days_gained > 0:
        exec_summary = (
            f"Taking action delays critical drought conditions by {days_gained} days "
            f"and improves SPI by {spi_improvement:.2f} over the {projection_days}-day projection. "
            f"This provides valuable additional time to prepare for worsening conditions."
        )
        recommendation = (
            f"Implement the selected actions immediately to gain the projected {days_gained} days. "
            f"Use this time to prepare additional contingency measures if conditions continue worsening."
        )
    else:
        exec_summary = (
            f"The selected actions provide minimal impact on drought trajectory over {projection_days} days. "
            f"Consider more aggressive measures or alternative strategies."
        )
        recommendation = (
            "Re-evaluate action selection or consider implementing multiple complementary actions. "
            "Monitor conditions closely for any changes."
        )
    
    risk_context = {
        "CRITICAL": "Extreme drought conditions are present. Water resources are severely stressed and immediate action is required.",
        "HIGH": "Severe drought conditions are developing. Water conservation measures should be prioritized.",
        "MEDIUM": "Moderate drought conditions exist. Preventive measures can help avoid escalation.",
        "LOW": "Mild drought conditions. Good time for proactive planning and preventive measures.",
    }.get(current_risk_level, "Drought conditions require assessment.")
    
    action_rationale = (
        f"The selected actions ({', '.join(actions[:2]) if actions else 'none'}) "
        f"work by reducing water demand and improving efficiency, which helps maintain "
        f"water reserves longer during drought periods."
    ) if actions else "No specific actions were selected for this simulation."
    
    return {
        "executive_summary": exec_summary,
        "risk_context": risk_context,
        "action_rationale": action_rationale,
        "recommendation": recommendation,
    }
