"""Tests for price parsing utilities."""
from decimal import Decimal

import pytest

from price_tracker.collectors.web.price import parse_price


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("61999", Decimal("61999")),
        ("₹61,999", Decimal("61999")),
        ("₹ 61,999.00", Decimal("61999.00")),
        ("$1,299.99", Decimal("1299.99")),
        ("€1.299,99", Decimal("1299.99")),
    ],
)
def test_parse_price(value: str, expected: Decimal) -> None:
    """Price parser should convert common formatted prices."""
    assert parse_price(value) == expected
@pytest.mark.parametrize(
    "value",
    [
        "",
        "abc",
        "₹",
        "0",
        "-100",
    ],
)
def test_parse_price_rejects_invalid_values(value: str) -> None:
    """Price parser should reject invalid or non-positive prices."""
    with pytest.raises(ValueError):
        parse_price(value)
