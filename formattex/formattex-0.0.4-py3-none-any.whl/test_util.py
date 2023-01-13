from .intermediate_repr import remove_double_newline


def test_remove_double_newline():
    expressions = list("ab\nc\n\nd")
    result = ["a", "b", "\n", "c", "\n\n", "d"]
    assert remove_double_newline(expressions) == result
