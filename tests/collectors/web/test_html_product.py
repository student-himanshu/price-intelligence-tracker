"""Tests for the HTML collector with price parsing."""
from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from price_tracker.collectors.web.html_product import HtmlProductCollector


def test_html_product_collector_extracts_product() -> None:
    """Collector should extract and parse product fields."""
    http_client = MagicMock()
    http_client.get.return_value = """
    <html>
        <body>
            <div data-product-name>Apple iPhone 15</div>
            <div data-product-price>₹61,999</div>
            <div data-product-seller>Demo Electronics</div>
        </body>
    </html>
    """
    collector = HtmlProductCollector(
        url="https://example.com/iphone-15",
        http_client=http_client,
    )
    result = collector.collect()
    assert result == [
        {
            "name": "Apple iPhone 15",
            "price": Decimal("61999"),
            "seller_name": "Demo Electronics",
            "seller_domain": "example.com",
            "url": "https://example.com/iphone-15",
        }
    ]
def test_html_product_collector_supports_custom_selectors() -> None:
    """Collector should support website-specific CSS selectors."""
    http_client = MagicMock()
    http_client.get.return_value = """
    <html>
        <body>
            <h1 class="product-title">Samsung Galaxy S24</h1>
            <span class="current-price">₹67,999</span>
            <span class="store-name">Demo Store</span>
        </body>
    </html>
    """
    collector = HtmlProductCollector(
        url="https://store.example.com/s24",
        http_client=http_client,
        name_selector=".product-title",
        price_selector=".current-price",
        seller_selector=".store-name",
    )
    result = collector.collect()
    assert result[0]["name"] == "Samsung Galaxy S24"
    assert result[0]["price"] == Decimal("67999")
    assert result[0]["seller_name"] == "Demo Store"
    assert result[0]["seller_domain"] == "store.example.com"
def test_html_product_collector_returns_empty_when_fields_missing() -> None:
    """Collector should return no records when required fields are missing."""
    http_client = MagicMock()
    http_client.get.return_value = """
    <html>
        <body>
            <div data-product-name>Apple iPhone 15</div>
        </body>
    </html>
    """
    collector = HtmlProductCollector(
        url="https://example.com/iphone-15",
        http_client=http_client,
    )
    assert collector.collect() == []
def test_html_product_collector_rejects_invalid_price() -> None:
    """Collector should reject invalid product prices."""
    http_client = MagicMock()
    http_client.get.return_value = """
    <html>
        <body>
            <div data-product-name>Apple iPhone 15</div>
            <div data-product-price>-100</div>
            <div data-product-seller>Demo Electronics</div>
        </body>
    </html>
    """
    collector = HtmlProductCollector(
        url="https://example.com/iphone-15",
        http_client=http_client,
    )
    with pytest.raises(ValueError, match="negative"):
        collector.collect()
