import pytest
from datetime import UTC, datetime

from x9core.domain.services.dork_builder import DorkBuilder
from x9core.domain.value_objects.dork import Dork
from x9core.domain.value_objects.time_window import TimeWindow


class FixedClock:
    def __init__(self, moment: datetime) -> None:
        self._moment = moment

    def now(self) -> datetime:
        return self._moment


class TestDorkBuilder:
    def test_builds_dork_with_single_quoted_term(self) -> None:
        clock = FixedClock(datetime(2026, 6, 23, 12, 0, tzinfo=UTC))
        dork = DorkBuilder(clock).with_terms("João Silva").build()
        assert str(dork) == '"João Silva"'

    def test_builds_dork_with_multiple_terms_or_joined(self) -> None:
        clock = FixedClock(datetime(2026, 6, 23, 12, 0, tzinfo=UTC))
        dork = DorkBuilder(clock).with_terms("João Silva", "joao").build()
        assert str(dork) == '("João Silva" OR "joao")'

    def test_builds_dork_with_single_site(self) -> None:
        clock = FixedClock(datetime(2026, 6, 23, 12, 0, tzinfo=UTC))
        dork = DorkBuilder(clock).with_terms("João Silva").with_site("x.com").build()
        assert str(dork) == '"João Silva" site:x.com'

    def test_builds_dork_with_multiple_sites_or_joined(self) -> None:
        clock = FixedClock(datetime(2026, 6, 23, 12, 0, tzinfo=UTC))
        dork = (
            DorkBuilder(clock)
            .with_terms("João Silva")
            .with_sites("x.com", "twitter.com")
            .build()
        )
        assert str(dork) == '"João Silva" (site:x.com OR site:twitter.com)'

    def test_adds_after_operator_for_24h_window(self) -> None:
        clock = FixedClock(datetime(2026, 6, 23, 12, 0, tzinfo=UTC))
        dork = (
            DorkBuilder(clock)
            .with_terms("João Silva")
            .with_time_window(TimeWindow.hours(24))
            .build()
        )
        assert str(dork) == '"João Silva" after:2026-06-22'

    def test_adds_after_operator_for_12h_window(self) -> None:
        clock = FixedClock(datetime(2026, 6, 23, 12, 0, tzinfo=UTC))
        dork = (
            DorkBuilder(clock)
            .with_terms("João Silva")
            .with_time_window(TimeWindow.hours(12))
            .build()
        )
        assert str(dork) == '"João Silva" after:2026-06-23'

    def test_adds_after_operator_for_multi_day_window(self) -> None:
        clock = FixedClock(datetime(2026, 6, 23, 12, 0, tzinfo=UTC))
        dork = (
            DorkBuilder(clock)
            .with_terms("João Silva")
            .with_time_window(TimeWindow.days(7))
            .build()
        )
        assert str(dork) == '"João Silva" after:2026-06-16'

    def test_builds_full_dork_with_all_parts(self) -> None:
        clock = FixedClock(datetime(2026, 6, 23, 12, 0, tzinfo=UTC))
        dork = (
            DorkBuilder(clock)
            .with_terms("João Silva", "joao")
            .with_sites("x.com", "instagram.com")
            .with_time_window(TimeWindow.hours(24))
            .build()
        )
        assert (
            str(dork)
            == '("João Silva" OR "joao") (site:x.com OR site:instagram.com) after:2026-06-22'
        )

    def test_accepts_clock_protocol_implementation(self) -> None:
        class AnotherClock:
            def now(self) -> datetime:
                return datetime(2026, 6, 23, 12, 0, tzinfo=UTC)

        dork = DorkBuilder(AnotherClock()).with_terms("João Silva").build()
        assert isinstance(dork, Dork)

    def test_rejects_build_without_terms(self) -> None:
        clock = FixedClock(datetime(2026, 6, 23, 12, 0, tzinfo=UTC))
        with pytest.raises(ValueError, match="termo"):
            DorkBuilder(clock).build()

    def test_rejects_empty_term(self) -> None:
        clock = FixedClock(datetime(2026, 6, 23, 12, 0, tzinfo=UTC))
        with pytest.raises(ValueError, match="vazio"):
            DorkBuilder(clock).with_terms("").build()

    def test_rejects_empty_site(self) -> None:
        clock = FixedClock(datetime(2026, 6, 23, 12, 0, tzinfo=UTC))
        with pytest.raises(ValueError, match="site"):
            DorkBuilder(clock).with_terms("João Silva").with_site("  ").build()

    def test_builder_is_reusable_after_build(self) -> None:
        clock = FixedClock(datetime(2026, 6, 23, 12, 0, tzinfo=UTC))
        builder = DorkBuilder(clock).with_terms("João Silva")
        assert str(builder.build()) == '"João Silva"'
        dork = builder.with_site("x.com").build()
        assert str(dork) == '"João Silva" site:x.com'
