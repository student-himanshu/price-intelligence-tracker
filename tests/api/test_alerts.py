"""Tests for price alert API."""

from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from price_tracker.api.app import app
from price_tracker.database.session import get_session

client = TestClient(app)


def test_check_price_alert_triggered() -> None:
    """Alert should trigger when current price reaches target."""
    product = MagicMock(
        id=193,
        normalized_name="apple iphone 15 128gb",
    )

    listing = MagicMock(
        id=194,
        product_id=193,
    )

    price = MagicMock(
        listing_id=194,
        price=Decimal("59999.00"),
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

    session = MagicMock()
    session.get.return_value = product

    listing_query = MagicMock()
    listing_query.filter.return_value.all.return_value = [listing]

    price_query = MagicMock()
    price_query.filter.return_value.order_by.return_value.all.return_value = [
        price
    ]

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
            "/alerts/193?target_price=60000",
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == 193
    assert data["product_name"] == "apple iphone 15 128gb"
    assert data["current_price"] == "59999.00"
    assert data["target_price"] == "60000"
    assert data["price_difference"] == "1.00"
    assert data["triggered"] is True
    assert data["currency"] == "INR"


def test_check_price_alert_not_triggered() -> None:
    """Alert should not trigger when current price is above target."""
    product = MagicMock(
        id=193,
        normalized_name="apple iphone 15 128gb",
    )

    listing = MagicMock(
        id=194,
        product_id=193,
    )

    price = MagicMock(
        listing_id=194,
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

    session = MagicMock()
    session.get.return_value = product

    listing_query = MagicMock()
    listing_query.filter.return_value.all.return_value = [listing]

    price_query = MagicMock()
    price_query.filter.return_value.order_by.return_value.all.return_value = [
        price
    ]

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
            "/alerts/193?target_price=60000",
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["current_price"] == "61999.00"
    assert data["target_price"] == "60000"
    assert data["price_difference"] == "-1999.00"
    assert data["triggered"] is False


def test_check_price_alert_product_not_found() -> None:
    """Alert endpoint should return 404 for an unknown product."""
    session = MagicMock()
    session.get.return_value = None

    def override_get_session():
        """Provide the fake database session."""
        yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        response = client.get(
            "/alerts/999?target_price=60000",
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found.",
    }