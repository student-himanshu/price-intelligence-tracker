"""Tests for product comparison with multiple sellers."""

from decimal import Decimal
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from price_tracker.api.app import app
from price_tracker.database.session import get_session

client = TestClient(app)


def test_product_price_comparison_orders_by_lowest_price() -> None:
    """Product comparison should order available listings by price."""
    product = MagicMock(
        id=172,
        normalized_name="apple iphone 15 128gb",
    )

    listing_one = MagicMock(
        id=172,
        product_id=172,
        seller_id=115,
        availability=True,
    )

    listing_two = MagicMock(
        id=175,
        product_id=172,
        seller_id=116,
        availability=True,
    )

    price_one = MagicMock(
        listing_id=172,
        price=Decimal("61999.00"),
        currency="INR",
    )

    price_two = MagicMock(
        listing_id=175,
        price=Decimal("59999.00"),
        currency="INR",
    )

    seller_one = MagicMock(
        seller_name="Demo Electronics",
    )

    seller_two = MagicMock(
        seller_name="Demo Marketplace",
    )

    session = MagicMock()

    def fake_get(model, object_id):
        """Return fake ORM objects."""
        model_name = model.__name__

        if model_name == "Product" and object_id == 172:
            return product

        if model_name == "Seller" and object_id == 115:
            return seller_one

        if model_name == "Seller" and object_id == 116:
            return seller_two

        return None

    session.get.side_effect = fake_get

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
            "/analytics/products/172/comparison",
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == 172
    assert data["seller_count"] == 2
    assert data["lowest_price"] == "59999.00"

    assert data["listings"][0]["seller_name"] == "Demo Marketplace"
    assert data["listings"][0]["price"] == "59999.00"

    assert data["listings"][1]["seller_name"] == "Demo Electronics"
    assert data["listings"][1]["price"] == "61999.00"