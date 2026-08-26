"""Tests for database model constraints."""

from price_tracker.models import Listing, PriceHistory, Product, Seller


def test_product_columns() -> None:
    """Product should contain the expected required fields."""
    columns = Product.__table__.c

    assert columns.id.primary_key
    assert not columns.normalized_name.nullable
    assert columns.brand.nullable
    assert columns.model.nullable
    assert columns.category.nullable


def test_seller_columns() -> None:
    """Seller should contain the expected fields."""
    columns = Seller.__table__.c

    assert columns.id.primary_key
    assert not columns.seller_name.nullable
    assert columns.domain.nullable


def test_listing_foreign_keys() -> None:
    """Listing should reference products and sellers."""
    foreign_keys = {
        foreign_key.target_fullname
        for column in Listing.__table__.columns
        for foreign_key in column.foreign_keys
    }

    assert "products.id" in foreign_keys
    assert "sellers.id" in foreign_keys


def test_price_history_constraints() -> None:
    """Price history should reference listings and use decimal prices."""
    columns = PriceHistory.__table__.c

    foreign_keys = {
        foreign_key.target_fullname
        for column in PriceHistory.__table__.columns
        for foreign_key in column.foreign_keys
    }

    assert "listings.id" in foreign_keys
    assert not columns.price.nullable
    assert columns.price.type.precision == 12
    assert columns.price.type.scale == 2