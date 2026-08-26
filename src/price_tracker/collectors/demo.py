"""Deterministic demo price collector."""

from typing import Any

from price_tracker.collectors.base import BaseCollector


class DemoCollector(BaseCollector):
    """Return deterministic sample product listings."""

    def collect(self) -> list[dict[str, Any]]:
        """Return a fixed set of sample price observations."""
        return [
            {
                "brand": "Apple",
                "model": "iPhone 15",
                "name": "Apple iPhone 15 128GB",
                "category": "Smartphone",
                "seller_name": "Demo Electronics",
                "seller_domain": "demo-electronics.example",
                "external_product_id": "IPHONE15-128-BLK",
                "url": "https://demo-electronics.example/products/iphone-15-128gb",
                "price": 61999.00,
                "original_price": 69999.00,
                "currency": "INR",
                "availability": True,
            },
            {
                "brand": "Samsung",
                "model": "Galaxy S24",
                "name": "Samsung Galaxy S24 256GB",
                "category": "Smartphone",
                "seller_name": "Demo Electronics",
                "seller_domain": "demo-electronics.example",
                "external_product_id": "S24-256-BLK",
                "url": "https://demo-electronics.example/products/galaxy-s24-256gb",
                "price": 67999.00,
                "original_price": 79999.00,
                "currency": "INR",
                "availability": True,
            },
            {
                "brand": "OnePlus",
                "model": "12",
                "name": "OnePlus 12 256GB",
                "category": "Smartphone",
                "seller_name": "Demo Marketplace",
                "seller_domain": "demo-marketplace.example",
                "external_product_id": "OP12-256-GRN",
                "url": "https://demo-marketplace.example/products/oneplus-12-256gb",
                "price": 54999.00,
                "original_price": 64999.00,
                "currency": "INR",
                "availability": True,
            },
        ]