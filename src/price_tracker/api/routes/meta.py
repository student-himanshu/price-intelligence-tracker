"""API metadata routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/meta", tags=["Meta"])


@router.get("")
def get_api_metadata() -> dict[str, str]:
    """Return basic API metadata."""
    return {
        "name": "Price Intelligence Tracker API",
        "version": "0.1.0",
        "status": "ready",
    }