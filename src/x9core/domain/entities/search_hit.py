"""Entidades de resultado de busca."""

from dataclasses import dataclass

from x9core.domain.services.url_normalizer import normalize_url


@dataclass(frozen=True, slots=True)
class SearchHit:
    """Um resultado orgânico extraído de uma página de busca."""

    title: str
    url: str
    snippet: str

    @property
    def fingerprint(self) -> str:
        """Identificador estável para deduplicação baseado na URL normalizada."""
        return normalize_url(self.url)
