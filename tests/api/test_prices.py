"""Tests for the price history API endpoints."""

from datetime import UTC, datetime
from decimal import Decimal

from fastapi.testclient import TestClient

from price_tracker.api.app import app

client = TestClient(app)


class FakePriceHistory:
    """Fake price history record returned by the service."""

    id = 1
    listing_id = 10
    price = Decimal("49999.00")
    original_price = Decimal("54999.00")
    discount_percentage = None
    currency = "INR"
    collected_at = datetime(2026, 8, 27, 10, 30, tzinfo=UTC)


class FakePriceHistoryService:
    """Fake price history service for API tests."""

    def __init__(self, session: object) -> None:
        self.session = session

    def get_by_id(self, price_history_id: int) -> FakePriceHistory | None:
        """Return a fake price history record."""
        if price_history_id == 1:
            return FakePriceHistory()

        return None


def test_get_price_history(monkeypatch) -> None:
    """Price history endpoint should return price data."""
    monkeypatch.setattr(
        "price_tracker.api.routes.prices.PriceHistoryService",
        FakePriceHistoryService,
    )

    response = client.get("/prices/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "listing_id": 10,
        "price": "49999.00",
        "original_price": "54999.00",
        "discount_percentage": None,
        "currency": "INR",
        "collected_at": "2026-08-27T10:30:00Z",
    }
    


def test_get_price_history_not_found(monkeypatch) -> None:
    """Price history endpoint should return 404 when missing."""
    monkeypatch.setattr(
        "price_tracker.api.routes.prices.PriceHistoryService",
        FakePriceHistoryService,
    )

    response = client.get("/prices/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Price history record not found.",
    }