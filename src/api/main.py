"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.settings import get_settings
from src.db.connection import init_db
from src.api.routers import (
    zones_router,
    ingestion_router,
    risk_router,
    actions_router,
    scenarios_router,
)

# Initialize FastAPI app
app = FastAPI(
    title="Water Risk Platform API",
    description="Decision Intelligence Platform for Water Risk (Drought)",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup."""
    try:
        init_db()
        print("Database connection initialized")
    except Exception as e:
        print(f"Warning: Failed to initialize database: {e}")


# Include routers
app.include_router(zones_router)
app.include_router(ingestion_router)
app.include_router(risk_router)
app.include_router(actions_router)
app.include_router(scenarios_router)


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "Water Risk Platform API",
        "version": "0.1.0",
        "description": "Decision Intelligence Platform for Water Risk (Drought)",
        "pilot_zones": ["cdmx", "monterrey"],
        "endpoints": {
            "zones": "/zones",
            "ingestion": "/ingestion/run",
            "risk": "/risk/current",
            "actions": "/actions/recommended",
            "scenarios": "/scenarios/simulate",
        },
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    try:
        settings = get_settings()
        return {
            "status": "healthy",
            "environment": settings.environment,
            "demo_mode": settings.is_demo_mode,
            "database_configured": bool(settings.database_url),
            "openai_configured": bool(settings.openai_api_key),
        }
    except Exception as e:
        return {
            "status": "healthy",
            "environment": "development",
            "demo_mode": True,
            "database_configured": False,
            "openai_configured": False,
            "note": "Running in demo mode"
        }


# Run with: uvicorn src.api.main:app --reload
if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
