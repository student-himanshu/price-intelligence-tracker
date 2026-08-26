"""Tests for product services."""

from unittest.mock import MagicMock

from price_tracker.models import Product
from price_tracker.schemas.product import ProductCreate
from price_tracker.services.product_service import ProductService


def test_get_by_id_delegates_to_repository() -> None:
    """Product service should delegate ID lookup to the repository."""
    session = MagicMock()
    product = Product(
        id=1,
        normalized_name="iphone 15 128gb",
    )

    repository = MagicMock()
    repository.get_by_id.return_value = product

    service = ProductService(session)
    service.repository = repository

    result = service.get_by_id(1)

    assert result is product
    repository.get_by_id.assert_called_once_with(1)


def test_get_or_create_returns_existing_product() -> None:
    """Service should return an existing product without creating another."""
    session = MagicMock()

    existing_product = Product(
        id=1,
        normalized_name="iphone 15 128gb",
    )

    repository = MagicMock()
    repository.get_by_normalized_name.return_value = existing_product

    service = ProductService(session)
    service.repository = repository

    product_data = ProductCreate(
        brand="Apple",
        model="iPhone 15",
        normalized_name="iphone 15 128gb",
        category="smartphone",
    )

    result = service.get_or_create(product_data)

    assert result is existing_product
    repository.get_by_normalized_name.assert_called_once_with(
        "iphone 15 128gb",
    )
    repository.add.assert_not_called()


def test_get_or_create_creates_new_product() -> None:
    """Service should create a product when no existing product is found."""
    session = MagicMock()

    repository = MagicMock()
    repository.get_by_normalized_name.return_value = None

    created_product = Product(
        id=1,
        brand="Apple",
        model="iPhone 15",
        normalized_name="iphone 15 128gb",
        category="smartphone",
    )
    repository.add.return_value = created_product

    service = ProductService(session)
    service.repository = repository

    product_data = ProductCreate(
        brand="Apple",
        model="iPhone 15",
        normalized_name="iphone 15 128gb",
        category="smartphone",
    )

    result = service.get_or_create(product_data)

    assert result is created_product
    repository.get_by_normalized_name.assert_called_once_with(
        "iphone 15 128gb",
    )
    repository.add.assert_called_once()


def test_get_or_create_rejects_invalid_product() -> None:
    """Service should reject invalid product data before repository access."""
    session = MagicMock()
    repository = MagicMock()

    service = ProductService(session)
    service.repository = repository

    invalid_product = ProductCreate(
        brand="Apple",
        model="iPhone 15",
        normalized_name="   ",
        category="smartphone",
    )

    try:
        service.get_or_create(invalid_product)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid product should raise ValueError")

    repository.get_by_normalized_name.assert_not_called()
    repository.add.assert_not_called()