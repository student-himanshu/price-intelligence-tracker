"""Tests for the price history service."""
from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import MagicMock

from price_tracker.services.price_history_service import PriceHistoryService


def test_get_by_listing_id_returns_history_in_time_order() -> None:
    """History should be returned in collection-time order."""
    session = MagicMock()
    older = type(
        "FakePriceHistory",
        (),
        {
            "listing_id": 10,
            "price": Decimal("61999"),
            "collected_at": datetime(
                2026,
                8,
                27,
                10,
                tzinfo=UTC,
            ),
        },
    )()
    newer = type(
        "FakePriceHistory",
        (),
        {
            "listing_id": 10,
            "price": Decimal("59999"),
            "collected_at": datetime(
                2026,
                8,
                28,
                10,
                tzinfo=UTC,
            ),
        },
    )()
    session.scalars.return_value.all.return_value = [
        older,
        newer,
    ]
    service = PriceHistoryService(session)
    result = service.get_by_listing_id(10)
    assert result == [older, newer]
    session.scalars.assert_called_once()
def test_get_by_listing_id_returns_empty_list() -> None:
    """Missing history should return an empty list."""
    session = MagicMock()
    session.scalars.return_value.all.return_value = []
    service = PriceHistoryService(session)
    result = service.get_by_listing_id(999)
    assert result == []
    session.scalars.assert_called_once()
