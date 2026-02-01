"""H11: Markov Transition - Predicción de Transición de Fase Probabilística.

Uses Markov chain analysis to predict probability of transitioning
to severe drought, activating preemptive measures when P > 60%.
"""

from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext
from src.config.constants import Trend


class H11MarkovTransition(BaseHeuristic):
    """
    H11: Markov Transition (Predicción de Transición de Fase Probabilística)

    Rationale:
    - Climate has short-term "memory" due to persistence
    - Historical transition probabilities are statistically informative
    - Waiting for deterministic confirmation is inefficient
    - Probabilistic activation allows preemptive resource positioning

    Activation:
    - transition_prob_to_severe > 60%

    Actions:
    - Preemptive activation of next-phase measures
    - Probability-based alerts to decision makers
    - Contingency preparation
    """

    HEURISTIC_ID = "H11"
    REQUIRES_MARKOV = True

    APPLICABLE_ACTION_CODES = [
        "H11_PREEMPTIVE_ACTIVATION",
        "H11_PROBABILITY_ALERT",
        "H11_CONTINGENCY_PREPARATION",
    ]

    PROBABILITY_THRESHOLD = 0.60  # 60%

    def check_activation(self, context: HeuristicContext) -> bool:
        """High probability of transitioning to severe drought."""
        if context.transition_prob_to_severe is None:
            return False

        return context.transition_prob_to_severe > self.PROBABILITY_THRESHOLD

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Priority scales with transition probability:
        - 60-70%: moderate priority
        - 70-80%: high priority
        - >80%: critical priority
        """
        if context.transition_prob_to_severe is None:
            return 0

        prob = context.transition_prob_to_severe

        if prob > 0.80:
            return 80
        elif prob > 0.70:
            return 70
        elif prob > 0.60:
            return 60
        else:
            return 0

    def generate_justification(self, context: HeuristicContext) -> str:
        prob = context.transition_prob_to_severe or 0
        current_state = context.markov_current_state or "desconocido"

        prob_pct = prob * 100

        if prob > 0.80:
            urgency = "MUY ALTA"
        elif prob > 0.70:
            urgency = "ALTA"
        else:
            urgency = "MODERADA"

        return (
            f"[PREDICCIÓN MARKOV - Urgencia {urgency}] "
            f"Estado actual: {current_state}. "
            f"P(transición a severo) = {prob_pct:.0f}%. "
            f"Probabilidad supera umbral del 60%. "
            f"Activar medidas preventivas antes de que ocurra el deterioro."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        prob = context.transition_prob_to_severe or 0
        prob_extreme = context.transition_prob_to_extreme or 0

        return {
            "markov_current_state": context.markov_current_state,
            "transition_prob_to_severe": prob,
            "transition_prob_to_extreme": prob_extreme,
            "probability_threshold_used": self.PROBABILITY_THRESHOLD,
            "preemptive_measures": True,
            "contingency_level": (
                "full" if prob > 0.80 else
                "enhanced" if prob > 0.70 else
                "standard"
            ),
        }
