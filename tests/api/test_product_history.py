"""Tests for product-level price history."""

from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from price_tracker.api.app import app
from price_tracker.database.session import get_session

client = TestClient(app)


def test_product_price_history() -> None:
    """Product history should return price observations by seller."""
    product = MagicMock(
        id=172,
        normalized_name="apple iphone 15 128gb",
    )

    listing_one = MagicMock(
        id=172,
        product_id=172,
        seller_id=115,
    )

    listing_two = MagicMock(
        id=175,
        product_id=172,
        seller_id=116,
    )

    seller_one = MagicMock(
        id=115,
        seller_name="demo electronics",
    )

    seller_two = MagicMock(
        id=116,
        seller_name="demo marketplace",
    )

    history_one = MagicMock(
        id=199,
        listing_id=172,
        price=Decimal("61999.00"),
        currency="INR",
        collected_at=datetime(
            2026,
            8,
            28,
            10,
            0,
            tzinfo=UTC,
        ),
    )

    history_two = MagicMock(
        id=202,
        listing_id=175,
        price=Decimal("59999.00"),
        currency="INR",
        collected_at=datetime(
            2026,
            8,
            28,
            10,
            5,
            tzinfo=UTC,
        ),
    )

    session = MagicMock()

    session.get.side_effect = lambda model, object_id: {
        172: product,
        115: seller_one,
        116: seller_two,
    }.get(object_id)

    listing_query = MagicMock()
    listing_query.filter.return_value.all.return_value = [
        listing_one,
        listing_two,
    ]

    history_query_one = MagicMock()
    history_query_one.filter.return_value.order_by.return_value.all.return_value = [
        history_one,
    ]

    history_query_two = MagicMock()
    history_query_two.filter.return_value.order_by.return_value.all.return_value = [
        history_two,
    ]

    session.query.side_effect = [
        listing_query,
        history_query_one,
        history_query_two,
    ]

    def override_get_session():
        """Provide the fake database session."""
        yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        response = client.get(
            "/analytics/products/172/history",
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == 172
    assert data["product_name"] == "apple iphone 15 128gb"
    assert data["observation_count"] == 2

    assert data["history"][0]["seller_name"] == "demo electronics"
    assert data["history"][0]["price"] == "61999.00"
    assert data["history"][0]["currency"] == "INR"

    assert data["history"][1]["seller_name"] == "demo marketplace"
    assert data["history"][1]["price"] == "59999.00"
    assert data["history"][1]["currency"] == "INR"


def test_product_price_history_product_not_found() -> None:
    """Product history should return 404 for an unknown product."""
    session = MagicMock()
    session.get.return_value = None

    def override_get_session():
        """Provide the fake database session."""
        yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        response = client.get(
            "/analytics/products/999/history",
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found.",
    }