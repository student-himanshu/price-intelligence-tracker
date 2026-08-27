"""Tests for the product API endpoints."""


from datetime import UTC, datetime

from fastapi.testclient import TestClient

from price_tracker.api.app import app


class FakeProduct:
    """Fake product returned by the service."""

    id = 1
    brand = "Apple"
    model = "iPhone 15"
    normalized_name = "apple iphone 15"
    category = "Smartphone"
    created_at = datetime(2026, 8, 27, 10, 0, tzinfo=UTC)
    updated_at = datetime(2026, 8, 27, 10, 0, tzinfo=UTC)

class FakeProductService:
    """Fake product service for API tests."""

    def __init__(self, session: object) -> None:
        self.session = session

    def get_by_id(self, product_id: int) -> FakeProduct | None:
        """Return a fake product."""
        if product_id == 1:
            return FakeProduct()

        return None


client = TestClient(app)


def test_get_product(monkeypatch) -> None:
    """Product endpoint should return product data."""
    monkeypatch.setattr(
        "price_tracker.api.routes.products.ProductService",
        FakeProductService,
    )

    response = client.get("/products/1")

    assert response.status_code == 200
    assert response.json() == {
    "id": 1,
    "brand": "Apple",
    "model": "iPhone 15",
    "normalized_name": "apple iphone 15",
    "category": "Smartphone",
    "created_at": "2026-08-27T10:00:00Z",
    "updated_at": "2026-08-27T10:00:00Z",
}


def test_get_product_not_found(monkeypatch) -> None:
    """Product endpoint should return 404 for a missing product."""
    monkeypatch.setattr(
        "price_tracker.api.routes.products.ProductService",
        FakeProductService,
    )

    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found.",
    }