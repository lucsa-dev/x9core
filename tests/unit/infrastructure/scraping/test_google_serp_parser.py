import pytest

from x9core.infrastructure.scraping.google_serp_parser import parse_google_serp_html


class TestParseGoogleSerpHtml:
    def test_parses_organic_results_from_fixture(self, sample_serp_html: str) -> None:
        hits = parse_google_serp_html(sample_serp_html)

        assert len(hits) == 3
        assert hits[0].title == "João Silva no X"
        assert hits[0].url == "https://x.com/joao/status/123456"
        assert "Post recente" in hits[0].snippet

    def test_parses_instagram_result(self, sample_serp_html: str) -> None:
        hits = parse_google_serp_html(sample_serp_html)

        assert hits[1].title == "João Silva no Instagram"
        assert hits[1].url == "https://www.instagram.com/p/ABC123/"

    def test_returns_empty_list_for_html_without_results(self) -> None:
        hits = parse_google_serp_html("<html><body><p>sem resultados</p></body></html>")
        assert hits == []

    def test_skips_blocks_without_link_or_title(self) -> None:
        html = """
        <html><body>
          <div class="g"><span>incompleto</span></div>
          <div class="g">
            <a href="https://example.com"><h3>Exemplo</h3></a>
            <div class="VwiC3b"><span>Snippet válido</span></div>
          </div>
        </body></html>
        """
        hits = parse_google_serp_html(html)

        assert len(hits) == 1
        assert hits[0].title == "Exemplo"

    def test_skips_blocks_with_empty_title(self) -> None:
        html = """
        <html><body>
          <div class="g">
            <a href="https://example.com"><h3></h3></a>
            <div class="VwiC3b"><span>Snippet ignorado</span></div>
          </div>
        </body></html>
        """
        hits = parse_google_serp_html(html)

        assert hits == []

    def test_uses_iszvec_selector_for_snippet(self) -> None:
        html = """
        <html><body>
          <div class="g">
            <a href="https://example.com"><h3>Título</h3></a>
            <div class="IsZvec">Snippet via IsZvec</div>
          </div>
        </body></html>
        """
        hits = parse_google_serp_html(html)

        assert hits[0].snippet == "Snippet via IsZvec"

    def test_uses_data_sncf_selector_for_snippet(self) -> None:
        html = """
        <html><body>
          <div class="g">
            <a href="https://example.com"><h3>Título</h3></a>
            <div data-sncf="1">Snippet via data-sncf</div>
          </div>
        </body></html>
        """
        hits = parse_google_serp_html(html)

        assert hits[0].snippet == "Snippet via data-sncf"

    def test_skips_empty_snippet_element_and_uses_next_selector(self) -> None:
        html = """
        <html><body>
          <div class="g">
            <a href="https://example.com"><h3>Título</h3></a>
            <div class="VwiC3b"><span>   </span></div>
            <div class="IsZvec">Snippet válido</div>
          </div>
        </body></html>
        """
        hits = parse_google_serp_html(html)

        assert hits[0].snippet == "Snippet válido"

    def test_uses_empty_snippet_when_not_found(self) -> None:
        html = """
        <html><body>
          <div class="g">
            <a href="https://example.com"><h3>Sem snippet</h3></a>
          </div>
        </body></html>
        """
        hits = parse_google_serp_html(html)

        assert hits[0].snippet == ""
