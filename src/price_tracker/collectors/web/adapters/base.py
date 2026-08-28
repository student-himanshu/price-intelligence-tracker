"""Marketplace-specific HTML collector adapters."""
from typing import Any

from price_tracker.collectors.web.html_product import HtmlProductCollector
from price_tracker.collectors.web.http import HttpCollector


class MarketplaceHtmlCollector(HtmlProductCollector):
    """Base collector for marketplace-specific HTML selectors."""
    name_selector: str = "[data-product-name]"
    price_selector: str = "[data-product-price]"
    seller_selector: str = "[data-product-seller]"
    def __init__(
        self,
        url: str,
        http_client: HttpCollector | None = None,
    ) -> None:
        super().__init__(
            url=url,
            http_client=http_client,
            name_selector=self.name_selector,
            price_selector=self.price_selector,
            seller_selector=self.seller_selector,
        )
    def collect(self) -> list[dict[str, Any]]:
        """Collect product data using marketplace selectors."""
        return super().collect()
