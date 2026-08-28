"""FastAPI application factory."""

from fastapi import FastAPI

from price_tracker.api.routes import (
    alerts_router,
    analytics_router,
    forecast_router,
    health_router,
    listings_router,
    meta_router,
    price_alerts_router,
    prices_router,
    product_analytics_router,
    products_router,
    sellers_router,
)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Price Intelligence Tracker API",
        version="0.1.0",
        description=(
            "API for collecting, normalizing, analyzing, "
            "and tracking product prices."
        ),
    )

    app.include_router(meta_router)
    app.include_router(health_router)
    app.include_router(products_router)
    app.include_router(sellers_router)
    app.include_router(listings_router)
    app.include_router(prices_router)
    app.include_router(analytics_router)
    app.include_router(product_analytics_router)
    app.include_router(forecast_router)
    app.include_router(alerts_router)
    app.include_router(price_alerts_router)

    return app


app = create_app()