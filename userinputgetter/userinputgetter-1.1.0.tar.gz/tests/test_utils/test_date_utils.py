import pytest

from userinputgetter.utils.date_utils import get_day_suffix


def test_get_day_suffix():
    with pytest.raises(TypeError):
        get_day_suffix("42")

    assert get_day_suffix(8) == "th"
    assert get_day_suffix(9) == "th"
    assert get_day_suffix(10) == "th"
    assert get_day_suffix(11) == "th"
    assert get_day_suffix(20) == "th"

    assert get_day_suffix(1) == "st"
    assert get_day_suffix(2) == "nd"
    assert get_day_suffix(3) == "rd"

    assert get_day_suffix(31) == "st"
