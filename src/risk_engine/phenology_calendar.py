"""Phenological calendar for detecting critical crop growth windows."""

from datetime import date
from typing import Optional


class PhenologyCalendar:
    """
    Calendar of critical phenological windows for major crops.

    Used by H4 (Phenological Stress) to elevate drought severity
    during sensitive crop growth stages like flowering and grain filling.

    Water stress during these critical windows can cause catastrophic
    yield losses that are disproportionate to the drought magnitude.
    """

    CRITICAL_WINDOWS = {
        "maiz": {
            "siembra": {
                "start": (3, 15),
                "end": (4, 30),
                "severity_multiplier": 1.2,
            },
            "floracion": {
                "start": (7, 1),
                "end": (8, 15),
                "severity_multiplier": 1.5,
            },
            "llenado_grano": {
                "start": (8, 15),
                "end": (9, 30),
                "severity_multiplier": 1.4,
            },
        },
        "frijol": {
            "floracion": {
                "start": (7, 15),
                "end": (8, 30),
                "severity_multiplier": 1.5,
            },
            "llenado": {
                "start": (8, 15),
                "end": (9, 15),
                "severity_multiplier": 1.4,
            },
        },
        "trigo": {
            "encañado": {
                "start": (1, 15),
                "end": (2, 28),
                "severity_multiplier": 1.3,
            },
            "espigado": {
                "start": (2, 15),
                "end": (3, 31),
                "severity_multiplier": 1.5,
            },
        },
        "sorgo": {
            "floracion": {
                "start": (8, 1),
                "end": (9, 15),
                "severity_multiplier": 1.5,
            },
            "llenado_grano": {
                "start": (9, 1),
                "end": (10, 15),
                "severity_multiplier": 1.4,
            },
        },
        "cebada": {
            "espigado": {
                "start": (2, 1),
                "end": (3, 15),
                "severity_multiplier": 1.5,
            },
        },
        "avena": {
            "espigado": {
                "start": (2, 15),
                "end": (4, 15),
                "severity_multiplier": 1.4,
            },
        },
    }

    MOST_CRITICAL_STAGES = [
        "floracion",
        "espigado",
        "llenado",
        "llenado_grano",
    ]

    def __init__(self, crops: list[str] = None):
        """
        Initialize calendar for specific crops.

        Args:
            crops: List of crops to monitor (default: maiz, frijol)
        """
        self.crops = crops or ["maiz", "frijol"]

    def _is_in_window(
        self,
        ref_date: date,
        start: tuple[int, int],
        end: tuple[int, int]
    ) -> bool:
        """Check if date is within window (month, day) tuples."""
        start_date = date(ref_date.year, start[0], start[1])
        end_date = date(ref_date.year, end[0], end[1])

        if start_date <= end_date:
            return start_date <= ref_date <= end_date
        else:
            return ref_date >= start_date or ref_date <= end_date

    def is_critical_period(
        self,
        ref_date: Optional[date] = None
    ) -> dict:
        """
        Check if currently in a critical phenological period.

        Args:
            ref_date: Reference date (default: today)

        Returns:
            Dictionary with:
            - is_critical: Whether in critical period
            - crops_affected: List of affected crops
            - stages: List of "crop:stage" strings
            - max_severity_multiplier: Highest multiplier among active windows
        """
        ref_date = ref_date or date.today()
        affected_crops = []
        stages = []
        max_multiplier = 1.0

        for crop in self.crops:
            if crop not in self.CRITICAL_WINDOWS:
                continue

            for stage, window in self.CRITICAL_WINDOWS[crop].items():
                if self._is_in_window(ref_date, window["start"], window["end"]):
                    affected_crops.append(crop)
                    stages.append(f"{crop}:{stage}")
                    max_multiplier = max(
                        max_multiplier,
                        window["severity_multiplier"]
                    )

        return {
            "is_critical": len(affected_crops) > 0,
            "crops_affected": list(set(affected_crops)),
            "stages": stages,
            "max_severity_multiplier": max_multiplier,
        }

    def get_stress_multiplier(
        self,
        ref_date: Optional[date] = None
    ) -> float:
        """
        Get severity multiplier based on current phenological stage.

        Higher multipliers during most critical stages (flowering, grain fill).

        Args:
            ref_date: Reference date

        Returns:
            Multiplier (1.0 = normal, up to 1.5 for critical stages)
        """
        result = self.is_critical_period(ref_date)
        return result["max_severity_multiplier"]

    def is_most_critical_stage(
        self,
        ref_date: Optional[date] = None
    ) -> bool:
        """
        Check if in the most critical stages (flowering, grain filling).

        Args:
            ref_date: Reference date

        Returns:
            True if in flowering or grain filling stage
        """
        result = self.is_critical_period(ref_date)

        for stage in result["stages"]:
            for critical in self.MOST_CRITICAL_STAGES:
                if critical in stage:
                    return True

        return False

    def get_upcoming_windows(
        self,
        ref_date: Optional[date] = None,
        days_ahead: int = 30
    ) -> list[dict]:
        """
        Get list of upcoming critical windows.

        Args:
            ref_date: Reference date
            days_ahead: Days to look ahead

        Returns:
            List of upcoming windows with crop, stage, start date
        """
        ref_date = ref_date or date.today()
        upcoming = []

        for crop in self.crops:
            if crop not in self.CRITICAL_WINDOWS:
                continue

            for stage, window in self.CRITICAL_WINDOWS[crop].items():
                start_date = date(
                    ref_date.year,
                    window["start"][0],
                    window["start"][1]
                )

                if start_date < ref_date:
                    start_date = date(
                        ref_date.year + 1,
                        window["start"][0],
                        window["start"][1]
                    )

                days_until = (start_date - ref_date).days
                if 0 < days_until <= days_ahead:
                    upcoming.append({
                        "crop": crop,
                        "stage": stage,
                        "start_date": start_date.isoformat(),
                        "days_until": days_until,
                        "severity_multiplier": window["severity_multiplier"],
                    })

        upcoming.sort(key=lambda x: x["days_until"])
        return upcoming

    def get_phenological_context(
        self,
        ref_date: Optional[date] = None
    ) -> dict:
        """
        Get complete phenological context for heuristic evaluation.

        Args:
            ref_date: Reference date

        Returns:
            Complete context dictionary for HeuristicContext
        """
        ref_date = ref_date or date.today()
        current = self.is_critical_period(ref_date)
        upcoming = self.get_upcoming_windows(ref_date, days_ahead=30)

        return {
            "is_critical_phenological_window": current["is_critical"],
            "crops_affected": current["crops_affected"],
            "phenological_stages": current["stages"],
            "severity_multiplier": current["max_severity_multiplier"],
            "is_most_critical_stage": self.is_most_critical_stage(ref_date),
            "upcoming_windows": upcoming,
        }
