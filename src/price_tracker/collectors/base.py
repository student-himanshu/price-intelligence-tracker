"""Base interface for price data collectors."""

from abc import ABC, abstractmethod
from typing import Any


class BaseCollector(ABC):
    """Abstract interface for all price data collectors."""

    @abstractmethod
    def collect(self) -> list[dict[str, Any]]:
        """Collect and return raw product listing data."""
        raise NotImplementedError