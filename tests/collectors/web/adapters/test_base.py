"""Tests for marketplace HTML collector adapters."""
from unittest.mock import MagicMock

from price_tracker.collectors.web.adapters.base import MarketplaceHtmlCollector


def test_marketplace_html_collector_uses_default_selectors() -> None:
    """Marketplace adapter should use the shared HTML collector."""
    http_client = MagicMock()
    http_client.get.return_value = """
    <html>
        <body>
            <h1 data-product-name>Apple iPhone 15</h1>
            <span data-product-price>₹61,999</span>
            <span data-product-seller>Demo Electronics</span>
        </body>
    </html>
    """
    collector = MarketplaceHtmlCollector(
        url="https://example.com/iphone-15",
        http_client=http_client,
    )
    result = collector.collect()
    assert len(result) == 1
    assert result[0]["name"] == "Apple iPhone 15"
    assert result[0]["price"] == 61999
    assert result[0]["seller_name"] == "Demo Electronics"
    assert result[0]["seller_domain"] == "example.com"
