"""AI Orchestrator for action parameterization."""

from typing import Optional
from dataclasses import dataclass

from src.config.constants import Trend, Profile, RiskLevel
from src.ai_orchestrator.openai_client import OpenAIClient
from src.ai_orchestrator.prompt_templates import PromptTemplates
from src.ai_orchestrator.fallback_handler import FallbackHandler


@dataclass
class ParameterizedAction:
    """Result of action parameterization."""

    action_code: str
    parameters: dict
    justification: str
    expected_effect: dict
    method: str  # 'ai' or 'fallback'


class AIOrchestrator:
    """
    Orchestrate AI-based action parameterization.

    Purpose: Parametrize base actions from the catalog (NOT create new ones)

    Flow:
    1. Receive risk context + applicable actions from heuristics
    2. Call OpenAI with structured prompt
    3. Parse response and validate parameters within allowed ranges
    4. If AI fails, fallback to default parameters with trend-based adjustment
    """

    def __init__(
        self,
        openai_client: Optional[OpenAIClient] = None,
        fallback_handler: Optional[FallbackHandler] = None,
    ):
        self.openai = openai_client or OpenAIClient()
        self.fallback = fallback_handler or FallbackHandler()

    def parameterize_action(
        self,
        zone: str,
        spi: float,
        risk_level: RiskLevel,
        trend: Trend,
        days_to_critical: Optional[int],
        profile: Profile,
        action_code: str,
        action_title: str,
        action_description: str,
        impact_formula: str,
        default_urgency_days: int,
        parameter_schema: dict,
        default_parameters: dict,
    ) -> ParameterizedAction:
        """
        Parameterize a single action using AI or fallback.

        Args:
            zone: Zone identifier
            spi: Current SPI-6 value
            risk_level: Current risk level
            trend: Current trend
            days_to_critical: Days until critical
            profile: User profile
            action_code: Action code
            action_title: Action title
            action_description: Action description
            impact_formula: Impact formula string
            default_urgency_days: Default urgency
            parameter_schema: Schema for allowed parameters
            default_parameters: Default parameter values

        Returns:
            ParameterizedAction with optimized parameters
        """
        # Try AI first
        try:
            if self.openai.api_key:
                ai_result = self._parameterize_with_ai(
                    zone=zone,
                    spi=spi,
                    risk_level=risk_level,
                    trend=trend,
                    days_to_critical=days_to_critical,
                    profile=profile,
                    action_code=action_code,
                    action_title=action_title,
                    action_description=action_description,
                    impact_formula=impact_formula,
                    default_urgency_days=default_urgency_days,
                    parameter_schema=parameter_schema,
                    default_parameters=default_parameters,
                )

                if ai_result:
                    # Validate parameters are within allowed ranges
                    validated_params = self._validate_parameters(
                        ai_result.get("parameters", {}),
                        parameter_schema,
                    )

                    return ParameterizedAction(
                        action_code=action_code,
                        parameters=validated_params,
                        justification=ai_result.get("justification", ""),
                        expected_effect=ai_result.get("expected_effect", {}),
                        method="ai",
                    )
        except Exception as e:
            print(f"AI parameterization failed: {e}")

        # Fallback to heuristic-based parameters
        return self._parameterize_with_fallback(
            action_code=action_code,
            trend=trend,
            spi=spi,
            days_to_critical=days_to_critical,
            parameter_schema=parameter_schema,
            default_parameters=default_parameters,
            impact_formula=impact_formula,
        )

    def _parameterize_with_ai(
        self,
        zone: str,
        spi: float,
        risk_level: RiskLevel,
        trend: Trend,
        days_to_critical: Optional[int],
        profile: Profile,
        action_code: str,
        action_title: str,
        action_description: str,
        impact_formula: str,
        default_urgency_days: int,
        parameter_schema: dict,
        default_parameters: dict,
    ) -> Optional[dict]:
        """Use AI to parameterize action."""
        prompt = PromptTemplates.format_action_prompt(
            zone=zone,
            spi=spi,
            risk_level=risk_level.value,
            trend=trend.value,
            days_to_critical=days_to_critical,
            profile=profile.value,
            action_code=action_code,
            action_title=action_title,
            action_description=action_description or "",
            impact_formula=impact_formula,
            default_urgency_days=default_urgency_days,
            parameter_schema=parameter_schema or {},
            default_parameters=default_parameters or {},
        )

        return self.openai.complete_json(
            system_prompt=PromptTemplates.SYSTEM_PROMPT,
            user_prompt=prompt,
        )

    def _parameterize_with_fallback(
        self,
        action_code: str,
        trend: Trend,
        spi: float,
        days_to_critical: Optional[int],
        parameter_schema: dict,
        default_parameters: dict,
        impact_formula: str,
    ) -> ParameterizedAction:
        """Use fallback handler when AI is unavailable."""
        parameters = self.fallback.generate_fallback_parameters(
            parameter_schema=parameter_schema,
            trend=trend,
            default_parameters=default_parameters,
        )

        justification = self.fallback.generate_justification(
            trend=trend,
            spi=spi,
            days_to_critical=days_to_critical,
        )

        expected_effect = self.fallback.estimate_effect(
            impact_formula=impact_formula,
            parameters=parameters,
        )

        return ParameterizedAction(
            action_code=action_code,
            parameters=parameters,
            justification=justification,
            expected_effect=expected_effect,
            method="fallback",
        )

    def _validate_parameters(
        self,
        parameters: dict,
        schema: dict,
    ) -> dict:
        """
        Validate and clamp parameters to allowed ranges.

        Args:
            parameters: Parameters from AI
            schema: Parameter schema with ranges

        Returns:
            Validated parameters
        """
        if not schema:
            return parameters

        validated = {}

        for param_name, value in parameters.items():
            if param_name not in schema:
                # Keep unknown parameters as-is
                validated[param_name] = value
                continue

            spec = schema[param_name]

            # Clamp numeric values to range
            if "min" in spec and "max" in spec:
                if isinstance(value, (int, float)):
                    clamped = max(spec["min"], min(spec["max"], value))
                    # Match type
                    if isinstance(spec["min"], int) and isinstance(spec["max"], int):
                        clamped = int(round(clamped))
                    validated[param_name] = clamped
                    continue

            # Validate options
            if "options" in spec:
                options = spec["options"]
                if value in options:
                    validated[param_name] = value
                elif options:
                    validated[param_name] = spec.get("default", options[0])
                continue

            # Keep as-is if no validation rules
            validated[param_name] = value

        # Add defaults for missing required parameters
        for param_name, spec in schema.items():
            if param_name not in validated and "default" in spec:
                validated[param_name] = spec["default"]

        return validated

    def parameterize_multiple(
        self,
        zone: str,
        spi: float,
        risk_level: RiskLevel,
        trend: Trend,
        days_to_critical: Optional[int],
        profile: Profile,
        actions: list[dict],
    ) -> list[ParameterizedAction]:
        """
        Parameterize multiple actions.

        Can use batch AI call or individual calls.

        Args:
            zone: Zone identifier
            spi: Current SPI
            risk_level: Risk level
            trend: Trend
            days_to_critical: Days to critical
            profile: User profile
            actions: List of action details

        Returns:
            List of ParameterizedAction
        """
        results = []

        for action in actions:
            result = self.parameterize_action(
                zone=zone,
                spi=spi,
                risk_level=risk_level,
                trend=trend,
                days_to_critical=days_to_critical,
                profile=profile,
                action_code=action.get("action_code", ""),
                action_title=action.get("title", ""),
                action_description=action.get("description", ""),
                impact_formula=action.get("impact_formula", ""),
                default_urgency_days=action.get("default_urgency_days", 7),
                parameter_schema=action.get("parameter_schema", {}),
                default_parameters=action.get("default_parameters", {}),
            )
            results.append(result)

        return results
