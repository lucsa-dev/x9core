"""Injeção de dependências da API."""

from typing import Annotated

from fastapi import Depends, HTTPException, status

from x9core.application.ports.search_provider import SearchProvider
from x9core.application.use_cases.search_by_dork import SearchByDork


def get_search_provider() -> SearchProvider:
    """Retorna o provedor de busca configurado.

    Raises:
        HTTPException: Quando o scraper Google ainda não estiver configurado (Step 4).

    """
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Scraper Google não configurado. Disponível após Step 4.",
    )


def get_search_by_dork(
    search_provider: Annotated[SearchProvider, Depends(get_search_provider)],
) -> SearchByDork:
    """Monta o caso de uso de busca com o provedor injetado."""
    return SearchByDork(search_provider)


SearchByDorkDep = Annotated[SearchByDork, Depends(get_search_by_dork)]
