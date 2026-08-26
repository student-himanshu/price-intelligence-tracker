"""Tests for the seller API endpoints."""

from fastapi.testclient import TestClient

from price_tracker.api.app import app

client = TestClient(app)


class FakeSeller:
    """Fake seller returned by the service."""

    id = 1
    seller_name = "Amazon"
    domain = "amazon.in"


class FakeSellerService:
    """Fake seller service for API tests."""

    def __init__(self, session: object) -> None:
        self.session = session

    def get_by_id(self, seller_id: int) -> FakeSeller | None:
        """Return a fake seller."""
        if seller_id == 1:
            return FakeSeller()

        return None


def test_get_seller(monkeypatch) -> None:
    """Seller endpoint should return seller data."""
    monkeypatch.setattr(
        "price_tracker.api.routes.sellers.SellerService",
        FakeSellerService,
    )

    response = client.get("/sellers/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "seller_name": "Amazon",
        "domain": "amazon.in",
    }


def test_get_seller_not_found(monkeypatch) -> None:
    """Seller endpoint should return 404 for a missing seller."""
    monkeypatch.setattr(
        "price_tracker.api.routes.sellers.SellerService",
        FakeSellerService,
    )

    response = client.get("/sellers/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Seller not found.",
    }