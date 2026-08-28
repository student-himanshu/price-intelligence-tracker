"""Tests for product-level price comparison API."""

from decimal import Decimal
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from price_tracker.api.app import app
from price_tracker.database.session import get_session

client = TestClient(app)


def test_get_product_price_comparison() -> None:
    """Comparison endpoint should return listings sorted by price."""
    product = MagicMock(
        id=193,
        normalized_name="apple iphone 15 128gb",
    )

    listing_one = MagicMock(
        id=194,
        product_id=193,
        seller_id=10,
        availability=True,
    )

    listing_two = MagicMock(
        id=195,
        product_id=193,
        seller_id=11,
        availability=True,
    )

    seller_one = MagicMock(
        seller_name="Amazon",
    )

    seller_two = MagicMock(
        seller_name="Flipkart",
    )

    price_one = MagicMock(
        listing_id=194,
        price=Decimal("61999.00"),
        currency="INR",
    )

    price_two = MagicMock(
        listing_id=195,
        price=Decimal("59999.00"),
        currency="INR",
    )

    session = MagicMock()
    session.get.side_effect = [
        product,
        seller_one,
        seller_two,
    ]

    listing_query = MagicMock()
    listing_query.filter.return_value.all.return_value = [
        listing_one,
        listing_two,
    ]

    price_query_one = MagicMock()
    price_query_one.filter.return_value.order_by.return_value.first.return_value = (
        price_one
    )

    price_query_two = MagicMock()
    price_query_two.filter.return_value.order_by.return_value.first.return_value = (
        price_two
    )

    session.query.side_effect = [
        listing_query,
        price_query_one,
        price_query_two,
    ]

    def override_get_session():
        """Provide the fake database session."""
        yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        response = client.get(
            "/analytics/products/193/comparison",
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == 193
    assert data["product_name"] == "apple iphone 15 128gb"
    assert data["lowest_price"] == "59999.00"
    assert data["seller_count"] == 2

    assert data["best_deal"]["seller_name"] == "Flipkart"
    assert data["best_deal"]["price"] == "59999.00"
    assert data["savings_vs_highest_price"] == "2000.00"

    assert data["listings"][0]["seller_name"] == "Flipkart"
    assert data["listings"][0]["price"] == "59999.00"
    assert data["listings"][1]["seller_name"] == "Amazon"
    assert data["listings"][1]["price"] == "61999.00"


def test_get_product_price_comparison_product_not_found() -> None:
    """Comparison endpoint should return 404 for an unknown product."""
    session = MagicMock()
    session.get.return_value = None

    def override_get_session():
        """Provide the fake database session."""
        yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        response = client.get(
            "/analytics/products/999/comparison",
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found.",
    }


def test_get_product_price_comparison_without_available_listing() -> None:
    """Best deal should be None when every listing is unavailable."""
    product = MagicMock(
        id=193,
        normalized_name="apple iphone 15 128gb",
    )

    listing = MagicMock(
        id=194,
        product_id=193,
        seller_id=10,
        availability=False,
    )

    seller = MagicMock(
        seller_name="Amazon",
    )

    price = MagicMock(
        listing_id=194,
        price=Decimal("61999.00"),
        currency="INR",
    )

    session = MagicMock()
    session.get.side_effect = [
        product,
        seller,
    ]

    listing_query = MagicMock()
    listing_query.filter.return_value.all.return_value = [listing]

    price_query = MagicMock()
    price_query.filter.return_value.order_by.return_value.first.return_value = (
        price
    )

    session.query.side_effect = [
        listing_query,
        price_query,
    ]

    def override_get_session():
        """Provide the fake database session."""
        yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        response = client.get(
            "/analytics/products/193/comparison",
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["seller_count"] == 1
    assert data["lowest_price"] == "61999.00"
    assert data["best_deal"] is None
    assert data["savings_vs_highest_price"] is None