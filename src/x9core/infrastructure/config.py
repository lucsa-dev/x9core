from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "x9core"
    app_env: str = "development"
    debug: bool = False

    database_url: str = "postgresql+asyncpg://x9core:x9core@postgres:5432/x9core"
    redis_url: str = "redis://redis:6379/0"

    serp_api_key: str = ""

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"


def get_settings() -> Settings:
    return Settings()
