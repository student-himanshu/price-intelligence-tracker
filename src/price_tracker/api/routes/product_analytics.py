"""Product-level price comparison API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from price_tracker.database.session import get_session
from price_tracker.models import Listing, PriceHistory, Product, Seller

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)


@router.get("/products/{product_id}/comparison")
def get_product_price_comparison(
    product_id: int,
    session: Session = Depends(get_session),
) -> dict[str, object]:
    """Return the latest price for every seller listing of a product."""
    product = session.get(Product, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )

    listings = (
        session.query(Listing)
        .filter(Listing.product_id == product_id)
        .all()
    )

    comparisons: list[dict[str, object]] = []

    for listing in listings:
        latest_price = (
            session.query(PriceHistory)
            .filter(PriceHistory.listing_id == listing.id)
            .order_by(PriceHistory.collected_at.desc())
            .first()
        )

        if latest_price is None:
            continue

        seller = session.get(Seller, listing.seller_id)

        comparisons.append(
            {
                "listing_id": listing.id,
                "seller_id": listing.seller_id,
                "seller_name": (
                    seller.seller_name
                    if seller
                    else None
                ),
                "price": latest_price.price,
                "currency": latest_price.currency,
                "availability": listing.availability,
            },
        )

    comparisons.sort(
        key=lambda item: item["price"],
    )

    best_deal = None

    for comparison in comparisons:
        if comparison["availability"]:
            best_deal = comparison
            break

    savings = None

    if best_deal is not None and comparisons:
        highest_price = comparisons[-1]["price"]
        savings = highest_price - best_deal["price"]

    return {
        "product_id": product.id,
        "product_name": product.normalized_name,
        "lowest_price": (
            comparisons[0]["price"]
            if comparisons
            else None
        ),
        "seller_count": len(comparisons),
        "best_deal": best_deal,
        "savings_vs_highest_price": savings,
        "listings": comparisons,
    }