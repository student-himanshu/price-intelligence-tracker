"""Tests for the listing API endpoints."""
from datetime import UTC, datetime

from fastapi.testclient import TestClient

from price_tracker.api.app import app

client = TestClient(app)


class FakeListing:
    """Fake listing returned by the service."""

    id = 1
    product_id = 10
    seller_id = 20
    url = "https://example.com/product/10"
    external_product_id = "EXT-10"
    availability = True
    created_at = datetime(2026, 8, 27, 10, 0, tzinfo=UTC)
    updated_at = datetime(2026, 8, 27, 10, 0, tzinfo=UTC)


class FakeListingService:
    """Fake listing service for API tests."""

    def __init__(self, session: object) -> None:
        self.session = session

    def get_by_id(self, listing_id: int) -> FakeListing | None:
        """Return a fake listing."""
        if listing_id == 1:
            return FakeListing()

        return None


def test_get_listing(monkeypatch) -> None:
    """Listing endpoint should return listing data."""
    monkeypatch.setattr(
        "price_tracker.api.routes.listings.ListingService",
        FakeListingService,
    )

    response = client.get("/listings/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "product_id": 10,
        "seller_id": 20,
        "url": "https://example.com/product/10",
        "external_product_id": "EXT-10",
        "availability": True,
        "created_at": "2026-08-27T10:00:00Z",
        "updated_at": "2026-08-27T10:00:00Z",
    }


def test_get_listing_not_found(monkeypatch) -> None:
    """Listing endpoint should return 404 for a missing listing."""
    monkeypatch.setattr(
        "price_tracker.api.routes.listings.ListingService",
        FakeListingService,
    )

    response = client.get("/listings/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Listing not found.",
    }