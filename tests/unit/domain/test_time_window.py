import pytest

import x9core
from x9core.domain.value_objects.time_window import TimeWindow, TimeWindowUnit


def test_package_has_version() -> None:
    assert x9core.__version__ == "0.1.0"


class TestTimeWindow:
    def test_hours_factory_creates_valid_window(self) -> None:
        tw = TimeWindow.hours(12)
        assert tw.amount == 12
        assert tw.unit == TimeWindowUnit.HOURS

    def test_days_factory_creates_valid_window(self) -> None:
        tw = TimeWindow.days(7)
        assert tw.amount == 7
        assert tw.unit == TimeWindowUnit.DAYS

    def test_from_string_parses_hours(self) -> None:
        assert TimeWindow.from_string("24h") == TimeWindow.hours(24)

    def test_from_string_parses_days(self) -> None:
        assert TimeWindow.from_string("7d") == TimeWindow.days(7)

    def test_from_string_is_case_insensitive(self) -> None:
        assert TimeWindow.from_string(" 12H ") == TimeWindow.hours(12)

    def test_rejects_zero_amount(self) -> None:
        with pytest.raises(ValueError, match="positivo"):
            TimeWindow.hours(0)

    def test_rejects_negative_amount(self) -> None:
        with pytest.raises(ValueError, match="positivo"):
            TimeWindow.hours(-1)

    def test_from_string_rejects_invalid_format(self) -> None:
        with pytest.raises(ValueError, match="inválido"):
            TimeWindow.from_string("invalid")

    def test_equality(self) -> None:
        assert TimeWindow.hours(24) == TimeWindow.hours(24)
        assert TimeWindow.hours(12) != TimeWindow.hours(24)

    def test_equality_with_other_type_returns_not_implemented(self) -> None:
        tw = TimeWindow.hours(12)
        assert tw.__eq__("12h") is NotImplemented

    def test_hash(self) -> None:
        assert hash(TimeWindow.hours(24)) == hash(TimeWindow.hours(24))

    def test_repr(self) -> None:
        assert repr(TimeWindow.hours(24)) == "TimeWindow(24h)"
