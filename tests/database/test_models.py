"""Tests for SQLAlchemy ORM models."""

from price_tracker import models
from price_tracker.database.base import Base


def test_all_models_are_registered() -> None:
    """All expected ORM models should be registered in metadata."""
    expected_tables = {
        "products",
        "sellers",
        "listings",
        "price_history",
    }

    assert expected_tables == set(Base.metadata.tables)
    assert models.Product.__tablename__ == "products"
    assert models.Seller.__tablename__ == "sellers"
    assert models.Listing.__tablename__ == "listings"
    assert models.PriceHistory.__tablename__ == "price_history"