"""Action catalog for retrieving and managing base actions."""

from typing import Optional
import uuid

from sqlalchemy.orm import Session

from src.db.models import Action


class ActionCatalog:
    """
    Catalog of base actions available for drought response.

    Provides methods to query and filter actions from the database.
    """

    def __init__(self, session: Session):
        self.session = session

    def get_all_actions(self) -> list[Action]:
        """Get all actions in the catalog."""
        return self.session.query(Action).all()

    def get_action_by_code(self, code: str) -> Optional[Action]:
        """Get a specific action by its code."""
        return self.session.query(Action).filter(Action.code == code).first()

    def get_action_by_id(self, action_id: uuid.UUID) -> Optional[Action]:
        """Get a specific action by its ID."""
        return self.session.query(Action).filter(Action.id == action_id).first()

    def get_actions_by_heuristic(self, heuristic_id: str) -> list[Action]:
        """Get all actions associated with a heuristic."""
        return (
            self.session.query(Action)
            .filter(Action.heuristic == heuristic_id)
            .all()
        )

    def get_actions_for_spi(self, spi: float) -> list[Action]:
        """
        Get all actions applicable for a given SPI value.

        Args:
            spi: Current SPI-6 value

        Returns:
            List of applicable actions
        """
        return (
            self.session.query(Action)
            .filter(Action.spi_min <= spi)
            .filter(Action.spi_max >= spi)
            .all()
        )

    def get_actions_by_codes(self, codes: list[str]) -> list[Action]:
        """Get multiple actions by their codes."""
        if not codes:
            return []
        return (
            self.session.query(Action)
            .filter(Action.code.in_(codes))
            .all()
        )

    def to_dict(self, action: Action) -> dict:
        """Convert action to dictionary representation."""
        return {
            "id": str(action.id),
            "code": action.code,
            "title": action.title,
            "description": action.description,
            "heuristic": action.heuristic,
            "spi_min": action.spi_min,
            "spi_max": action.spi_max,
            "impact_formula": action.impact_formula,
            "base_cost": action.base_cost,
            "default_urgency_days": action.default_urgency_days,
            "parameter_schema": action.parameter_schema,
        }
