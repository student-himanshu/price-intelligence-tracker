"""Factory for creating price data collectors."""
from price_tracker.collectors.base import BaseCollector
from price_tracker.collectors.demo import DemoCollector
from price_tracker.collectors.web.adapters.demo_marketplace import (
    DemoMarketplaceCollector,
)


def create_collector(
    collector_type: str,
    url: str | None = None,
) -> BaseCollector:
    """Create a collector from its configured type."""
    if collector_type == "demo":
        return DemoCollector()
    if collector_type == "demo_marketplace":
        if not url:
            raise ValueError(
                "URL is required for demo_marketplace collector.",
            )
        return DemoMarketplaceCollector(url=url)
    raise ValueError(f"Unknown collector type: {collector_type}")
