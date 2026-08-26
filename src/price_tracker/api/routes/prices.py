"""Price history API routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("")
def list_prices() -> dict[str, str]:
    """Return a placeholder response for price history."""
    return {
        "message": "Price history endpoint is ready.",
    }