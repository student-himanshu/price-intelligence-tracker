"""Repository operations for products."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from price_tracker.models.product import Product


class ProductRepository:
    """Provide database operations for Product entities."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, product_id: int) -> Product | None:
        """Return a product by its primary key."""
        return self.session.get(Product, product_id)

    def get_by_normalized_name(self, normalized_name: str) -> Product | None:
        """Return a product by its normalized name."""
        statement = select(Product).where(
            Product.normalized_name == normalized_name,
        )
        return self.session.scalar(statement)

    def list_all(self) -> list[Product]:
        """Return all products ordered by ID."""
        statement = select(Product).order_by(Product.id)
        return list(self.session.scalars(statement).all())

    def add(self, product: Product) -> Product:
        """Add a product to the current transaction."""
        self.session.add(product)
        self.session.flush()
        return product