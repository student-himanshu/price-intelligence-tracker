"""Tests for ORM model registration."""

from price_tracker.database.base import Base
from price_tracker.models import (
    Listing,
    PriceAlert,
    PriceHistory,
    Product,
    Seller,
)


def test_all_models_are_registered() -> None:
    """All expected ORM models should be registered in metadata."""
    expected_tables = {
        "products",
        "sellers",
        "listings",
        "price_history",
        "price_alerts",
    }

    assert expected_tables == set(Base.metadata.tables)


def test_price_alert_model_is_registered() -> None:
    """PriceAlert should be registered in SQLAlchemy metadata."""
    assert PriceAlert.__tablename__ in Base.metadata.tables


def test_all_expected_models_are_importable() -> None:
    """All ORM models should be importable from the models package."""
    assert Product is not None
    assert Seller is not None
    assert Listing is not None
    assert PriceHistory is not None
    assert PriceAlert is not None