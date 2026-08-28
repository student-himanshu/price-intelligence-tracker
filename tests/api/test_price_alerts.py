"""Tests for persistent price alert API."""

from decimal import Decimal
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from price_tracker.api.app import app
from price_tracker.database.session import get_session

client = TestClient(app)


def test_create_price_alert() -> None:
    """Create endpoint should persist a new price alert."""
    product = MagicMock(
        id=193,
        normalized_name="apple iphone 15 128gb",
    )

    alert = MagicMock(
        id=1,
        product_id=193,
        target_price=Decimal("60000.00"),
        is_active=True,
        created_at="2026-08-28T10:00:00",
    )

    session = MagicMock()
    session.get.return_value = product

    def refresh(instance):
        instance.id = alert.id
        instance.product_id = alert.product_id
        instance.target_price = alert.target_price
        instance.is_active = alert.is_active
        instance.created_at = alert.created_at

    session.refresh.side_effect = refresh

    def override_get_session():
        """Provide the fake database session."""
        yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        response = client.post(
            "/price-alerts/193?target_price=60000",
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["product_id"] == 193
    assert data["target_price"] == "60000.00"
    assert data["is_active"] is True

    session.add.assert_called_once()
    session.commit.assert_called_once()


def test_list_price_alerts() -> None:
    """List endpoint should return alerts for a product."""
    product = MagicMock(
        id=193,
        normalized_name="apple iphone 15 128gb",
    )

    alert_one = MagicMock(
        id=1,
        product_id=193,
        target_price=Decimal("60000.00"),
        is_active=True,
        created_at="2026-08-28T10:00:00",
    )

    alert_two = MagicMock(
        id=2,
        product_id=193,
        target_price=Decimal("55000.00"),
        is_active=False,
        created_at="2026-08-28T11:00:00",
    )

    session = MagicMock()
    session.get.return_value = product

    alert_query = MagicMock()
    alert_query.filter.return_value.order_by.return_value.all.return_value = [
        alert_one,
        alert_two,
    ]

    session.query.return_value = alert_query

    def override_get_session():
        """Provide the fake database session."""
        yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        response = client.get("/price-alerts/193")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[0]["target_price"] == "60000.00"
    assert data[0]["is_active"] is True
    assert data[1]["id"] == 2
    assert data[1]["target_price"] == "55000.00"
    assert data[1]["is_active"] is False


def test_deactivate_price_alert() -> None:
    """Delete endpoint should deactivate an existing alert."""
    alert = MagicMock(
        id=1,
        product_id=193,
        target_price=Decimal("60000.00"),
        is_active=True,
    )

    session = MagicMock()
    session.get.return_value = alert

    def override_get_session():
        """Provide the fake database session."""
        yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        response = client.delete("/price-alerts/1")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["product_id"] == 193
    assert data["target_price"] == "60000.00"
    assert data["is_active"] is False

    session.commit.assert_called_once()


def test_deactivate_price_alert_not_found() -> None:
    """Delete endpoint should return 404 for an unknown alert."""
    session = MagicMock()
    session.get.return_value = None

    def override_get_session():
        """Provide the fake database session."""
        yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        response = client.delete("/price-alerts/999")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Price alert not found.",
    }