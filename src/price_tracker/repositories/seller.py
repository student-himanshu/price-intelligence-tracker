"""Repository operations for sellers."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from price_tracker.models.seller import Seller


class SellerRepository:
    """Provide database operations for Seller entities."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, seller_id: int) -> Seller | None:
        """Return a seller by its primary key."""
        return self.session.get(Seller, seller_id)

    def get_by_domain(self, domain: str) -> Seller | None:
        """Return a seller by its domain."""
        statement = select(Seller).where(Seller.domain == domain)
        return self.session.scalar(statement)

    def get_by_name(self, seller_name: str) -> Seller | None:
        """Return a seller by its name."""
        statement = select(Seller).where(Seller.seller_name == seller_name)
        return self.session.scalar(statement)

    def list_all(self) -> list[Seller]:
        """Return all sellers ordered by ID."""
        statement = select(Seller).order_by(Seller.id)
        return list(self.session.scalars(statement).all())

    def add(self, seller: Seller) -> Seller:
        """Add a seller to the current transaction."""
        self.session.add(seller)
        self.session.flush()
        return seller