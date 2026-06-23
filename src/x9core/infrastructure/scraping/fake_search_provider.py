"""Implementações fake de scraping para testes e desenvolvimento offline."""

from x9core.domain.entities.search_hit import SearchHit
from x9core.domain.value_objects.dork import Dork
from x9core.domain.value_objects.time_window import TimeWindow
from x9core.infrastructure.scraping.google_serp_parser import parse_google_serp_html


class FakeSearchProvider:
    """Provedor de busca em memória ou baseado em HTML fixture."""

    def __init__(
        self,
        hits: list[SearchHit] | None = None,
        html: str | None = None,
    ) -> None:
        """Configura o fake com hits explícitos ou HTML para parsear.

        Args:
            hits: Resultados fixos retornados diretamente.
            html: HTML da SERP parseado em tempo de busca.

        Raises:
            ValueError: Se nenhuma fonte de dados for informada.

        """
        if hits is None and html is None:
            msg = "FakeSearchProvider requer hits ou html"
            raise ValueError(msg)
        self._hits = hits
        self._html = html

    async def search(
        self,
        dork: Dork,
        time_window: TimeWindow | None = None,
    ) -> list[SearchHit]:
        """Retorna hits configurados ou parseia o HTML fixture."""
        _ = dork, time_window
        if self._hits is not None:
            return list(self._hits)
        assert self._html is not None
        return parse_google_serp_html(self._html)
