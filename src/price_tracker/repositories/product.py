"""Product repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from price_tracker.models import Product


class ProductRepository:
    """Data-access operations for products."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, product_id: int) -> Product | None:
        """Return a product by ID."""
        statement = select(Product).where(Product.id == product_id)

        return self.session.scalar(statement)