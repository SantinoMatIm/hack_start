"""Alembic environment configuration."""

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db.models import Base
from src.config.settings import get_settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url():
    """Get database URL from settings."""
    return get_settings().database_url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    url = get_url()
    if not url:
        raise RuntimeError("DATABASE_URL not set. Configure .env before running migrations.")

    # Supabase pooler (port 6543) often hangs with Alembic. Use direct connection (port 5432).
    if "pooler.supabase.com" in url and ":6543" in url:
        print("\n*** WARNING: Pooler URL detected. Migrations may hang. ***")
        print("Use direct connection for migrations:")
        print("  postgresql://postgres:PASSWORD@db.PROJECT_REF.supabase.co:5432/postgres")
        print("  (Get it from Supabase Dashboard > Project Settings > Database)\n")

    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = url
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
