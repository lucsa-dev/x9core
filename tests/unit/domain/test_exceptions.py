from x9core.domain.exceptions import DomainError, ValidationError


def test_domain_error_is_exception() -> None:
    assert issubclass(DomainError, Exception)


def test_validation_error_inherits_from_domain_error() -> None:
    assert issubclass(ValidationError, DomainError)
    err = ValidationError("campo inválido")
    assert str(err) == "campo inválido"
