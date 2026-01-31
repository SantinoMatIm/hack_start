"""API routers."""

from src.api.routers.zones import router as zones_router
from src.api.routers.ingestion import router as ingestion_router
from src.api.routers.risk import router as risk_router
from src.api.routers.actions import router as actions_router
from src.api.routers.scenarios import router as scenarios_router

__all__ = [
    "zones_router",
    "ingestion_router",
    "risk_router",
    "actions_router",
    "scenarios_router",
]
