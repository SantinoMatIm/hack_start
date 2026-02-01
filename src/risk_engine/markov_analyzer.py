"""Markov chain analysis for drought state transition prediction."""

from typing import Optional
import numpy as np
import pandas as pd


class MarkovTransitionAnalyzer:
    """
    Markov chain analysis for predicting drought state transitions.

    Uses historical SPI data to build a transition probability matrix
    and predict future state probabilities.

    Used by H11 (Markovian Shift) to activate preemptive measures
    when probability of transitioning to severe drought exceeds threshold.
    """

    STATES = ["normal", "mild", "moderate", "severe", "extreme"]
    STATE_TO_IDX = {s: i for i, s in enumerate(STATES)}

    def __init__(self):
        """Initialize analyzer with empty transition matrix."""
        self.transition_matrix: Optional[np.ndarray] = None
        self._n_states = len(self.STATES)

    def spi_to_state(self, spi: float) -> str:
        """
        Map SPI value to categorical drought state.

        Classification based on standard SPI thresholds:
        - Normal: SPI > -0.5
        - Mild: -0.5 >= SPI > -1.0
        - Moderate: -1.0 >= SPI > -1.5
        - Severe: -1.5 >= SPI > -2.0
        - Extreme: SPI <= -2.0

        Args:
            spi: SPI value

        Returns:
            State name string
        """
        if spi > -0.5:
            return "normal"
        elif spi > -1.0:
            return "mild"
        elif spi > -1.5:
            return "moderate"
        elif spi > -2.0:
            return "severe"
        else:
            return "extreme"

    def spi_to_category(self, spi: float) -> int:
        """
        Map SPI to integer category (for flash drought detection).

        Categories:
        - 0: Wet (SPI > 0)
        - 1: Normal (0 >= SPI > -0.5)
        - 2: Mild (-0.5 >= SPI > -1.0)
        - 3: Moderate (-1.0 >= SPI > -1.5)
        - 4: Severe (-1.5 >= SPI > -2.0)
        - 5: Extreme (SPI <= -2.0)
        """
        if spi > 0:
            return 0
        elif spi > -0.5:
            return 1
        elif spi > -1.0:
            return 2
        elif spi > -1.5:
            return 3
        elif spi > -2.0:
            return 4
        else:
            return 5

    def fit_transition_matrix(
        self,
        spi_series: pd.DataFrame
    ) -> np.ndarray:
        """
        Estimate transition probability matrix from historical SPI data.

        Uses Maximum Likelihood Estimation (counting transitions).

        Args:
            spi_series: DataFrame with 'spi' column

        Returns:
            N x N transition probability matrix
        """
        if spi_series.empty or len(spi_series) < 2:
            self.transition_matrix = np.eye(self._n_states) / self._n_states
            return self.transition_matrix

        states = [self.spi_to_state(row["spi"]) for _, row in spi_series.iterrows()]

        counts = np.zeros((self._n_states, self._n_states))

        for i in range(len(states) - 1):
            from_idx = self.STATE_TO_IDX[states[i]]
            to_idx = self.STATE_TO_IDX[states[i + 1]]
            counts[from_idx, to_idx] += 1

        row_sums = counts.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1

        self.transition_matrix = counts / row_sums

        return self.transition_matrix

    def predict_transition_probability(
        self,
        current_state: str,
        target_state: str,
        steps: int = 1
    ) -> float:
        """
        Calculate probability of transitioning from current to target state.

        Args:
            current_state: Current drought state
            target_state: Target drought state
            steps: Number of time steps (months) to look ahead

        Returns:
            Transition probability (0-1)
        """
        if self.transition_matrix is None:
            return 0.0

        if current_state not in self.STATE_TO_IDX:
            return 0.0
        if target_state not in self.STATE_TO_IDX:
            return 0.0

        matrix_n = np.linalg.matrix_power(self.transition_matrix, steps)

        from_idx = self.STATE_TO_IDX[current_state]
        to_idx = self.STATE_TO_IDX[target_state]

        return float(matrix_n[from_idx, to_idx])

    def predict_worsening_probability(
        self,
        current_state: str,
        steps: int = 1
    ) -> float:
        """
        Calculate probability of transitioning to ANY worse state.

        Args:
            current_state: Current drought state
            steps: Number of time steps to look ahead

        Returns:
            Probability of worsening (0-1)
        """
        if self.transition_matrix is None:
            return 0.0

        if current_state not in self.STATE_TO_IDX:
            return 0.0

        current_idx = self.STATE_TO_IDX[current_state]

        if current_idx >= self._n_states - 1:
            return 0.0

        matrix_n = np.linalg.matrix_power(self.transition_matrix, steps)

        prob = 0.0
        for worse_idx in range(current_idx + 1, self._n_states):
            prob += matrix_n[current_idx, worse_idx]

        return float(prob)

    def get_steady_state(self) -> Optional[np.ndarray]:
        """
        Calculate steady-state distribution of the Markov chain.

        Returns:
            Steady-state probability vector or None if not fitted
        """
        if self.transition_matrix is None:
            return None

        eigenvalues, eigenvectors = np.linalg.eig(self.transition_matrix.T)

        idx = np.argmin(np.abs(eigenvalues - 1.0))
        steady = np.real(eigenvectors[:, idx])
        steady = steady / steady.sum()

        return steady

    def analyze_current_position(
        self,
        current_spi: float,
        spi_series: pd.DataFrame
    ) -> dict:
        """
        Complete analysis of current position and transition risks.

        Args:
            current_spi: Current SPI value
            spi_series: Historical SPI for fitting

        Returns:
            Dictionary with analysis results
        """
        self.fit_transition_matrix(spi_series)

        current_state = self.spi_to_state(current_spi)

        prob_severe = self.predict_transition_probability(
            current_state, "severe", steps=1
        )
        prob_extreme = self.predict_transition_probability(
            current_state, "extreme", steps=1
        )
        prob_worsening = self.predict_worsening_probability(current_state, steps=1)

        prob_severe_2m = self.predict_transition_probability(
            current_state, "severe", steps=2
        )
        prob_extreme_2m = self.predict_transition_probability(
            current_state, "extreme", steps=2
        )

        return {
            "current_state": current_state,
            "transition_prob_to_severe": prob_severe,
            "transition_prob_to_extreme": prob_extreme,
            "prob_worsening_1m": prob_worsening,
            "transition_prob_to_severe_2m": prob_severe_2m,
            "transition_prob_to_extreme_2m": prob_extreme_2m,
        }
