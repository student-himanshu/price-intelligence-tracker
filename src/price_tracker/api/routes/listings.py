"""Listing API routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/listings", tags=["Listings"])


@router.get("")
def list_listings() -> dict[str, str]:
    """Return a placeholder response for listing data."""
    return {
        "message": "Listing endpoint is ready.",
    }