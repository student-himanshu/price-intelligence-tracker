"""Tests for the collector factory."""
import pytest

from price_tracker.collectors.demo import DemoCollector
from price_tracker.collectors.factory import create_collector
from price_tracker.collectors.web.adapters.demo_marketplace import (
    DemoMarketplaceCollector,
)


def test_factory_creates_demo_collector() -> None:
    """Factory should create the demo collector."""
    collector = create_collector("demo")
    assert isinstance(collector, DemoCollector)
def test_factory_creates_demo_marketplace_collector() -> None:
    """Factory should create the marketplace collector."""
    collector = create_collector(
        "demo_marketplace",
        url="https://demo.example.com/product",
    )
    assert isinstance(collector, DemoMarketplaceCollector)
def test_factory_requires_url_for_marketplace() -> None:
    """Marketplace collectors should require a URL."""
    with pytest.raises(
        ValueError,
        match="URL is required",
    ):
        create_collector("demo_marketplace")
def test_factory_rejects_unknown_collector() -> None:
    """Factory should reject unsupported collector types."""
    with pytest.raises(
        ValueError,
        match="Unknown collector type",
    ):
        create_collector("unknown")
