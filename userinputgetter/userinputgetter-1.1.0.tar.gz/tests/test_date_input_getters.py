import datetime as dt
import pytest

from userinputgetter.date_input_getters import _AnyDateInputGetter
from userinputgetter.date_input_getters import _SpecifiedDateInputGetter
from userinputgetter.date_input_getters import DateInputGetter


class Test_SpecifiedDateInputGetter:
    @pytest.fixture()
    def valid_inputs(self, supported_options):
        yield (
            supported_options[0].strftime("%Y-%m-%d"),
            supported_options[0].strftime("%Y/%m/%d"),
            supported_options[0].strftime("%Y%m%d"),
            supported_options[0].strftime("%d-%m-%Y"),
            supported_options[1].strftime("%d-%m-%Y"),
            supported_options[2].strftime("%d-%m-%Y"),
            supported_options[0].strftime("%d-%m"),
            supported_options[1].strftime("%d-%m"),
            supported_options[2].strftime("%d-%m"),
            supported_options[0].strftime("%d/%m"),
            supported_options[1].strftime("%d/%m"),
            supported_options[2].strftime("%d/%m"),
            str(supported_options[0].day),
            "Thu",
            "Fri",
            "23rd",
            supported_options[1].strftime("%A"),
            supported_options[2].strftime("%A")[:3],
        )

    @pytest.fixture()
    def invalid_inputs(self):
        yield (
            "February",
            "2022-35-19"
        )

    @pytest.fixture()
    def supported_options(self):
        yield (dt.date(2022, 1, 1), dt.date(2022, 2, 2), dt.date(2022, 3, 3))

    @pytest.fixture
    def unsupported_options(self):
        yield (dt.date(2023, 1, 1), dt.date(2022, 2, 1))

    @pytest.fixture()
    def date_input_getter(self, supported_options):
        yield _SpecifiedDateInputGetter(supported_options)

    def test_initialiser(self):
        with pytest.raises(TypeError):
            _SpecifiedDateInputGetter(("2022-01-01",))

        with pytest.raises(ValueError):
            _SpecifiedDateInputGetter(tuple())

        _SpecifiedDateInputGetter((dt.date(2022, 1, 1), dt.date(2022, 12, 25)))

    def test_is_valid(self, date_input_getter, valid_inputs, invalid_inputs):
        assert all(date_input_getter.is_valid(x) for x in valid_inputs)
        assert not any(date_input_getter.is_valid(x) for x in invalid_inputs)

    def test_is_supported(self, date_input_getter, supported_options, unsupported_options):
        assert all(date_input_getter.is_supported(x) for x in supported_options)
        assert not any(date_input_getter.is_supported(x) for x in unsupported_options)

    def test_parse(self, date_input_getter, valid_inputs, supported_options):
        expected_outputs = (
            supported_options[0],
            supported_options[0],
            supported_options[0],
            supported_options[0],
            supported_options[1],
            supported_options[2],
            supported_options[0],
            supported_options[1],
            supported_options[2],
            supported_options[0],
            supported_options[1],
            supported_options[2],
            supported_options[0],
            supported_options[2],
            "Fri",
            "23rd",
            supported_options[1],
            supported_options[2]
        )
        observed_outputs = tuple(date_input_getter.parse(x) for x in valid_inputs)

        assert observed_outputs == expected_outputs

    def test_get_input(self, date_input_getter, supported_options, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: supported_options[0].strftime("%Y%m%d"))
        assert date_input_getter.get_input() == supported_options[0]

    def test_get_multiple_inputs(self, date_input_getter, supported_options, monkeypatch):
        monkeypatch.setattr(
            'builtins.input',
            lambda _: (
                f"{supported_options[0].strftime('%A')[:3]}, "
                f"{supported_options[1].strftime('%A')[:3]}"
            )
        )

        assert date_input_getter.get_multiple_inputs() == (
            supported_options[0],
            supported_options[1]
        )


class Test_AnyDateInputGetter:
    @pytest.fixture()
    def date_input_getter(self):
        yield _AnyDateInputGetter()

    @pytest.fixture()
    def valid_inputs(self):
        yield (
            "2022-12-25",
            "25-12-2022",
            "01-01-2022",
            "1990-01-01",
        )

    @pytest.fixture()
    def invalid_inputs(self):
        yield (
            "Fri",
            "February",
            "3rd Jan 2022"
        )

    def test_initialiser(self):
        with pytest.raises(TypeError):
            _AnyDateInputGetter("2022-01-01")  # pylint: disable=too-many-function-args

        with pytest.raises(TypeError):
            _AnyDateInputGetter(dt.date(2022, 1, 1))  # pylint: disable=too-many-function-args

        with pytest.raises(TypeError):
            _AnyDateInputGetter((dt.date(2022, 1, 1), ))  # pylint: disable=too-many-function-args

        _AnyDateInputGetter()

    def test_is_valid(self, date_input_getter, valid_inputs, invalid_inputs):
        assert all(date_input_getter.is_valid(x) for x in valid_inputs)
        assert not any(date_input_getter.is_valid(x) for x in invalid_inputs)

    def test_parse(self, date_input_getter, valid_inputs):
        expected_outputs = (
            dt.date(2022, 12, 25),
            dt.date(2022, 12, 25),
            dt.date(2022, 1, 1),
            dt.date(1990, 1, 1),
        )
        observed_outputs = tuple(date_input_getter.parse(x) for x in valid_inputs)

        assert observed_outputs == expected_outputs

    def test_get_input(self, date_input_getter, valid_inputs, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: valid_inputs[0])
        assert date_input_getter.get_input() == dt.date(2022, 12, 25)

    def test_get_multiple_inputs(self, date_input_getter, valid_inputs, monkeypatch):
        monkeypatch.setattr(
            'builtins.input',
            lambda _: ", ".join((valid_inputs[0], valid_inputs[3]))
        )

        assert date_input_getter.get_multiple_inputs() == (
            dt.date(2022, 12, 25),
            dt.date(1990, 1, 1)
        )


class TestDateInputGetter:
    def test_init(self):
        assert isinstance(DateInputGetter(), _AnyDateInputGetter)
        assert isinstance(DateInputGetter(dt.date(2022, 12, 25)), _SpecifiedDateInputGetter)
        assert isinstance(
            DateInputGetter((dt.date(2022, 12, 25), dt.date(1990, 1, 1))),
            _SpecifiedDateInputGetter
        )
