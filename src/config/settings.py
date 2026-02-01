"""Pydantic Settings for environment configuration."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database (optional for demo mode)
    database_url: str = ""

    # OpenAI
    openai_api_key: str = ""

    # EIA (Energy Information Administration)
    eia_api_key: str = ""

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Environment
    environment: str = "development"
    debug: bool = True

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_demo_mode(self) -> bool:
        """Check if running in demo mode (no database)."""
        return not self.database_url


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
