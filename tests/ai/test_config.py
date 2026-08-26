"""Tests for AI configuration."""

from pydantic import SecretStr

from price_tracker.ai.config import AISettings


def test_ai_settings_defaults_to_groq() -> None:
    """AI settings should use Groq by default."""
    settings = AISettings()

    assert settings.ai_provider == "groq"


def test_ai_settings_accepts_google_provider() -> None:
    """AI settings should accept Google as the provider."""
    settings = AISettings(
        google_api_key=SecretStr("test-key"),
        ai_provider="google",
    )

    assert settings.ai_provider == "google"
    assert settings.google_api_key is not None
def test_ai_settings_reads_environment_variables(monkeypatch) -> None:
    """AI settings should read provider credentials from environment."""
    monkeypatch.setenv("AI_PROVIDER", "google")
    monkeypatch.setenv("GOOGLE_API_KEY", "test-google-key")

    settings = AISettings()

    assert settings.ai_provider == "google"
    assert settings.google_api_key is not None
    assert settings.google_api_key.get_secret_value() == "test-google-key"
def test_ai_settings_environment_isolation() -> None:
    """AI settings should use defaults when no environment overrides exist."""
    settings = AISettings()

    assert settings.ai_provider == "groq"