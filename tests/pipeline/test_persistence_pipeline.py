"""Tests for the persistence pipeline."""

from unittest.mock import MagicMock

from price_tracker.pipeline.persistence_pipeline import PersistencePipeline


def create_pipeline() -> tuple[PersistencePipeline, MagicMock, MagicMock, MagicMock, MagicMock]:
    """Create a pipeline with mocked persistence services."""
    session = MagicMock()
    pipeline = PersistencePipeline(session)

    product_service = MagicMock()
    seller_service = MagicMock()
    listing_service = MagicMock()
    price_history_service = MagicMock()

    pipeline.product_service = product_service
    pipeline.seller_service = seller_service
    pipeline.listing_service = listing_service
    pipeline.price_history_service = price_history_service

    return (
        pipeline,
        product_service,
        seller_service,
        listing_service,
        price_history_service,
    )


def test_persist_returns_processed_record_count() -> None:
    """Pipeline should return the number of successfully processed records."""
    (
        pipeline,
        product_service,
        seller_service,
        listing_service,
        _,
    ) = create_pipeline()

    product_service.get_or_create.return_value = MagicMock(id=1)
    seller_service.get_or_create.return_value = MagicMock(id=2)
    listing_service.get_or_create.return_value = MagicMock(id=3)

    records = [
        {
            "brand": "Apple",
            "model": "iPhone 15",
            "name": "apple iphone 15 128gb",
            "category": "Smartphone",
            "seller_name": "Demo Electronics",
            "seller_domain": "demo-electronics.example",
            "external_product_id": "IPHONE15-128-BLK",
            "url": "https://example.com/iphone-15",
            "price": 61999.00,
            "original_price": 69999.00,
            "currency": "INR",
            "availability": True,
        },
        {
            "brand": "Samsung",
            "model": "Galaxy S24",
            "name": "samsung galaxy s24 256gb",
            "category": "Smartphone",
            "seller_name": "Demo Electronics",
            "seller_domain": "demo-electronics.example",
            "external_product_id": "S24-256-BLK",
            "url": "https://example.com/galaxy-s24",
            "price": 67999.00,
            "original_price": 79999.00,
            "currency": "INR",
            "availability": True,
        },
    ]

    result = pipeline.persist(records)

    assert result == 2


def test_persist_creates_product_seller_listing_and_price() -> None:
    """Pipeline should pass each record through all persistence services."""
    (
        pipeline,
        product_service,
        seller_service,
        listing_service,
        price_history_service,
    ) = create_pipeline()

    product_service.get_or_create.return_value = MagicMock(id=10)
    seller_service.get_or_create.return_value = MagicMock(id=20)
    listing_service.get_or_create.return_value = MagicMock(id=30)

    record = {
        "brand": "Apple",
        "model": "iPhone 15",
        "name": "apple iphone 15 128gb",
        "category": "Smartphone",
        "seller_name": "Demo Electronics",
        "seller_domain": "demo-electronics.example",
        "external_product_id": "IPHONE15-128-BLK",
        "url": "https://example.com/iphone-15",
        "price": 61999.00,
        "original_price": 69999.00,
        "currency": "INR",
        "availability": True,
    }

    result = pipeline.persist([record])

    assert result == 1
    product_service.get_or_create.assert_called_once()
    seller_service.get_or_create.assert_called_once()
    listing_service.get_or_create.assert_called_once()
    price_history_service.record.assert_called_once()


def test_persist_uses_product_and_seller_ids_for_listing() -> None:
    """Listing should use IDs returned by product and seller services."""
    (
        pipeline,
        product_service,
        seller_service,
        listing_service,
        _,
    ) = create_pipeline()

    product_service.get_or_create.return_value = MagicMock(id=101)
    seller_service.get_or_create.return_value = MagicMock(id=202)
    listing_service.get_or_create.return_value = MagicMock(id=303)

    record = {
        "name": "apple iphone 15",
        "seller_name": "Demo Electronics",
        "url": "https://example.com/iphone-15",
        "price": 61999.00,
    }

    pipeline.persist([record])

    listing_call = listing_service.get_or_create.call_args.args[0]

    assert listing_call.product_id == 101
    assert listing_call.seller_id == 202


def test_persist_records_price_using_listing_id() -> None:
    """Price history should use the ID returned by the listing service."""
    (
        pipeline,
        product_service,
        seller_service,
        listing_service,
        price_history_service,
    ) = create_pipeline()

    product_service.get_or_create.return_value = MagicMock(id=1)
    seller_service.get_or_create.return_value = MagicMock(id=2)
    listing_service.get_or_create.return_value = MagicMock(id=3)

    record = {
        "name": "apple iphone 15",
        "seller_name": "Demo Electronics",
        "url": "https://example.com/iphone-15",
        "price": 61999.00,
        "original_price": 69999.00,
        "currency": "INR",
    }

    pipeline.persist([record])

    price_call = price_history_service.record.call_args.args[0]

    assert price_call.listing_id == 3
    assert price_call.price == 61999
    assert price_call.original_price == 69999
    assert price_call.currency == "INR"


def test_persist_uses_default_values_when_optional_fields_missing() -> None:
    """Pipeline should apply defaults for optional collector fields."""
    (
        pipeline,
        product_service,
        seller_service,
        listing_service,
        price_history_service,
    ) = create_pipeline()

    product_service.get_or_create.return_value = MagicMock(id=1)
    seller_service.get_or_create.return_value = MagicMock(id=2)
    listing_service.get_or_create.return_value = MagicMock(id=3)

    record = {
        "name": "apple iphone 15",
        "seller_name": "Demo Electronics",
        "url": "https://example.com/iphone-15",
        "price": 61999.00,
    }

    pipeline.persist([record])

    listing_call = listing_service.get_or_create.call_args.args[0]
    price_call = price_history_service.record.call_args.args[0]

    assert listing_call.availability is True
    assert listing_call.external_product_id is None
    assert price_call.original_price is None
    assert price_call.currency == "INR"