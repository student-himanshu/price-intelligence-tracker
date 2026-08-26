"""Analytics API routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
def analytics_summary() -> dict[str, str]:
    """Return a placeholder analytics summary."""
    return {
        "message": "Analytics summary endpoint is ready.",
    }