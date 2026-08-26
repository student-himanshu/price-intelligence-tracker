"""Tests for database repositories."""

from unittest.mock import MagicMock

from price_tracker.models import Listing, PriceHistory, Product, Seller
from price_tracker.repositories.listing import ListingRepository
from price_tracker.repositories.price_history import PriceHistoryRepository
from price_tracker.repositories.product import ProductRepository
from price_tracker.repositories.seller import SellerRepository
from sqlalchemy.sql import Select

def test_product_repository_get_by_id() -> None:
    """Product repository should query by product ID."""
    session = MagicMock()
    product = Product(id=1, normalized_name="test product")
    session.scalar.return_value = product

    repository = ProductRepository(session)

    result = repository.get_by_id(1)

    assert result is product
    session.scalar.assert_called_once()


def test_seller_repository_get_by_id() -> None:
    """Seller repository should query by seller ID."""
    session = MagicMock()
    seller = Seller(id=1, seller_name="Amazon")
    session.scalar.return_value = seller

    repository = SellerRepository(session)

    result = repository.get_by_id(1)

    assert result is seller
    session.scalar.assert_called_once()


def test_listing_repository_get_by_id() -> None:
    """Listing repository should query by listing ID."""
    session = MagicMock()
    listing = Listing(
        id=1,
        product_id=10,
        seller_id=20,
        url="https://example.com/product",
    )
    session.scalar.return_value = listing

    repository = ListingRepository(session)

    result = repository.get_by_id(1)

    assert result is listing
    session.scalar.assert_called_once()


def test_price_history_repository_get_by_id() -> None:
    """Price history repository should query by record ID."""
    session = MagicMock()
    price_history = PriceHistory(
        id=1,
        listing_id=10,
    )
    session.scalar.return_value = price_history

    repository = PriceHistoryRepository(session)

    result = repository.get_by_id(1)

    assert result is price_history
    session.scalar.assert_called_once()
def test_product_repository_returns_none_when_missing() -> None:
    """Product repository should return None when product is missing."""
    session = MagicMock()
    session.scalar.return_value = None

    repository = ProductRepository(session)

    assert repository.get_by_id(999) is None


def test_seller_repository_returns_none_when_missing() -> None:
    """Seller repository should return None when seller is missing."""
    session = MagicMock()
    session.scalar.return_value = None

    repository = SellerRepository(session)

    assert repository.get_by_id(999) is None


def test_listing_repository_returns_none_when_missing() -> None:
    """Listing repository should return None when listing is missing."""
    session = MagicMock()
    session.scalar.return_value = None

    repository = ListingRepository(session)

    assert repository.get_by_id(999) is None


def test_price_history_repository_returns_none_when_missing() -> None:
    """Price history repository should return None when record is missing."""
    session = MagicMock()
    session.scalar.return_value = None

    repository = PriceHistoryRepository(session)

    assert repository.get_by_id(999) is None
 
def test_product_repository_builds_id_query() -> None:
    """Product repository should build a SELECT filtered by product ID."""
    session = MagicMock()
    session.scalar.return_value = None

    repository = ProductRepository(session)

    repository.get_by_id(42)

    statement = session.scalar.call_args.args[0]

    assert "products" in str(statement)
    assert list(statement.compile().params.values()) == [42]


def test_seller_repository_builds_id_query() -> None:
    """Seller repository should build a SELECT filtered by seller ID."""
    session = MagicMock()
    session.scalar.return_value = None

    repository = SellerRepository(session)

    repository.get_by_id(42)

    statement = session.scalar.call_args.args[0]

    assert "sellers" in str(statement)
    assert list(statement.compile().params.values()) == [42]


def test_listing_repository_builds_id_query() -> None:
    """Listing repository should build a SELECT filtered by listing ID."""
    session = MagicMock()
    session.scalar.return_value = None

    repository = ListingRepository(session)

    repository.get_by_id(42)

    statement = session.scalar.call_args.args[0]

    assert "listings" in str(statement)
    assert list(statement.compile().params.values()) == [42]


def test_price_history_repository_builds_id_query() -> None:
    """Price history repository should build a SELECT filtered by record ID."""
    session = MagicMock()
    session.scalar.return_value = None

    repository = PriceHistoryRepository(session)

    repository.get_by_id(42)

    statement = session.scalar.call_args.args[0]

    assert "price_history" in str(statement)
    assert list(statement.compile().params.values()) == [42]