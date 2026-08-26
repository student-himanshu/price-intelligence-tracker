"""Tests for seller services."""

from unittest.mock import MagicMock

from price_tracker.models import Seller
from price_tracker.schemas.seller import SellerCreate
from price_tracker.services.seller_service import SellerService


def test_get_by_id_delegates_to_repository() -> None:
    """Seller service should delegate ID lookup to the repository."""
    session = MagicMock()
    seller = Seller(
        id=1,
        seller_name="Amazon",
        domain="amazon.in",
    )

    repository = MagicMock()
    repository.get_by_id.return_value = seller

    service = SellerService(session)
    service.repository = repository

    result = service.get_by_id(1)

    assert result is seller
    repository.get_by_id.assert_called_once_with(1)


def test_get_or_create_returns_existing_seller() -> None:
    """Service should return an existing seller without creating another."""
    session = MagicMock()

    existing_seller = Seller(
        id=1,
        seller_name="Amazon",
        domain="amazon.in",
    )

    repository = MagicMock()
    repository.get_by_name.return_value = existing_seller

    service = SellerService(session)
    service.repository = repository

    seller_data = SellerCreate(
        seller_name="Amazon",
        domain="amazon.in",
    )

    result = service.get_or_create(seller_data)

    assert result is existing_seller
    repository.get_by_name.assert_called_once_with("Amazon")
    repository.add.assert_not_called()


def test_get_or_create_creates_new_seller() -> None:
    """Service should create a seller when none exists."""
    session = MagicMock()

    repository = MagicMock()
    repository.get_by_name.return_value = None

    created_seller = Seller(
        id=1,
        seller_name="Amazon",
        domain="amazon.in",
    )
    repository.add.return_value = created_seller

    service = SellerService(session)
    service.repository = repository

    seller_data = SellerCreate(
        seller_name="Amazon",
        domain="amazon.in",
    )

    result = service.get_or_create(seller_data)

    assert result is created_seller
    repository.get_by_name.assert_called_once_with("Amazon")
    repository.add.assert_called_once()

def test_get_or_create_rejects_invalid_seller() -> None:
    """Service should reject invalid seller data before repository access."""
    session = MagicMock()
    repository = MagicMock()

    service = SellerService(session)
    service.repository = repository

    invalid_seller = SellerCreate(
        seller_name="   ",
        domain="amazon.in",
    )

    try:
        service.get_or_create(invalid_seller)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid seller should raise ValueError")

    repository.get_by_name.assert_not_called()
    repository.add.assert_not_called()