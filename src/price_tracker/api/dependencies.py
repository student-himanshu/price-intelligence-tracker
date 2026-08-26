"""FastAPI dependencies."""

from collections.abc import Generator

from sqlalchemy.orm import Session

from price_tracker.database.session import get_session


def get_db() -> Generator[Session, None, None]:
    """Provide a database session for a request."""
    yield from get_session()