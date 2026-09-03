"""Environment-driven configuration, validated once at startup."""

from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Identity
    gcp_project: str 
    service_name: str = "exposure-receiver"
    environment: str = "local"

    # Server
    port: int = 8080
    log_level: str = "INFO"

    # Request admission
    max_body_bytes: int = 64_000

    # Pub/Sub
    pubsub_topic: str = "exposures"
    publish_time_seconds: float = 5.0
    publish_max_messages: int = 100
    publish_max_bytes: int = 10_000_00
    publish_max_latency: float = 0.05

    @computed_field
    @property
    def topic_path(self) -> str:
        return f"projects/{self.gcp_project}/topics/{self.pubsub_topic}"


@lru_cache
def get_settings() -> Settings:
    """Cached so the whole app shares one instance; override in tests."""
    return Settings()
