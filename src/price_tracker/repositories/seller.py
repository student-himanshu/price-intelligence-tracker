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

    def get_by_name(self, seller_name: str) -> Seller | None:
        """Return a seller by name."""
        statement = select(Seller).where(
            Seller.seller_name == seller_name,
        )

        return self.session.scalar(statement)

    def add(self, seller: Seller) -> Seller:
        """Add a seller and flush it to the database session."""
        self.session.add(seller)
        self.session.flush()

        return seller