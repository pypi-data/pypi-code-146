from pytz import timezone

from shared.external.tools.misc import get_nested_keys
from datetime import datetime


def test_get_nested_keys():
    a = {"a": "b",
         "c": {"d": 1, "e": 2, "h": {"a": "mmm"}}}

    assert get_nested_keys(a) == ["a", "c.d", "c.e", "c.h.a"]