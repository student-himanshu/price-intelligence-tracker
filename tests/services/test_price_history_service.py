"""Tests for price history services."""

from unittest.mock import MagicMock

from pydantic import ValidationError

from price_tracker.models import PriceHistory
from price_tracker.schemas.price_history import PriceHistoryCreate
from price_tracker.services.price_history_service import PriceHistoryService


def test_get_by_id_delegates_to_repository() -> None:
    """Price history service should delegate ID lookup."""
    session = MagicMock()

    record = PriceHistory(
        id=1,
        listing_id=10,
        price=49999,
        currency="INR",
    )

    repository = MagicMock()
    repository.get_by_id.return_value = record

    service = PriceHistoryService(session)
    service.repository = repository

    result = service.get_by_id(1)

    assert result is record
    repository.get_by_id.assert_called_once_with(1)


def test_record_creates_price_history() -> None:
    """Service should validate and record a new price observation."""
    session = MagicMock()

    repository = MagicMock()

    created_record = PriceHistory(
        id=1,
        listing_id=10,
        price=49999,
        original_price=54999,
        currency="INR",
    )
    repository.add.return_value = created_record

    service = PriceHistoryService(session)
    service.repository = repository

    price_data = PriceHistoryCreate(
        listing_id=10,
        price=49999,
        original_price=54999,
        currency="INR",
    )

    result = service.record(price_data)

    assert result is created_record
    repository.add.assert_called_once()


def test_get_latest_delegates_to_repository() -> None:
    """Service should delegate latest-price lookup."""
    session = MagicMock()

    latest_record = PriceHistory(
        id=2,
        listing_id=10,
        price=49999,
        currency="INR",
    )

    repository = MagicMock()
    repository.get_latest.return_value = latest_record

    service = PriceHistoryService(session)
    service.repository = repository

    result = service.get_latest(10)

    assert result is latest_record
    repository.get_latest.assert_called_once_with(10)


def test_list_by_listing_delegates_to_repository() -> None:
    """Service should delegate listing price-history lookup."""
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

    repository = MagicMock()
    repository.list_by_listing.return_value = records

    service = PriceHistoryService(session)
    service.repository = repository

    result = service.list_by_listing(10)

    assert result == records
    repository.list_by_listing.assert_called_once_with(10)

def test_record_rejects_invalid_price() -> None:
    """Schema should reject invalid price before service access."""
    session = MagicMock()
    repository = MagicMock()

    service = PriceHistoryService(session)
    service.repository = repository

    try:
        PriceHistoryCreate(
            listing_id=10,
            price=0,
            original_price=54999,
            currency="INR",
        )
    except ValidationError:
        pass
    else:
        raise AssertionError("Invalid price should raise ValidationError")

    repository.add.assert_not_called()