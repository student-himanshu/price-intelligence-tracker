"""Tests for the HTML collector with the normalization pipeline."""
from decimal import Decimal
from unittest.mock import MagicMock

from price_tracker.collectors.web.html_product import HtmlProductCollector
from price_tracker.pipeline.collector_pipeline import CollectorPipeline


def test_html_product_collector_works_with_pipeline() -> None:
    """HTML collector output should flow through normalization."""
    http_client = MagicMock()
    http_client.get.return_value = """
    <html>
        <body>
            <div data-product-name="x">
                Apple   iPhone 15   128GB
            </div>
            <div data-product-price="x">₹61,999</div>
            <div data-product-seller="x">
                Demo   Electronics
            </div>
        </body>
    </html>
    """
    collector = HtmlProductCollector(
        url="https://example.com/iphone-15",
        http_client=http_client,
    )
    pipeline = CollectorPipeline(collector)
    result = pipeline.run()
    assert result == [
        {
            "name": "apple iphone 15 128gb",
            "price": Decimal("61999"),
            "seller_name": "demo electronics",
            "seller_domain": "example.com",
            "url": "https://example.com/iphone-15",
        }
    ]
