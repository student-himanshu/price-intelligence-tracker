"""Application services for products."""

from sqlalchemy.orm import Session

from price_tracker.models.product import Product
from price_tracker.repositories.product import ProductRepository
from price_tracker.schemas.product import ProductCreate
from price_tracker.validation.product import validate_product


class ProductService:
    """Handle product business operations."""

    def __init__(self, session: Session) -> None:
        self.repository = ProductRepository(session)

    def get_by_id(self, product_id: int) -> Product | None:
        """Return a product by ID."""
        return self.repository.get_by_id(product_id)

    def get_or_create(self, product: ProductCreate) -> Product:
        """Return an existing product or create a new one."""
        validated_product = validate_product(product)

        existing = self.repository.get_by_normalized_name(
            validated_product.normalized_name,
        )

        if existing is not None:
            return existing

        new_product = Product(**validated_product.model_dump())
        return self.repository.add(new_product)