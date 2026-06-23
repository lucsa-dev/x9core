import re
from enum import StrEnum

_TIME_WINDOW_PATTERN = re.compile(r"^\d+[hd]$")


class TimeWindowUnit(StrEnum):
    HOURS = "h"
    DAYS = "d"


class TimeWindow:
    """Janela temporal para filtros de busca (ex.: últimas 12h, 24h)."""

    __slots__ = ("_amount", "_unit")

    def __init__(self, amount: int, unit: TimeWindowUnit) -> None:
        if amount <= 0:
            msg = "amount deve ser positivo"
            raise ValueError(msg)
        self._amount = amount
        self._unit = unit

    @classmethod
    def hours(cls, amount: int) -> "TimeWindow":
        return cls(amount=amount, unit=TimeWindowUnit.HOURS)

    @classmethod
    def days(cls, amount: int) -> "TimeWindow":
        return cls(amount=amount, unit=TimeWindowUnit.DAYS)

    @classmethod
    def from_string(cls, value: str) -> "TimeWindow":
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
        return self._amount

    @property
    def unit(self) -> TimeWindowUnit:
        return self._unit

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TimeWindow):
            return NotImplemented
        return self._amount == other._amount and self._unit == other._unit

    def __hash__(self) -> int:
        return hash((self._amount, self._unit))

    def __repr__(self) -> str:
        return f"TimeWindow({self._amount}{self._unit})"
