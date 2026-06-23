"""Configuração da aplicação via variáveis de ambiente."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações carregadas de variáveis de ambiente e arquivo ``.env``."""

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

    scraper_headless: bool = True
    scraper_proxy_url: str = ""
    scraper_request_delay_seconds: float = 2.0

    @property
    def is_development(self) -> bool:
        """Indica se a aplicação está rodando em ambiente de desenvolvimento."""
        return self.app_env == "development"


def get_settings() -> Settings:
    """Retorna as configurações da aplicação."""
    return Settings()
