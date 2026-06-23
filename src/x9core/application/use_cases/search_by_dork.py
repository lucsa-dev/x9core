"""Casos de uso da aplicação."""

from dataclasses import dataclass

from x9core.application.ports.search_provider import SearchProvider
from x9core.domain.entities.search_hit import SearchHit
from x9core.domain.services.dedup_service import deduplicate_hits
from x9core.domain.value_objects.dork import Dork
from x9core.domain.value_objects.time_window import TimeWindow


@dataclass(frozen=True, slots=True)
class SearchByDorkInput:
    """Entrada do caso de uso de busca por dork."""

    dork: Dork
    time_window: TimeWindow | None = None


@dataclass(frozen=True, slots=True)
class SearchByDorkOutput:
    """Saída do caso de uso de busca por dork."""

    results: list[SearchHit]
    total_raw: int
    total_unique: int


class SearchByDork:
    """Orquestra busca por dork com deduplicação de resultados."""

    def __init__(self, search_provider: SearchProvider) -> None:
        """Inicializa o caso de uso com um provedor de busca injetável.

        Args:
            search_provider: Adapter que executa a busca (scraper ou fake).

        """
        self._search_provider = search_provider

    async def execute(self, input_data: SearchByDorkInput) -> SearchByDorkOutput:
        """Executa a busca e remove duplicatas por URL.

        Args:
            input_data: Dork e janela temporal opcional.

        Returns:
            Resultados únicos e contadores de bruto vs deduplicado.

        """
        raw_hits = await self._search_provider.search(input_data.dork, input_data.time_window)
        unique_hits = deduplicate_hits(raw_hits)
        return SearchByDorkOutput(
            results=unique_hits,
            total_raw=len(raw_hits),
            total_unique=len(unique_hits),
        )
