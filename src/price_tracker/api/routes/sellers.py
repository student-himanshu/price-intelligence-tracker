"""Seller API routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/sellers", tags=["Sellers"])


@router.get("")
def list_sellers() -> dict[str, str]:
    """Return a placeholder response for seller listing."""
    return {
        "message": "Seller listing endpoint is ready.",
    }