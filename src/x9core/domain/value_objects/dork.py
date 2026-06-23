"""Value objects relacionados a Google Dorks."""


class Dork:
    """Query string de Google Dork para busca."""

    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        """Cria um dork a partir de uma query já montada.

        Args:
            value: Texto completo da query de busca.

        Raises:
            ValueError: Se a query estiver vazia após normalização.

        """
        normalized = value.strip()
        if not normalized:
            msg = "dork não pode ser vazio"
            raise ValueError(msg)
        self._value = normalized

    def __str__(self) -> str:
        """Retorna a query pronta para envio ao provedor de busca."""
        return self._value

    def __eq__(self, other: object) -> bool:
        """Compara dois dorks pelo valor da query."""
        if not isinstance(other, Dork):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        """Permite uso do dork em conjuntos e como chave de dicionário."""
        return hash(self._value)

    def __repr__(self) -> str:
        """Representação legível para depuração."""
        return f"Dork({self._value!r})"
