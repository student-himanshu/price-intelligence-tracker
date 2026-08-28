"""Tests for the AI service."""
import pytest
from pydantic import SecretStr

from price_tracker.ai.config import AISettings
from price_tracker.ai.providers import AIProvider
from price_tracker.ai.service import AIService


class FakeAIProvider(AIProvider):
    """Fake provider for testing."""
    def generate(self, prompt: str) -> str:
        """Return a deterministic test response."""
        return f"Generated response for: {prompt}"
def test_ai_service_generate(monkeypatch) -> None:
    """AI service should delegate generation to its provider."""
    settings = AISettings(
        groq_api_key=SecretStr("test-key"),
        ai_provider="groq",
    )
    monkeypatch.setattr(
        "price_tracker.ai.service.GroqProvider",
        lambda settings: FakeAIProvider(),
    )
    service = AIService(settings)
    result = service.generate("Analyze this product price.")
    assert result == "Generated response for: Analyze this product price."
def test_ai_service_selects_google_provider(monkeypatch) -> None:
    """AI service should select the Google provider when configured."""
    settings = AISettings(
        google_api_key=SecretStr("test-key"),
        ai_provider="google",
    )
    monkeypatch.setattr(
        "price_tracker.ai.service.GoogleProvider",
        lambda settings: FakeAIProvider(),
    )
    service = AIService(settings)
    result = service.generate("Analyze price trend.")
    assert result == "Generated response for: Analyze price trend."
def test_ai_service_accepts_gemini_provider(monkeypatch) -> None:
    """AI service should accept Gemini as an alias for Google."""
    settings = AISettings(
        google_api_key=SecretStr("test-key"),
        ai_provider="gemini",
    )
    monkeypatch.setattr(
        "price_tracker.ai.service.GoogleProvider",
        lambda settings: FakeAIProvider(),
    )
    service = AIService(settings)
    result = service.generate("Analyze price trend.")
    assert result == "Generated response for: Analyze price trend."
def test_ai_service_rejects_unsupported_provider() -> None:
    """AI service should reject unsupported providers."""
    settings = AISettings(
        ai_provider="unsupported",
    )
    with pytest.raises(
        ValueError,
        match="Unsupported AI provider: unsupported",
    ):
        AIService(settings)
