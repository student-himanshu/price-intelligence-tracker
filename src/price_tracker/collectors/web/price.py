"""Price parsing utilities for web collectors."""
import re
from decimal import Decimal, InvalidOperation


def parse_price(value: str) -> Decimal:
    """Convert a formatted price string into a positive Decimal."""
    if "-" in value:
        raise ValueError("Price must not be negative.")
    cleaned = re.sub(r"[^\d.,]", "", value).strip()
    if not cleaned:
        raise ValueError("Price does not contain a numeric value.")
    if "," in cleaned and "." in cleaned:
        if cleaned.rfind(",") > cleaned.rfind("."):
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        parts = cleaned.split(",")
        if len(parts[-1]) == 2:
            cleaned = "".join(parts[:-1]) + "." + parts[-1]
        else:
            cleaned = cleaned.replace(",", "")
    try:
        price = Decimal(cleaned)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid price: {value}") from exc
    if price <= 0:
        raise ValueError("Price must be greater than zero.")
    return price
