"""Service for price history records."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from price_tracker.models import PriceHistory
from price_tracker.schemas.price_history import PriceHistoryCreate


class PriceHistoryService:
    """Manage price history database operations."""
    def __init__(self, session: Session) -> None:
        self.session = session
    def record(self, data: PriceHistoryCreate) -> PriceHistory:
        """Create and return a price history record."""
        price_history = PriceHistory(**data.model_dump())
        self.session.add(price_history)
        self.session.flush()
        return price_history
    def get_by_listing_id(self, listing_id: int) -> list[PriceHistory]:
        """Return price history for a listing ordered by collection time."""
        statement = (
            select(PriceHistory)
            .where(PriceHistory.listing_id == listing_id)
            .order_by(PriceHistory.collected_at.asc())
        )
        return list(self.session.scalars(statement).all())
