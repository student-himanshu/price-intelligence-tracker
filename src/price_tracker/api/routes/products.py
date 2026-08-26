"""Product API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from price_tracker.api.dependencies import get_db
from price_tracker.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
) -> dict[str, object]:
    """Return a product by ID."""
    service = ProductService(db)
    product = service.get_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )

    return {
        "id": product.id,
        "brand": product.brand,
        "model": product.model,
        "normalized_name": product.normalized_name,
        "category": product.category,
    }