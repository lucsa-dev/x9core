"""Value objects para janelas temporais de busca."""

import re
from enum import StrEnum

_TIME_WINDOW_PATTERN = re.compile(r"^\d+[hd]$")


class TimeWindowUnit(StrEnum):
    """Unidade de medida de uma janela temporal."""

    HOURS = "h"
    DAYS = "d"


class TimeWindow:
    """Janela temporal para filtros de busca (ex.: últimas 12h, 24h)."""

    __slots__ = ("_amount", "_unit")

    def __init__(self, amount: int, unit: TimeWindowUnit) -> None:
        """Inicializa uma janela temporal.

        Args:
            amount: Quantidade de unidades (deve ser positiva).
            unit: Unidade de tempo (horas ou dias).

        Raises:
            ValueError: Se amount for menor ou igual a zero.

        """
        if amount <= 0:
            msg = "amount deve ser positivo"
            raise ValueError(msg)
        self._amount = amount
        self._unit = unit

    @classmethod
    def hours(cls, amount: int) -> "TimeWindow":
        """Cria uma janela em horas."""
        return cls(amount=amount, unit=TimeWindowUnit.HOURS)

    @classmethod
    def days(cls, amount: int) -> "TimeWindow":
        """Cria uma janela em dias."""
        return cls(amount=amount, unit=TimeWindowUnit.DAYS)

    @classmethod
    def from_string(cls, value: str) -> "TimeWindow":
        """Converte strings como ``12h`` ou ``7d`` em ``TimeWindow``.

        Args:
            value: Representação textual da janela.

        Raises:
            ValueError: Se o formato for inválido.

        """
        normalized = value.strip().lower()
        if not _TIME_WINDOW_PATTERN.fullmatch(normalized):
            msg = f"time_window inválido: {value!r}"
            raise ValueError(msg)
        amount = int(normalized[:-1])
        if normalized.endswith("h"):
            return cls.hours(amount)
        return cls.days(amount)

    @property
    def amount(self) -> int:
        """Quantidade de unidades da janela."""
        return self._amount

    @property
    def unit(self) -> TimeWindowUnit:
        """Unidade de tempo da janela."""
        return self._unit

    def __eq__(self, other: object) -> bool:
        """Compara duas janelas por quantidade e unidade."""
        if not isinstance(other, TimeWindow):
            return NotImplemented
        return self._amount == other._amount and self._unit == other._unit

    def __hash__(self) -> int:
        """Permite uso da janela em conjuntos e como chave de dicionário."""
        return hash((self._amount, self._unit))

    def __repr__(self) -> str:
        """Representação legível para depuração."""
        return f"TimeWindow({self._amount}{self._unit})"
