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
            PriceHistory.id == price_history_id
        )

        return self.session.scalar(statement)