"""Aplicação FastAPI do x9core."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from x9core import __version__
from x9core.api.routes.search import router as search_router
from x9core.infrastructure.config import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Cria e configura a aplicação FastAPI.

    Args:
        settings: Configurações opcionais; usa variáveis de ambiente por padrão.

    Returns:
        Instância configurada do FastAPI com rotas registradas.

    """
    settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        """Gerencia o ciclo de vida da aplicação (startup e shutdown)."""
        yield

    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        lifespan=lifespan,
    )

    app.include_router(search_router)

    @app.get("/health")
    async def health() -> dict[str, str]:
        """Retorna o status operacional da API."""
        return {"status": "ok", "version": __version__}

    return app


app = create_app()
