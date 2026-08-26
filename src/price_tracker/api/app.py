"""FastAPI application factory."""

from fastapi import FastAPI


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

    return app


app = create_app()