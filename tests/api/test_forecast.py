"""Tests for the price forecasting API."""

from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from price_tracker.api.app import app
from price_tracker.database.session import get_session

client = TestClient(app)


def test_forecast_product_price() -> None:
    """Forecast endpoint should return the next predicted price."""
    product = MagicMock(
        id=172,
        normalized_name="apple iphone 15 128gb",
    )

    listing = MagicMock(
        id=172,
        product_id=172,
    )

    history_one = MagicMock(
        listing_id=172,
        price=Decimal("61999.00"),
        currency="INR",
        collected_at=datetime(
            2026,
            8,
            27,
            10,
            0,
            tzinfo=UTC,
        ),
    )

    history_two = MagicMock(
        listing_id=172,
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

    history_query = MagicMock()
    history_query.filter.return_value.order_by.return_value.all.return_value = [
        history_one,
        history_two,
    ]

    session.query.side_effect = [
        listing_query,
        history_query,
    ]

    def override_get_session():
        """Provide the fake database session."""
        yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        response = client.get("/forecast/172")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == 172
    assert data["product_name"] == "apple iphone 15 128gb"
    assert data["current_price"] == "59999.00"
    assert data["forecast_price"] == "57999.00"
    assert data["price_change"] == "-2000.00"
    assert data["price_change_percentage"] == "-3.2259"
    assert data["trend"] == "decreasing"
    assert data["confidence"] == "medium"
    assert data["currency"] == "INR"
    assert data["history_count"] == 2


def test_forecast_product_price_product_not_found() -> None:
    """Forecast endpoint should return 404 for an unknown product."""
    session = MagicMock()
    session.get.return_value = None

    def override_get_session():
        """Provide the fake database session."""
        yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        response = client.get("/forecast/999")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found.",
    }
    
def test_forecast_product_price_with_insufficient_history() -> None:
    """Forecast should report insufficient data for one observation."""
    product = MagicMock(
        id=172,
        normalized_name="apple iphone 15 128gb",
    )

    listing = MagicMock(
        id=172,
        product_id=172,
    )

    history = MagicMock(
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

    session = MagicMock()
    session.get.return_value = product

    listing_query = MagicMock()
    listing_query.filter.return_value.all.return_value = [listing]

    history_query = MagicMock()
    history_query.filter.return_value.order_by.return_value.all.return_value = [
        history,
    ]

    session.query.side_effect = [
        listing_query,
        history_query,
    ]

    def override_get_session():
        """Provide the fake database session."""
        yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        response = client.get("/forecast/172")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["current_price"] == "61999.00"
    assert data["forecast_price"] is None
    assert data["price_change"] is None
    assert data["price_change_percentage"] is None
    assert data["trend"] == "insufficient_data"
    assert data["confidence"] == "low"
    assert data["currency"] == "INR"
    assert data["history_count"] == 1
    
def test_forecast_product_price_high_confidence() -> None:
    """Forecast should report high confidence with enough history."""
    product = MagicMock(
        id=172,
        normalized_name="apple iphone 15 128gb",
    )

    listing = MagicMock(
        id=172,
        product_id=172,
    )

    history = [
        MagicMock(
            listing_id=172,
            price=Decimal(str(price)),
            currency="INR",
            collected_at=datetime(
                2026,
                8,
                24 + index,
                10,
                0,
                tzinfo=UTC,
            ),
        )
        for index, price in enumerate(
            [61999, 60999, 59999, 58999, 57999],
        )
    ]

    session = MagicMock()
    session.get.return_value = product

    listing_query = MagicMock()
    listing_query.filter.return_value.all.return_value = [listing]

    history_query = MagicMock()
    history_query.filter.return_value.order_by.return_value.all.return_value = (
        history
    )

    session.query.side_effect = [
        listing_query,
        history_query,
    ]

    def override_get_session():
        """Provide the fake database session."""
        yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        response = client.get("/forecast/172")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["confidence"] == "high"
    assert data["history_count"] == 5
    assert data["trend"] == "decreasing"