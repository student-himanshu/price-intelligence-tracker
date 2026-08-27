"""Tests for the collector pipeline."""

from unittest.mock import MagicMock

from price_tracker.pipeline.collector_pipeline import CollectorPipeline


def test_collector_pipeline_collects_records() -> None:
    """Pipeline should call the collector and return its records."""
    collector = MagicMock()
    collector.collect.return_value = [
        {
            "name": "Apple iPhone 15 128GB",
            "seller_name": "Demo Electronics",
            "seller_domain": "demo-electronics.example",
        }
    ]

    pipeline = CollectorPipeline(collector)

    result = pipeline.run()

    collector.collect.assert_called_once()
    assert len(result) == 1


def test_collector_pipeline_normalizes_product_name() -> None:
    """Pipeline should normalize the product name."""
    collector = MagicMock()
    collector.collect.return_value = [
        {
            "name": "  Apple   iPhone 15 128GB  ",
            "seller_name": "Demo Electronics",
            "seller_domain": "demo-electronics.example",
        }
    ]

    pipeline = CollectorPipeline(collector)

    result = pipeline.run()

    assert result[0]["name"] == "apple iphone 15 128gb"


def test_collector_pipeline_normalizes_seller_name() -> None:
    """Pipeline should normalize the seller name."""
    collector = MagicMock()
    collector.collect.return_value = [
        {
            "name": "Apple iPhone 15",
            "seller_name": "  DEMO   Electronics  ",
            "seller_domain": "demo-electronics.example",
        }
    ]

    pipeline = CollectorPipeline(collector)

    result = pipeline.run()

    assert result[0]["seller_name"] == "demo electronics"


def test_collector_pipeline_normalizes_seller_domain() -> None:
    """Pipeline should normalize the seller domain."""
    collector = MagicMock()
    collector.collect.return_value = [
        {
            "name": "Apple iPhone 15",
            "seller_name": "Demo Electronics",
            "seller_domain": "HTTPS://Demo-Electronics.Example/",
        }
    ]

    pipeline = CollectorPipeline(collector)

    result = pipeline.run()

    assert result[0]["seller_domain"] == "demo-electronics.example"


def test_collector_pipeline_preserves_original_fields() -> None:
    """Pipeline should preserve fields other than normalized fields."""
    collector = MagicMock()
    collector.collect.return_value = [
        {
            "brand": "Apple",
            "model": "iPhone 15",
            "name": "Apple iPhone 15",
            "category": "Smartphone",
            "seller_name": "Demo Electronics",
            "seller_domain": "demo-electronics.example",
            "external_product_id": "IPHONE15-128-BLK",
            "url": "https://example.com/product",
            "price": 61999.00,
            "original_price": 69999.00,
            "currency": "INR",
            "availability": True,
        }
    ]

    pipeline = CollectorPipeline(collector)

    result = pipeline.run()

    assert result[0]["brand"] == "Apple"
    assert result[0]["model"] == "iPhone 15"
    assert result[0]["category"] == "Smartphone"
    assert result[0]["external_product_id"] == "IPHONE15-128-BLK"
    assert result[0]["url"] == "https://example.com/product"
    assert result[0]["price"] == 61999.00
    assert result[0]["original_price"] == 69999.00
    assert result[0]["currency"] == "INR"
    assert result[0]["availability"] is True