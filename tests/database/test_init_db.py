"""Tests for database initialization."""

from unittest.mock import MagicMock

from price_tracker.database.init_db import initialize_database


def test_initialize_database(monkeypatch) -> None:
    """Database initialization should create all registered tables."""
    engine = MagicMock()
    metadata = MagicMock()

    monkeypatch.setattr(
        "price_tracker.database.init_db.get_engine",
        lambda: engine,
    )
    monkeypatch.setattr(
        "price_tracker.database.init_db.Base.metadata",
        metadata,
    )

    initialize_database()

    metadata.create_all.assert_called_once_with(bind=engine)