"""Serviços auxiliares do domínio."""

from x9core.domain.entities.search_hit import SearchHit


def deduplicate_hits(hits: list[SearchHit]) -> list[SearchHit]:
    """Remove resultados duplicados preservando a primeira ocorrência.

    Args:
        hits: Lista de resultados brutos da busca.

    Returns:
        Lista sem duplicatas por fingerprint de URL.

    """
    seen: set[str] = set()
    unique: list[SearchHit] = []
    for hit in hits:
        if hit.fingerprint in seen:
            continue
        seen.add(hit.fingerprint)
        unique.append(hit)
    return unique
