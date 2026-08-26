"""Seller name and domain normalization utilities."""

import re
from urllib.parse import urlparse


def normalize_seller_name(name: str) -> str:
    """Normalize a seller name for consistent matching."""
    if not isinstance(name, str):
        raise TypeError("Seller name must be a string.")

    normalized = name.strip().casefold()
    normalized = re.sub(r"\s+", " ", normalized)

    return normalized


def normalize_domain(domain: str) -> str:
    """Normalize a seller domain or URL to a hostname."""
    if not isinstance(domain, str):
        raise TypeError("Seller domain must be a string.")

    value = domain.strip().casefold()

    if "://" not in value:
        value = f"https://{value}"

    parsed = urlparse(value)
    hostname = parsed.hostname

    if not hostname:
        raise ValueError("Invalid seller domain.")

    return hostname.removeprefix("www.")