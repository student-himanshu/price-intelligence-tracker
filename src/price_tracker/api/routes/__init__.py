"""API route modules."""

from price_tracker.api.routes.alerts import router as alerts_router
from price_tracker.api.routes.analytics import router as analytics_router
from price_tracker.api.routes.forecast import router as forecast_router
from price_tracker.api.routes.health import router as health_router
from price_tracker.api.routes.listings import router as listings_router
from price_tracker.api.routes.meta import router as meta_router
from price_tracker.api.routes.price_alerts import (
    router as price_alerts_router,
)
from price_tracker.api.routes.prices import router as prices_router
from price_tracker.api.routes.product_analytics import (
    router as product_analytics_router,
)
from price_tracker.api.routes.products import router as products_router
from price_tracker.api.routes.sellers import router as sellers_router

__all__ = [
    "alerts_router",
    "analytics_router",
    "forecast_router",
    "health_router",
    "listings_router",
    "meta_router",
    "prices_router",
    "product_analytics_router",
    "products_router",
    "sellers_router",
    "price_alerts_router",
]