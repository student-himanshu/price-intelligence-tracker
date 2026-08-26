"""Repository operations for price history."""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from price_tracker.models.price_history import PriceHistory


class PriceHistoryRepository:
    """Provide database operations for price history."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, price_history_id: int) -> PriceHistory | None:
        """Return a price history record by its primary key."""
        return self.session.get(PriceHistory, price_history_id)

    def list_by_listing(self, listing_id: int) -> list[PriceHistory]:
        """Return price history for a listing, newest first."""
        statement = (
            select(PriceHistory)
            .where(PriceHistory.listing_id == listing_id)
            .order_by(PriceHistory.collected_at.desc())
        )
        return list(self.session.scalars(statement).all())

    def list_between(
        self,
        listing_id: int,
        start: datetime,
        end: datetime,
    ) -> list[PriceHistory]:
        """Return price observations within a time range."""
        statement = (
            select(PriceHistory)
            .where(
                PriceHistory.listing_id == listing_id,
                PriceHistory.collected_at >= start,
                PriceHistory.collected_at <= end,
            )
            .order_by(PriceHistory.collected_at.asc())
        )
        return list(self.session.scalars(statement).all())

    def get_latest(self, listing_id: int) -> PriceHistory | None:
        """Return the latest price observation for a listing."""
        statement = (
            select(PriceHistory)
            .where(PriceHistory.listing_id == listing_id)
            .order_by(PriceHistory.collected_at.desc())
            .limit(1)
        )
        return self.session.scalar(statement)

    def add(self, price_history: PriceHistory) -> PriceHistory:
        """Add a price history record to the current transaction."""
        self.session.add(price_history)
        self.session.flush()
        return price_history