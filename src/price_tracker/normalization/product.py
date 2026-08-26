"""Product name normalization utilities."""

import re
import unicodedata


def normalize_product_name(name: str) -> str:
    """Normalize a product name for matching and indexing."""
    if not isinstance(name, str):
        raise TypeError("Product name must be a string.")

    normalized = unicodedata.normalize("NFKC", name)
    normalized = normalized.casefold()
    normalized = re.sub(r"[^\w\s]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized)

    return normalized.strip()