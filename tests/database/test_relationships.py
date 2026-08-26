"""Tests for SQLAlchemy model relationships."""

from price_tracker.models import Listing, PriceHistory, Product, Seller


def test_product_has_listings_relationship() -> None:
    """Product should expose its listings relationship."""
    relationship = Product.__mapper__.relationships["listings"]

    assert relationship.back_populates == "product"


def test_seller_has_listings_relationship() -> None:
    """Seller should expose its listings relationship."""
    relationship = Seller.__mapper__.relationships["listings"]

    assert relationship.back_populates == "seller"


def test_listing_has_product_relationship() -> None:
    """Listing should expose its product relationship."""
    relationship = Listing.__mapper__.relationships["product"]

    assert relationship.back_populates == "listings"


def test_listing_has_seller_relationship() -> None:
    """Listing should expose its seller relationship."""
    relationship = Listing.__mapper__.relationships["seller"]

    assert relationship.back_populates == "listings"


def test_listing_has_price_history_relationship() -> None:
    """Listing should expose its price history relationship."""
    relationship = Listing.__mapper__.relationships["price_history"]

    assert relationship.back_populates == "listing"


def test_price_history_has_listing_relationship() -> None:
    """Price history should expose its listing relationship."""
    relationship = PriceHistory.__mapper__.relationships["listing"]

    assert relationship.back_populates == "price_history"