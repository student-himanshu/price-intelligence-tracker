"""Demo marketplace HTML collector adapter."""
from price_tracker.collectors.web.adapters.base import MarketplaceHtmlCollector


class DemoMarketplaceCollector(MarketplaceHtmlCollector):
    """Collect products from the demo marketplace HTML structure."""
    name_selector = ".product-title"
    price_selector = ".product-price"
    seller_selector = ".seller-name"
