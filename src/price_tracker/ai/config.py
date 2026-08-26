"""AI provider configuration."""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AISettings(BaseSettings):
    """Configuration for AI providers."""

    groq_api_key: SecretStr | None = None
    google_api_key: SecretStr | None = None
    ai_provider: str = "groq"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )