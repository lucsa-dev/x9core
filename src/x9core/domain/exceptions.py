"""Exceções de regra de negócio do domínio."""


class DomainError(Exception):
    """Erro de regra de negócio do domínio."""


class ValidationError(DomainError):
    """Valor ou entrada inválida no domínio."""
