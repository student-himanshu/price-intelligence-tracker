"""SQLAlchemy session configuration."""

from collections.abc import Generator
from functools import lru_cache

from sqlalchemy.orm import Session, sessionmaker

from price_tracker.database.engine import get_engine


@lru_cache(maxsize=1)
def get_session_factory() -> sessionmaker[Session]:
    """Return the cached SQLAlchemy session factory."""
    return sessionmaker(
        bind=get_engine(),
        class_=Session,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )


def get_session() -> Generator[Session, None, None]:
    """Yield a database session and close it after use."""
    session = get_session_factory()()

    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        