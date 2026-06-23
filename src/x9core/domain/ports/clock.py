"""Ports de tempo para serviços de domínio."""

from datetime import datetime
from typing import Protocol


class Clock(Protocol):
    """Contrato para leitura da data e hora atual."""

    def now(self) -> datetime:
        """Retorna o instante atual no fuso do provedor."""
        ...  # pragma: no cover
