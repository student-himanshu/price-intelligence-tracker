"""Application configuration and environment settings."""

from functools import lru_cache

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    """MySQL database configuration."""

    host: str = Field(default="localhost")
    port: int = Field(default=3306, ge=1, le=65535)
    database: str = Field(default="price_intelligence")
    user: str = Field(default="price_tracker")
    password: str = Field(default="change_me")

    @property
    def url(self) -> str:
        """Build the SQLAlchemy database connection URL."""
        return (
            f"mysql+mysqlconnector://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )


class Settings(BaseSettings):
    """Application-wide configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "price-intelligence-tracker"
    app_env: str = "development"
    log_level: str = "INFO"

    mysql_host: str = "localhost"
    mysql_port: int = Field(default=3306, ge=1, le=65535)
    mysql_database: str = "price_intelligence"
    mysql_user: str = "price_tracker"
    mysql_password: str = "change_me"

    api_host: str = "127.0.0.1"
    api_port: int = Field(default=8000, ge=1, le=65535)

    streamlit_host: str = "127.0.0.1"
    streamlit_port: int = Field(default=8501, ge=1, le=65535)

    @property
    def database(self) -> DatabaseSettings:
        """Return database configuration as a dedicated settings object."""
        return DatabaseSettings(
            host=self.mysql_host,
            port=self.mysql_port,
            database=self.mysql_database,
            user=self.mysql_user,
            password=self.mysql_password,
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the cached application settings instance."""
    return Settings()