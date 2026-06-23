import pytest

from x9core.domain.entities.search_hit import SearchHit
from x9core.domain.value_objects.dork import Dork
from x9core.infrastructure.scraping.fake_search_provider import FakeSearchProvider


class TestFakeSearchProvider:
    async def test_returns_configured_hits(self) -> None:
        hits = [SearchHit(title="A", url="https://a.com", snippet="s")]
        provider = FakeSearchProvider(hits=hits)

        result = await provider.search(Dork("site:a.com"))

        assert result == hits

    async def test_parses_html_when_configured(self) -> None:
        html = """
        <html><body>
          <div class="g">
            <a href="https://example.com"><h3>Exemplo</h3></a>
            <div class="VwiC3b"><span>Snippet</span></div>
          </div>
        </body></html>
        """
        provider = FakeSearchProvider(html=html)

        result = await provider.search(Dork("exemplo"))

        assert len(result) == 1
        assert result[0].title == "Exemplo"

    def test_requires_hits_or_html(self) -> None:
        with pytest.raises(ValueError, match="hits ou html"):
            FakeSearchProvider()
