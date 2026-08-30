"""Environment-driven configuration, validated once at startup."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Identity
    gcp_project: str = ""
    service_name: str = "exposure-receiver"
    environment: str = "local"

    # Server
    port: int = 8080
    log_level: str = "INFO"

    # Request admission
    max_body_bytes: int = 64_000


@lru_cache
def get_settings() -> Settings:
    """Cached so the whole app shares one instance; override in tests."""
    return Settings()
