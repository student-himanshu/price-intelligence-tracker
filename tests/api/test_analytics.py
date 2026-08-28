"""Tests for the price analytics API."""
from datetime import UTC, datetime
from decimal import Decimal

from fastapi.testclient import TestClient

from price_tracker.api.app import app

client = TestClient(app)
class FakePriceHistory:
    """Fake price history record for API tests."""
    def __init__(
        self,
        price: str,
        original_price: str | None,
        collected_at: datetime,
    ) -> None:
        self.price = Decimal(price)
        self.original_price = (
            Decimal(original_price)
            if original_price is not None
            else None
        )
        self.collected_at = collected_at
class FakePriceHistoryService:
    """Fake price history service for API tests."""
    def __init__(self, session: object) -> None:
        self.session = session
    def get_by_listing_id(self, listing_id: int) -> list[FakePriceHistory]:
        """Return deterministic price history."""
        if listing_id != 157:
            return []
        return [
            FakePriceHistory(
                "61999",
                "69999",
                datetime(2026, 8, 28, 10, 0, tzinfo=UTC),
            ),
        ]
def test_get_listing_analytics(monkeypatch) -> None:
    """Analytics endpoint should return calculated price metrics."""
    monkeypatch.setattr(
        "price_tracker.api.routes.analytics.PriceHistoryService",
        FakePriceHistoryService,
    )
    response = client.get("/analytics/listings/157")
    assert response.status_code == 200
    assert response.json() == {
        "current_price": "61999",
        "lowest_price": "61999",
        "highest_price": "61999",
        "average_price": "61999",
        "price_change": None,
        "price_change_percentage": None,
        "discount_percentage": "11.42873469620994585636937671",
    }
def test_get_listing_analytics_not_found(monkeypatch) -> None:
    """Analytics endpoint should return 404 without price history."""
    monkeypatch.setattr(
        "price_tracker.api.routes.analytics.PriceHistoryService",
        FakePriceHistoryService,
    )
    response = client.get("/analytics/listings/999")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Price history not found.",
    }

def test_get_listing_analytics_with_price_change(monkeypatch) -> None:
    """Analytics endpoint should return percentage price change."""
    first = FakePriceHistory(
        "61999",
        "69999",
        datetime(2026, 8, 27, 10, 0, tzinfo=UTC),
    )
    second = FakePriceHistory(
        "59999",
        "69999",
        datetime(2026, 8, 28, 10, 0, tzinfo=UTC),
    )

    class TwoPriceHistoryService:
        """Return two deterministic price observations."""

        def __init__(self, session: object) -> None:
            self.session = session

        def get_by_listing_id(
            self,
            listing_id: int,
        ) -> list[FakePriceHistory]:
            """Return two price observations."""
            return [first, second]

    monkeypatch.setattr(
        "price_tracker.api.routes.analytics.PriceHistoryService",
        TwoPriceHistoryService,
    )

    response = client.get("/analytics/listings/172")

    assert response.status_code == 200

    data = response.json()

    assert data["current_price"] == "59999"
    assert data["price_change"] == "-2000"
    assert data["price_change_percentage"] == "-3.2259"