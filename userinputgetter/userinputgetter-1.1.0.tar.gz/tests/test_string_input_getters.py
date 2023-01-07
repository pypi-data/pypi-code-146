import pytest

from userinputgetter.string_input_getters import CaseInsensitiveStringInputGetter


class TestCaseInsensitiveStringInputGetter:
    @pytest.fixture()
    def any_case_insensitive_string_input_getter(self):
        yield CaseInsensitiveStringInputGetter()

    @pytest.fixture()
    def supported_options(self):
        yield ("foo", "bar", "BAZ")

    @pytest.fixture()
    def specified_case_insensitive_string_input_getter(self, supported_options):
        yield CaseInsensitiveStringInputGetter(supported_options)

    @pytest.fixture()
    def inputs(self):
        yield ("foo", "bar", "car", "draw")

    def test_is_valid(self, any_case_insensitive_string_input_getter, inputs):
        assert all(any_case_insensitive_string_input_getter.is_valid(x) for x in inputs)

    def test_parse(
        self,
        any_case_insensitive_string_input_getter,
        specified_case_insensitive_string_input_getter
    ):

        assert any_case_insensitive_string_input_getter.parse("AbC") == "AbC"
        assert any_case_insensitive_string_input_getter.parse("ABC") == "ABC"
        assert any_case_insensitive_string_input_getter.parse("42.0") == "42.0"

        assert specified_case_insensitive_string_input_getter.parse("FoO") == "foo"
        assert specified_case_insensitive_string_input_getter.parse("BAR") == "bar"
        assert specified_case_insensitive_string_input_getter.parse("baz") == "BAZ"
        assert specified_case_insensitive_string_input_getter.parse("BAZ") == "BAZ"

    def test_get_input(
        self,
        any_case_insensitive_string_input_getter,
        specified_case_insensitive_string_input_getter,
        monkeypatch
    ):

        monkeypatch.setattr('builtins.input', lambda _: "FOO")
        assert any_case_insensitive_string_input_getter.get_input() == "FOO"
        assert specified_case_insensitive_string_input_getter.get_input() == "foo"

        monkeypatch.setattr('builtins.input', lambda _: "BaZ")
        assert specified_case_insensitive_string_input_getter.get_input() == "BAZ"

    def test_get_multiple_inputs(
        self,
        any_case_insensitive_string_input_getter,
        specified_case_insensitive_string_input_getter,
        monkeypatch
    ):

        monkeypatch.setattr('builtins.input', lambda _: "fOo, fOO, BAR")

        assert any_case_insensitive_string_input_getter.get_multiple_inputs() == (
            "fOo", "fOO", "BAR"
        )
        assert specified_case_insensitive_string_input_getter.get_multiple_inputs() == (
            "foo", "foo", "bar"
        )
