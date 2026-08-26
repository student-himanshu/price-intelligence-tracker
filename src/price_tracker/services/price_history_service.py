"""Application services for price history."""

from sqlalchemy.orm import Session

from price_tracker.models.price_history import PriceHistory
from price_tracker.repositories.price_history import PriceHistoryRepository
from price_tracker.schemas.price_history import PriceHistoryCreate
from price_tracker.validation.price_history import validate_price_history


class PriceHistoryService:
    """Handle price history business operations."""

    def __init__(self, session: Session) -> None:
        self.repository = PriceHistoryRepository(session)

    def get_by_id(self, price_history_id: int) -> PriceHistory | None:
        """Return a price history record by ID."""
        return self.repository.get_by_id(price_history_id)

    def record(self, price_history: PriceHistoryCreate) -> PriceHistory:
        """Validate and record a new price observation."""
        validated_price = validate_price_history(price_history)

        new_record = PriceHistory(**validated_price.model_dump())
        return self.repository.add(new_record)

    def get_latest(self, listing_id: int) -> PriceHistory | None:
        """Return the latest price observation for a listing."""
        return self.repository.get_latest(listing_id)

    def list_by_listing(self, listing_id: int) -> list[PriceHistory]:
        """Return all price observations for a listing."""
        return self.repository.list_by_listing(listing_id)