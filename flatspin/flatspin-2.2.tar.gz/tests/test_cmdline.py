import pytest
from flatspin.cmdline import parse_filter

def test_parse_filter():
    parsed_filter = parse_filter("1")
    assert parsed_filter == 1
    assert isinstance(parsed_filter, int)

    parsed_filter =  parse_filter("1.0")
    assert parsed_filter == 1.0
    assert isinstance(parsed_filter, float)

    assert parse_filter("(1,2,3)") == (1,2,3)
    assert parse_filter("[1,2,3]") == [1,2,3]

    assert parse_filter("1::") == slice(1, None, None)
    assert parse_filter("1:") == slice(1, None, None)
    assert parse_filter("1:2:3") == slice(1, 2, 3)
    assert parse_filter("1:2:") == slice(1, 2, None)

    assert parse_filter("float.is_integer") == float.is_integer
    assert callable(parse_filter("lambda x: x>5"))


