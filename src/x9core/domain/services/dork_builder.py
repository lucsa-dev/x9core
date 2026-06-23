"""Serviços de domínio para montagem de Google Dorks."""

from __future__ import annotations

from datetime import date, timedelta

from x9core.domain.ports.clock import Clock
from x9core.domain.value_objects.dork import Dork
from x9core.domain.value_objects.time_window import TimeWindow, TimeWindowUnit


class DorkBuilder:
    """Monta queries de Google Dork com termos, sites e filtro temporal."""

    def __init__(self, clock: Clock) -> None:
        """Inicializa o builder com um relógio injetável.

        Args:
            clock: Fonte de data/hora para cálculo do operador ``after:``.

        """
        self._clock = clock
        self._terms: list[str] = []
        self._sites: list[str] = []
        self._time_window: TimeWindow | None = None

    def with_terms(self, *terms: str) -> DorkBuilder:
        """Adiciona termos de busca entre aspas, combinados com OR se houver mais de um.

        Args:
            *terms: Nomes, apelidos ou palavras-chave da busca.

        Raises:
            ValueError: Se algum termo estiver vazio.

        """
        for term in terms:
            if not term.strip():
                msg = "termo de busca não pode ser vazio"
                raise ValueError(msg)
            self._terms.append(term.strip())
        return self

    def with_site(self, domain: str) -> DorkBuilder:
        """Adiciona um único domínio com o operador ``site:``."""
        return self.with_sites(domain)

    def with_sites(self, *domains: str) -> DorkBuilder:
        """Adiciona domínios com ``site:``, combinados com OR se houver mais de um.

        Args:
            *domains: Domínios alvo (ex.: ``x.com``, ``instagram.com``).

        Raises:
            ValueError: Se algum domínio estiver vazio.

        """
        for domain in domains:
            normalized = domain.strip()
            if not normalized:
                msg = "site não pode ser vazio"
                raise ValueError(msg)
            self._sites.append(normalized)
        return self

    def with_time_window(self, time_window: TimeWindow) -> DorkBuilder:
        """Define a janela temporal usada para calcular o operador ``after:``."""
        self._time_window = time_window
        return self

    def build(self) -> Dork:
        """Monta e retorna o dork final.

        Raises:
            ValueError: Se nenhum termo de busca tiver sido informado.

        """
        if not self._terms:
            msg = "dork precisa de ao menos um termo de busca"
            raise ValueError(msg)

        parts: list[str] = [_format_terms(self._terms)]

        if self._sites:
            parts.append(_format_sites(self._sites))

        if self._time_window is not None:
            parts.append(_format_after(self._clock, self._time_window))

        return Dork(" ".join(parts))


def _format_terms(terms: list[str]) -> str:
    """Formata termos de busca com aspas e operador OR quando necessário."""
    quoted = [f'"{term}"' for term in terms]
    if len(quoted) == 1:
        return quoted[0]
    return f"({' OR '.join(quoted)})"


def _format_sites(sites: list[str]) -> str:
    """Formata filtros ``site:`` com operador OR quando necessário."""
    formatted = [f"site:{site}" for site in sites]
    if len(formatted) == 1:
        return formatted[0]
    return f"({' OR '.join(formatted)})"


def _format_after(clock: Clock, time_window: TimeWindow) -> str:
    """Gera o operador ``after:YYYY-MM-DD`` a partir da janela temporal."""
    after_date = _calculate_after_date(clock, time_window)
    return f"after:{after_date.isoformat()}"


def _calculate_after_date(clock: Clock, time_window: TimeWindow) -> date:
    """Calcula a data limite inferior para o operador ``after:``."""
    now = clock.now()
    if time_window.unit == TimeWindowUnit.HOURS:
        threshold = now - timedelta(hours=time_window.amount)
    else:
        threshold = now - timedelta(days=time_window.amount)
    return threshold.date()
