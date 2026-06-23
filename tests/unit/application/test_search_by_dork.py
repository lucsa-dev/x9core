import pytest

from x9core.application.use_cases.search_by_dork import SearchByDork, SearchByDorkInput
from x9core.domain.entities.search_hit import SearchHit
from x9core.domain.value_objects.dork import Dork
from x9core.domain.value_objects.time_window import TimeWindow
from x9core.infrastructure.scraping.fake_search_provider import FakeSearchProvider


class TestSearchByDork:
    async def test_returns_parsed_results_from_html_fixture(self, sample_serp_html: str) -> None:
        use_case = SearchByDork(FakeSearchProvider(html=sample_serp_html))
        output = await use_case.execute(
            SearchByDorkInput(dork=Dork('"João Silva" site:x.com')),
        )

        assert output.total_raw == 3
        assert output.total_unique == 2
        assert output.results[0].title == "João Silva no X"

    async def test_deduplicates_by_url_fingerprint(self) -> None:
        duplicate_hit = SearchHit(
            title="A",
            url="https://x.com/post/1?utm_source=twitter",
            snippet="s1",
        )
        same_hit = SearchHit(
            title="B",
            url="https://x.com/post/1",
            snippet="s2",
        )
        use_case = SearchByDork(FakeSearchProvider(hits=[duplicate_hit, same_hit]))
        output = await use_case.execute(SearchByDorkInput(dork=Dork("site:x.com")))

        assert output.total_raw == 2
        assert output.total_unique == 1
        assert output.results[0].title == "A"

    async def test_passes_time_window_to_provider(self) -> None:
        class RecordingProvider(FakeSearchProvider):
            def __init__(self) -> None:
                super().__init__(hits=[])
                self.received_time_window: TimeWindow | None = None

            async def search(
                self,
                dork: Dork,
                time_window: TimeWindow | None = None,
            ) -> list[SearchHit]:
                self.received_time_window = time_window
                return []

        provider = RecordingProvider()
        use_case = SearchByDork(provider)
        time_window = TimeWindow.hours(24)
        await use_case.execute(
            SearchByDorkInput(dork=Dork("test"), time_window=time_window),
        )

        assert provider.received_time_window == time_window

    async def test_returns_empty_when_provider_has_no_results(self) -> None:
        use_case = SearchByDork(FakeSearchProvider(hits=[]))
        output = await use_case.execute(SearchByDorkInput(dork=Dork("vazio")))

        assert output.results == []
        assert output.total_raw == 0
        assert output.total_unique == 0
