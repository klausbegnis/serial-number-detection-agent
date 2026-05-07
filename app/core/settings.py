from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    environment: str = "local"
    google_api_key: str | None = None


@lru_cache
def get_settings() -> Settings:
    """
    Load environment variables and return cached settings.
    """
    load_dotenv()
    return Settings()
