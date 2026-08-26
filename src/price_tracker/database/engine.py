"""SQLAlchemy engine configuration for the application."""

from functools import lru_cache

from sqlalchemy import Engine, create_engine

from price_tracker.config.settings import get_settings


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """Create and return the cached SQLAlchemy engine."""
    settings = get_settings()

    return create_engine(
        settings.database.url,
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_size=5,
        max_overflow=10,
        future=True,
    )