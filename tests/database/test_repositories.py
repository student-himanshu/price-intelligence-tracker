"""Tests for database repositories."""

from unittest.mock import MagicMock

from price_tracker.models import Listing, PriceHistory, Product, Seller
from price_tracker.repositories.listing import ListingRepository
from price_tracker.repositories.price_history import PriceHistoryRepository
from price_tracker.repositories.product import ProductRepository
from price_tracker.repositories.seller import SellerRepository


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

def test_product_repository_get_by_normalized_name() -> None:
    """Product repository should find a product by normalized name."""
    session = MagicMock()
    product = Product(
        id=1,
        normalized_name="iphone 15 128gb",
    )
    session.scalar.return_value = product

    repository = ProductRepository(session)

    result = repository.get_by_normalized_name("iphone 15 128gb")

    assert result is product
    session.scalar.assert_called_once()

    statement = session.scalar.call_args.args[0]

    assert "products" in str(statement)
    assert list(statement.compile().params.values()) == ["iphone 15 128gb"]


def test_product_repository_add() -> None:
    """Product repository should add and flush a product."""
    session = MagicMock()
    product = Product(
        normalized_name="iphone 15 128gb",
    )

    repository = ProductRepository(session)

    result = repository.add(product)

    assert result is product
    session.add.assert_called_once_with(product)
    session.flush.assert_called_once()

def test_seller_repository_get_by_name() -> None:
    """Seller repository should find a seller by name."""
    session = MagicMock()
    seller = Seller(
        id=1,
        seller_name="Amazon",
        domain="amazon.in",
    )
    session.scalar.return_value = seller

    repository = SellerRepository(session)

    result = repository.get_by_name("Amazon")

    assert result is seller
    session.scalar.assert_called_once()

    statement = session.scalar.call_args.args[0]

    assert "sellers" in str(statement)
    assert list(statement.compile().params.values()) == ["Amazon"]


def test_seller_repository_add() -> None:
    """Seller repository should add and flush a seller."""
    session = MagicMock()
    seller = Seller(
        seller_name="Amazon",
        domain="amazon.in",
    )

    repository = SellerRepository(session)

    result = repository.add(seller)

    assert result is seller
    session.add.assert_called_once_with(seller)
    session.flush.assert_called_once()
    
def test_listing_repository_get_by_external_product_id() -> None:
    """Listing repository should find a listing by seller and external ID."""
    session = MagicMock()
    listing = Listing(
        id=1,
        product_id=10,
        seller_id=20,
        url="https://example.com/product",
        external_product_id="EXT-123",
    )
    session.scalar.return_value = listing

    repository = ListingRepository(session)

    result = repository.get_by_external_product_id(20, "EXT-123")

    assert result is listing
    session.scalar.assert_called_once()

    statement = session.scalar.call_args.args[0]

    assert "listings" in str(statement)
    assert set(statement.compile().params.values()) == {20, "EXT-123"}


def test_listing_repository_add() -> None:
    """Listing repository should add and flush a listing."""
    session = MagicMock()
    listing = Listing(
        product_id=10,
        seller_id=20,
        url="https://example.com/product",
    )

    repository = ListingRepository(session)

    result = repository.add(listing)

    assert result is listing
    session.add.assert_called_once_with(listing)
    session.flush.assert_called_once()


def test_listing_repository_list_by_product() -> None:
    """Listing repository should return listings for a product."""
    session = MagicMock()

    listings = [
        Listing(
            id=1,
            product_id=10,
            seller_id=20,
            url="https://example.com/1",
        ),
        Listing(
            id=2,
            product_id=10,
            seller_id=21,
            url="https://example.com/2",
        ),
    ]

    session.scalars.return_value.all.return_value = listings

    repository = ListingRepository(session)

    result = repository.list_by_product(10)

    assert result == listings
    session.scalars.assert_called_once()

    statement = session.scalars.call_args.args[0]

    assert "listings" in str(statement)
    assert list(statement.compile().params.values()) == [10]
    
def test_price_history_repository_add() -> None:
    """Price history repository should add and flush a record."""
    session = MagicMock()
    price_history = PriceHistory(
        listing_id=10,
        price=49999,
        original_price=54999,
        currency="INR",
    )

    repository = PriceHistoryRepository(session)

    result = repository.add(price_history)

    assert result is price_history
    session.add.assert_called_once_with(price_history)
    session.flush.assert_called_once()

def test_price_history_repository_get_latest() -> None:
    """Price history repository should return the latest observation."""
    session = MagicMock()

    latest = PriceHistory(
        id=2,
        listing_id=10,
        price=49999,
        currency="INR",
    )
    session.scalar.return_value = latest

    repository = PriceHistoryRepository(session)

    result = repository.get_latest(10)

    assert result is latest
    session.scalar.assert_called_once()

    statement = session.scalar.call_args.args[0]

    assert "price_history" in str(statement)

    params = statement.compile().params

    assert 10 in params.values()

def test_price_history_repository_list_by_listing() -> None:
    """Price history repository should return observations for a listing."""
    session = MagicMock()

    records = [
        PriceHistory(
            id=1,
            listing_id=10,
            price=54999,
            currency="INR",
        ),
        PriceHistory(
            id=2,
            listing_id=10,
            price=49999,
            currency="INR",
        ),
    ]

    session.scalars.return_value.all.return_value = records

    repository = PriceHistoryRepository(session)

    result = repository.list_by_listing(10)

    assert result == records
    session.scalars.assert_called_once()

    statement = session.scalars.call_args.args[0]

    assert "price_history" in str(statement)
    assert list(statement.compile().params.values()) == [10]