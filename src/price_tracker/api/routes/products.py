"""Product API routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("")
def list_products() -> dict[str, str]:
    """Return a placeholder response for product listing."""
    return {
        "message": "Product listing endpoint is ready.",
    }