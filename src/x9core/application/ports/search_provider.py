"""Ports da camada de aplicação."""

from typing import Protocol

from x9core.domain.entities.search_hit import SearchHit
from x9core.domain.value_objects.dork import Dork
from x9core.domain.value_objects.time_window import TimeWindow


class SearchProvider(Protocol):
    """Contrato para provedores de busca (scraper Google, fakes, etc.)."""

    async def search(
        self,
        dork: Dork,
        time_window: TimeWindow | None = None,
    ) -> list[SearchHit]:
        """Executa uma busca e retorna resultados orgânicos parseados.

        Args:
            dork: Query de Google Dork montada.
            time_window: Janela temporal opcional para filtros na URL de busca.

        Returns:
            Lista de resultados extraídos da página de busca.

        """
        ...  # pragma: no cover
