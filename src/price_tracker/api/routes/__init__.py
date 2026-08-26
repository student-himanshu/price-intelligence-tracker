"""API route modules."""

from price_tracker.api.routes.health import router as health_router
from price_tracker.api.routes.listings import router as listings_router
from price_tracker.api.routes.prices import router as prices_router
from price_tracker.api.routes.products import router as products_router
from price_tracker.api.routes.sellers import router as sellers_router

__all__ = [
    "health_router",
    "listings_router",
    "prices_router",
    "products_router",
    "sellers_router",
]