"""AI provider abstractions."""

from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Abstract interface for AI providers."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response from the provider."""
        raise NotImplementedError