"""Tests for price-alert integration in the persistence pipeline."""
from decimal import Decimal
from unittest.mock import MagicMock

from price_tracker.pipeline.persistence_pipeline import PersistencePipeline


def test_persistence_pipeline_deactivates_triggered_alert() -> None:
    """Pipeline should deactivate an alert when price reaches its target."""
    session = MagicMock()
    product = MagicMock(id=262)
    seller = MagicMock(id=10)
    listing = MagicMock(id=194)
    price_history = MagicMock(
        price=Decimal("59999.00"),
    )
    alert = MagicMock(
        product_id=262,
        target_price=Decimal("60000.00"),
        is_active=True,
    )
    pipeline = PersistencePipeline.__new__(PersistencePipeline)
    pipeline.session = session
    pipeline.product_service = MagicMock()
    pipeline.seller_service = MagicMock()
    pipeline.listing_service = MagicMock()
    pipeline.price_history_service = MagicMock()
    pipeline.product_service.get_or_create.return_value = product
    pipeline.seller_service.get_or_create.return_value = seller
    pipeline.listing_service.get_or_create.return_value = listing
    pipeline.price_history_service.record.return_value = price_history
    session.query.return_value.filter.return_value.order_by.return_value.all.return_value = [
        alert,
    ]
    records = [
        {
            "name": "apple iphone 15 128gb",
            "brand": "Apple",
            "model": "iPhone 15",
            "category": "Smartphone",
            "seller_name": "demo electronics",
            "seller_domain": "demo.example.com",
            "url": "https://example.com/iphone",
            "price": "59999.00",
            "currency": "INR",
            "availability": True,
        },
    ]
    processed = pipeline.persist(records)
    assert processed == 1
    assert alert.is_active is False
def test_persistence_pipeline_keeps_untriggered_alert_active() -> None:
    """Pipeline should keep an alert active when target is not reached."""
    session = MagicMock()
    product = MagicMock(id=262)
    seller = MagicMock(id=10)
    listing = MagicMock(id=194)
    price_history = MagicMock(
        price=Decimal("61999.00"),
    )
    alert = MagicMock(
        product_id=262,
        target_price=Decimal("60000.00"),
        is_active=True,
    )
    pipeline = PersistencePipeline.__new__(PersistencePipeline)
    pipeline.session = session
    pipeline.product_service = MagicMock()
    pipeline.seller_service = MagicMock()
    pipeline.listing_service = MagicMock()
    pipeline.price_history_service = MagicMock()
    pipeline.product_service.get_or_create.return_value = product
    pipeline.seller_service.get_or_create.return_value = seller
    pipeline.listing_service.get_or_create.return_value = listing
    pipeline.price_history_service.record.return_value = price_history
    session.query.return_value.filter.return_value.order_by.return_value.all.return_value = [
        alert,
    ]
    records = [
        {
            "name": "apple iphone 15 128gb",
            "brand": "Apple",
            "model": "iPhone 15",
            "category": "Smartphone",
            "seller_name": "demo electronics",
            "seller_domain": "demo.example.com",
            "url": "https://example.com/iphone",
            "price": "61999.00",
            "currency": "INR",
            "availability": True,
        },
    ]
    processed = pipeline.persist(records)
    assert processed == 1
    assert alert.is_active is True
