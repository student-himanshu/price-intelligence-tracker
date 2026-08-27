"""Tests for the demo collector."""

from price_tracker.collectors.demo import DemoCollector


def test_demo_collector_returns_three_records() -> None:
    """Demo collector should return three deterministic records."""
    collector = DemoCollector()

    records = collector.collect()

    assert len(records) == 3


def test_demo_collector_contains_required_fields() -> None:
    """Each demo record should contain all required collection fields."""
    collector = DemoCollector()

    records = collector.collect()

    required_fields = {
        "brand",
        "model",
        "name",
        "category",
        "seller_name",
        "seller_domain",
        "external_product_id",
        "url",
        "price",
        "original_price",
        "currency",
        "availability",
    }

    for record in records:
        assert required_fields.issubset(record.keys())


def test_demo_collector_contains_valid_price_data() -> None:
    """Demo records should contain positive price values."""
    collector = DemoCollector()

    records = collector.collect()

    for record in records:
        assert record["price"] > 0
        assert record["original_price"] > 0
        assert record["currency"] == "INR"


def test_demo_collector_contains_listing_data() -> None:
    """Demo records should contain seller and listing information."""
    collector = DemoCollector()

    records = collector.collect()

    for record in records:
        assert record["seller_name"]
        assert record["seller_domain"]
        assert record["external_product_id"]
        assert record["url"]
        assert record["availability"] is True


def test_demo_collector_is_deterministic() -> None:
    """Demo collector should return the same data on every call."""
    collector = DemoCollector()

    first_result = collector.collect()
    second_result = collector.collect()

    assert first_result == second_result