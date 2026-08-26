"""Seller repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from price_tracker.models import Seller


class SellerRepository:
    """Data-access operations for sellers."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, seller_id: int) -> Seller | None:
        """Return a seller by ID."""
        statement = select(Seller).where(Seller.id == seller_id)

        return self.session.scalar(statement)