"""Tests for listing services."""

from unittest.mock import MagicMock

from price_tracker.models import Listing
from price_tracker.schemas.listing import ListingCreate
from price_tracker.services.listing_service import ListingService


def test_get_by_id_delegates_to_repository() -> None:
    """Listing service should delegate ID lookup to the repository."""
    session = MagicMock()
    listing = Listing(
        id=1,
        product_id=10,
        seller_id=20,
        url="https://example.com/product",
    )

    repository = MagicMock()
    repository.get_by_id.return_value = listing

    service = ListingService(session)
    service.repository = repository

    result = service.get_by_id(1)

    assert result is listing
    repository.get_by_id.assert_called_once_with(1)


def test_get_or_create_returns_existing_listing() -> None:
    """Service should return an existing listing."""
    session = MagicMock()

    existing_listing = Listing(
        id=1,
        product_id=10,
        seller_id=20,
        url="https://example.com/product",
        external_product_id="EXT-123",
    )

    repository = MagicMock()
    repository.get_by_external_product_id.return_value = existing_listing

    service = ListingService(session)
    service.repository = repository

    listing_data = ListingCreate(
        product_id=10,
        seller_id=20,
        url="https://example.com/product",
        external_product_id="EXT-123",
    )

    result = service.get_or_create(listing_data)

    assert result is existing_listing
    repository.get_by_external_product_id.assert_called_once_with(
        20,
        "EXT-123",
    )
    repository.add.assert_not_called()


def test_get_or_create_creates_new_listing() -> None:
    """Service should create a listing when no existing listing is found."""
    session = MagicMock()

    repository = MagicMock()
    repository.get_by_external_product_id.return_value = None

    created_listing = Listing(
        id=1,
        product_id=10,
        seller_id=20,
        url="https://example.com/product",
        external_product_id="EXT-123",
    )
    repository.add.return_value = created_listing

    service = ListingService(session)
    service.repository = repository

    listing_data = ListingCreate(
        product_id=10,
        seller_id=20,
        url="https://example.com/product",
        external_product_id="EXT-123",
    )

    result = service.get_or_create(listing_data)

    assert result is created_listing
    repository.get_by_external_product_id.assert_called_once_with(
        20,
        "EXT-123",
    )
    repository.add.assert_called_once()


def test_list_by_product_delegates_to_repository() -> None:
    """Listing service should delegate product listing lookup."""
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

    repository = MagicMock()
    repository.list_by_product.return_value = listings

    service = ListingService(session)
    service.repository = repository

    result = service.list_by_product(10)

    assert result == listings
    repository.list_by_product.assert_called_once_with(10)
    
def test_get_or_create_creates_listing_without_external_product_id() -> None:
    """Service should create a listing without an external product ID."""
    session = MagicMock()

    repository = MagicMock()

    created_listing = Listing(
        id=1,
        product_id=10,
        seller_id=20,
        url="https://example.com/product",
    )
    repository.add.return_value = created_listing

    service = ListingService(session)
    service.repository = repository

    listing_data = ListingCreate(
        product_id=10,
        seller_id=20,
        url="https://example.com/product",
        external_product_id=None,
    )

    result = service.get_or_create(listing_data)

    assert result is created_listing
    repository.get_by_external_product_id.assert_not_called()
    repository.add.assert_called_once()