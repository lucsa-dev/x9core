import pytest

from x9core.domain.entities.search_hit import SearchHit
from x9core.domain.services.dedup_service import deduplicate_hits
from x9core.domain.services.url_normalizer import normalize_url


class TestNormalizeUrl:
    def test_lowercases_scheme_and_host(self) -> None:
        assert normalize_url("HTTPS://X.COM/Path") == "https://x.com/Path"

    def test_removes_trailing_slash(self) -> None:
        assert normalize_url("https://x.com/post/") == "https://x.com/post"

    def test_strips_tracking_parameters(self) -> None:
        url = "https://x.com/post/1?utm_source=twitter&keep=1"
        assert normalize_url(url) == "https://x.com/post/1?keep=1"

    def test_removes_fragment(self) -> None:
        assert normalize_url("https://x.com/post#section") == "https://x.com/post"


class TestSearchHitFingerprint:
    def test_fingerprint_uses_normalized_url(self) -> None:
        hit = SearchHit(
            title="t",
            url="https://X.COM/post/?utm_source=a",
            snippet="s",
        )
        assert hit.fingerprint == "https://x.com/post"


class TestDeduplicateHits:
    def test_removes_duplicates_preserving_first(self) -> None:
        hits = [
            SearchHit(title="A", url="https://x.com/1", snippet="s1"),
            SearchHit(title="B", url="https://x.com/1/", snippet="s2"),
            SearchHit(title="C", url="https://instagram.com/p/1", snippet="s3"),
        ]
        unique = deduplicate_hits(hits)

        assert len(unique) == 2
        assert unique[0].title == "A"
        assert unique[1].title == "C"

    def test_returns_empty_for_empty_input(self) -> None:
        assert deduplicate_hits([]) == []
