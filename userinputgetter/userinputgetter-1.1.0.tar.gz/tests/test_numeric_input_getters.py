import datetime as dt
import pytest

from userinputgetter.numeric_input_getters import IntegerInputGetter


class TestIntegerInputGetter:
    @pytest.fixture()
    def any_integer_input_getter(self):
        yield IntegerInputGetter()

    @pytest.fixture()
    def supported_options(self):
        yield (42, 100, 142)

    @pytest.fixture()
    def unsupported_options(self):
        yield (200, -42)

    @pytest.fixture()
    def specified_integer_input_getter(self, supported_options):
        yield IntegerInputGetter(supported_options)

    @pytest.fixture()
    def valid_inputs(self):
        yield ("1", "42", "99", "100", "-42")

    @pytest.fixture()
    def invalid_inputs(self):
        yield ("1.0", "Five")

    def test_initialiser(self):
        with pytest.raises(TypeError):
            IntegerInputGetter(("42"),)

    def test_is_valid(self, any_integer_input_getter, valid_inputs, invalid_inputs):
        assert all(any_integer_input_getter.is_valid(x) for x in valid_inputs)
        assert not any(any_integer_input_getter.is_valid(x) for x in invalid_inputs)

    def test_parse(self, any_integer_input_getter, valid_inputs):
        expected_outputs = (1, 42, 99, 100, -42)
        observed_outputs = tuple(any_integer_input_getter.parse(x) for x in valid_inputs)

        assert expected_outputs == observed_outputs

    def is_supported(
        self,
        any_integer_input_getter,
        specified_integer_input_getter,
        supported_options,
        unsupported_options
    ):

        assert all(any_integer_input_getter.is_supported(x) for x in supported_options)
        assert all(any_integer_input_getter.is_supported(x) for x in unsupported_options)

        assert all(specified_integer_input_getter.is_supported(x) for x in supported_options)
        assert not any(specified_integer_input_getter.is_supported(x) for x in unsupported_options)

    def test_get_input(self, any_integer_input_getter, specified_integer_input_getter, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: "42")

        for getter in (any_integer_input_getter, specified_integer_input_getter):
            assert getter.get_input() == 42

    def test_get_multiple_inputs(
        self,
        any_integer_input_getter,
        specified_integer_input_getter,
        monkeypatch
    ):

        monkeypatch.setattr('builtins.input', lambda _: "42, 100")

        for getter in (any_integer_input_getter, specified_integer_input_getter):
            assert getter.get_multiple_inputs() == (42, 100)
