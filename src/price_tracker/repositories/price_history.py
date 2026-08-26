"""Price history repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from price_tracker.models import PriceHistory


class PriceHistoryRepository:
    """Data-access operations for price history."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, price_history_id: int) -> PriceHistory | None:
        """Return a price history record by ID."""
        statement = select(PriceHistory).where(
            PriceHistory.id == price_history_id,
        )

        return self.session.scalar(statement)

    def add(self, price_history: PriceHistory) -> PriceHistory:
        """Add a price history record and flush the session."""
        self.session.add(price_history)
        self.session.flush()

        return price_history

    def get_latest(self, listing_id: int) -> PriceHistory | None:
        """Return the latest price observation for a listing."""
        statement = (
            select(PriceHistory)
            .where(PriceHistory.listing_id == listing_id)
            .order_by(PriceHistory.collected_at.desc())
            .limit(1)
        )

        return self.session.scalar(statement)

    def list_by_listing(self, listing_id: int) -> list[PriceHistory]:
        """Return all price observations for a listing."""
        statement = (
            select(PriceHistory)
            .where(PriceHistory.listing_id == listing_id)
            .order_by(PriceHistory.collected_at.desc())
        )

        return list(self.session.scalars(statement).all())