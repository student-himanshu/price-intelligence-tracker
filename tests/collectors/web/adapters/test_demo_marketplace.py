"""Tests for collector error handling."""
from unittest.mock import MagicMock

import pytest

from price_tracker.collectors.web.adapters.demo_marketplace import (
    DemoMarketplaceCollector,
)


def test_demo_marketplace_propagates_http_errors() -> None:
    """Marketplace collector should propagate HTTP failures."""
    http_client = MagicMock()
    http_client.get.side_effect = RuntimeError("HTTP error")
    collector = DemoMarketplaceCollector(
        url="https://demo.example.com/product",
        http_client=http_client,
    )
    with pytest.raises(RuntimeError, match="HTTP error"):
        collector.collect()
def test_demo_marketplace_returns_empty_for_invalid_html() -> None:
    """Marketplace collector should return no records for incomplete HTML."""
    http_client = MagicMock()
    http_client.get.return_value = """
    <html>
        <body>
            <h1 class="product-title">OnePlus 12</h1>
        </body>
    </html>
    """
    collector = DemoMarketplaceCollector(
        url="https://demo.example.com/product",
        http_client=http_client,
    )
    assert collector.collect() == []
