"""Parsers e adapters de scraping."""

from bs4 import BeautifulSoup, Tag

from x9core.domain.entities.search_hit import SearchHit

_RESULT_SELECTOR = "div.g"
_SNIPPET_SELECTORS = ("div.VwiC3b", "div.IsZvec", "div[data-sncf]")


def parse_google_serp_html(html: str) -> list[SearchHit]:
    """Extrai resultados orgânicos de uma página HTML do Google Search.

    Args:
        html: Conteúdo HTML completo da SERP.

    Returns:
        Lista de hits parseados; entradas inválidas são ignoradas.

    """
    soup = BeautifulSoup(html, "lxml")
    hits: list[SearchHit] = []
    for block in soup.select(_RESULT_SELECTOR):
        hit = _parse_result_block(block)
        if hit is not None:
            hits.append(hit)
    return hits


def _parse_result_block(block: Tag) -> SearchHit | None:
    """Extrai título, URL e snippet de um bloco de resultado."""
    link = block.select_one("a[href^='http']")
    heading = block.select_one("h3")
    if link is None or heading is None:
        return None

    href_raw = link.get("href", "")
    url = (href_raw[0] if isinstance(href_raw, list) else href_raw).strip()
    title = heading.get_text(strip=True)
    if not url or not title:
        return None

    snippet = _extract_snippet(block)
    return SearchHit(title=title, url=url, snippet=snippet)


def _extract_snippet(block: Tag) -> str:
    """Localiza o snippet do resultado usando seletores conhecidos do Google."""
    for selector in _SNIPPET_SELECTORS:
        element = block.select_one(selector)
        if element is not None:
            text = element.get_text(" ", strip=True)
            if text:
                return text
    return ""
