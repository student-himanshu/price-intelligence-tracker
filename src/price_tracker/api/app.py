"""FastAPI application factory."""

from fastapi import FastAPI

from price_tracker.api.routes import (
    analytics_router,
    forecast_router,
    health_router,
    listings_router,
    prices_router,
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

    app.include_router(health_router)
    app.include_router(products_router)
    app.include_router(sellers_router)
    app.include_router(listings_router)
    app.include_router(prices_router)
    app.include_router(analytics_router)
    app.include_router(forecast_router)

    return app


app = create_app()