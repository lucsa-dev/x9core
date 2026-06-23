import pytest

from x9core.domain.value_objects.dork import Dork


class TestDork:
    def test_creates_from_valid_query(self) -> None:
        dork = Dork('"João Silva" site:x.com')
        assert str(dork) == '"João Silva" site:x.com'

    def test_strips_whitespace(self) -> None:
        dork = Dork('  "João Silva"  ')
        assert str(dork) == '"João Silva"'

    def test_rejects_empty_string(self) -> None:
        with pytest.raises(ValueError, match="vazio"):
            Dork("")

    def test_rejects_whitespace_only(self) -> None:
        with pytest.raises(ValueError, match="vazio"):
            Dork("   ")

    def test_equality(self) -> None:
        assert Dork("site:x.com") == Dork("site:x.com")
        assert Dork("site:x.com") != Dork("site:instagram.com")

    def test_equality_with_other_type_returns_not_implemented(self) -> None:
        assert Dork("site:x.com").__eq__("site:x.com") is NotImplemented

    def test_hash(self) -> None:
        assert hash(Dork("site:x.com")) == hash(Dork("site:x.com"))

    def test_repr(self) -> None:
        assert repr(Dork("site:x.com")) == 'Dork(\'site:x.com\')'
