from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    port: int = 8080
    log_level: str = "info"
    env: str = "dev"
    app_mode: str = "receiver"
    gcp_project: str = ""
    gcs_bucket: str = ""
    gcs_prefix: str = "rum-poc"
    local_output_dir: str = "./local-gcs"
    pubsub_topic: str = ""
    pubsub_subscription: str = ""
    job_pull_max_messages: int = 100
    job_max_batches: int = 10


settings = Settings()
