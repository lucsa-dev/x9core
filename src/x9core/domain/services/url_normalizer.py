"""Utilitários para normalização de URLs."""

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

_TRACKING_PARAMS = frozenset(
    {
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_term",
        "utm_content",
        "fbclid",
        "gclid",
    },
)


def normalize_url(url: str) -> str:
    """Normaliza URL para deduplicação removendo parâmetros de rastreamento.

    Args:
        url: URL bruta extraída do HTML.

    Returns:
        URL normalizada em minúsculas, sem barra final e sem parâmetros de tracking.

    """
    parsed = urlparse(url.strip())
    filtered_query = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=True)
        if key.lower() not in _TRACKING_PARAMS
    ]
    path = parsed.path.rstrip("/") or "/"
    normalized = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=parsed.netloc.lower(),
        path=path,
        query=urlencode(filtered_query),
        fragment="",
    )
    return urlunparse(normalized)
