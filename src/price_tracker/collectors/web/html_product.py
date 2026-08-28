"""Generic HTML product collector."""
from typing import Any
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from price_tracker.collectors.base import BaseCollector
from price_tracker.collectors.web.http import HttpCollector
from price_tracker.collectors.web.price import parse_price


class HtmlProductCollector(BaseCollector):
    """Collect product data from configurable HTML selectors."""
    def __init__(
        self,
        url: str,
        http_client: HttpCollector | None = None,
        name_selector: str = "[data-product-name]",
        price_selector: str = "[data-product-price]",
        seller_selector: str = "[data-product-seller]",
    ) -> None:
        self.url = url
        self.http_client = http_client or HttpCollector()
        self.name_selector = name_selector
        self.price_selector = price_selector
        self.seller_selector = seller_selector
    def collect(self) -> list[dict[str, Any]]:
        """Fetch the page and extract a single product listing."""
        html = self.http_client.get(self.url)
        soup = BeautifulSoup(html, "html.parser")
        name_element = soup.select_one(self.name_selector)
        price_element = soup.select_one(self.price_selector)
        seller_element = soup.select_one(self.seller_selector)
        if not name_element or not price_element or not seller_element:
            return []
        parsed_url = urlparse(self.url)
        seller_domain = parsed_url.netloc.lower()
        price = parse_price(price_element.get_text(strip=True))
        return [
            {
                "name": name_element.get_text(" ", strip=True),
                "price": price,
                "seller_name": seller_element.get_text(" ", strip=True),
                "seller_domain": seller_domain,
                "url": self.url,
            }
        ]
