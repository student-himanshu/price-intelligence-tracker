"""AI service orchestration."""

from price_tracker.ai.config import AISettings
from price_tracker.ai.google_provider import GoogleProvider
from price_tracker.ai.groq_provider import GroqProvider
from price_tracker.ai.providers import AIProvider


class AIService:
    """Provide a unified interface for AI generation."""

    def __init__(self, settings: AISettings | None = None) -> None:
        self.settings = settings or AISettings()
        self.provider = self._create_provider()

    def _create_provider(self) -> AIProvider:
        """Create the configured AI provider."""
        provider = self.settings.ai_provider.lower()

        if provider == "groq":
            return GroqProvider(self.settings)

        if provider in {"google", "gemini"}:
            return GoogleProvider(self.settings)

        raise ValueError(
            f"Unsupported AI provider: {self.settings.ai_provider}"
        )

    def generate(self, prompt: str) -> str:
        """Generate a response using the configured provider."""
        return self.provider.generate(prompt)