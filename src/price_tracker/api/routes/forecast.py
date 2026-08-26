"""Price forecasting API routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/forecast", tags=["Forecast"])


@router.get("/{product_id}")
def forecast_product_price(product_id: int) -> dict[str, object]:
    """Return a placeholder price forecast for a product."""
    return {
        "product_id": product_id,
        "message": "Price forecast endpoint is ready.",
    }