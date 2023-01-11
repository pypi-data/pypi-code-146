import datetime

import arrow
import pytest

from w.services.technical.date_service import DateService
from w.tests.helpers import date_test_helper
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestDateService(TestCaseMixin):
    @staticmethod
    def setup_method():
        DateService.clear()

    @classmethod
    def teardown_class(cls):
        DateService.clear()

    """
    previous_weekday
    """

    def test_previous_weekday_with_date_equals_seeking_day(self):
        actual = DateService.previous_weekday(arrow.get("2017-10-04"), DateService.WED)
        expected = arrow.get("2017-10-04")
        assert expected == actual

    def test_previous_weekday_with_date_after_seeking_day(self):
        actual = DateService.previous_weekday(arrow.get("2017-10-06"), DateService.WED)
        expected = arrow.get("2017-10-04")
        assert expected == actual

    def test_previous_weekday_with_date_before_seeking_day(self):
        actual = DateService.previous_weekday(arrow.get("2017-10-03"), DateService.WED)
        expected = arrow.get("2017-09-27")
        assert expected == actual

    """
    next_weekday
    """

    def test_next_weekday_with_date_equals_seeking_day(self):
        actual = DateService.next_weekday(arrow.get("2017-10-04"), DateService.WED)
        expected = arrow.get("2017-10-04")
        assert expected == actual

    def test_next_weekday_with_date_after_seeking_day(self):
        actual = DateService.next_weekday(arrow.get("2017-10-06"), DateService.WED)
        expected = arrow.get("2017-10-11")
        assert expected == actual

    def test_next_weekday_with_date_before_seeking_day(self):
        actual = DateService.next_weekday(arrow.get("2017-10-03"), DateService.WED)
        expected = arrow.get("2017-10-04")
        assert expected == actual

    """
    get_weekday_date
    """

    def test_get_weekday_date_with_seeking_day_same_as_date_return_date(self):
        """
        Ensure return will be the same as date if seeking day is same as day date
        and use datetime.datetime as date
        """
        date = datetime.date(2018, 4, 25)
        assert arrow.get("2018-04-25") == DateService.get_weekday_date(
            date, DateService.WED
        )

    def test_get_weekday_date_with_seeking_day_before_return_date(self):
        """
        Ensure get date succeed with seeking day before date and use Arrow as date
        """
        assert arrow.get("2018-04-30") == DateService.get_weekday_date(
            arrow.get("2018-05-02"), DateService.MON
        )

    def test_get_weekday_date_with_seeking_day_after_date_return_date(self):
        """
        Ensure get date succeed with seeking day after date and use datetime.date
        as date
        """
        date = datetime.datetime(2018, 4, 25)
        assert arrow.get("2018-04-28") == DateService.get_weekday_date(
            date, DateService.SAT
        )

    """
    to_mysql_date
    """

    def test_to_mysql_date_with_success_return_str(self):
        expected = "2018-05-01"
        assert (
            datetime.datetime.now().strftime("%Y-%m-%d") == DateService.to_mysql_date()
        )
        assert expected == DateService.to_mysql_date(datetime.datetime(2018, 5, 1))
        assert expected == DateService.to_mysql_date(datetime.date(2018, 5, 1))
        assert expected == DateService.to_mysql_date(arrow.get("2018-05-01"))

    """
    to_mysql_datetime
    """

    def test_to_mysql_datetime_with_success_return_str(self):
        expected = "2018-05-01 15:18:36.224469"

        with date_test_helper.today_is(expected):
            assert expected == DateService.to_mysql_datetime()

        assert expected == DateService.to_mysql_datetime(
            datetime.datetime(2018, 5, 1, 15, 18, 36, 224469)
        )
        assert expected == DateService.to_mysql_datetime(
            arrow.get("2018-05-01 15:18:36.224469")
        )

    def test_to_mysql_datetime_with_timezone_return_str(self):
        DateService.set_timezone("Europe/Paris")

        expected = "2018-05-01 15:18:36.224469"

        with date_test_helper.today_is("2018-05-01 13:18:36.224469"):
            assert expected == DateService.to_mysql_datetime()

        assert expected == DateService.to_mysql_datetime(
            datetime.datetime(2018, 5, 1, 13, 18, 36, 224469)
        )
        assert expected == DateService.to_mysql_datetime(
            arrow.get("2018-05-01 13:18:36.224469")
        )

    """
    week_number
    """

    def test_week_number_success_return_int(self):
        assert 18 == DateService.week_number(datetime.datetime(2018, 5, 1))
        assert 18 == DateService.week_number(datetime.date(2018, 5, 1))
        assert 18 == DateService.week_number(arrow.get("2018-05-01"))
        assert (
            DateService.week_number(datetime.date.today()) == DateService.week_number()
        )

    """
    to_date
    """

    def test_to_date_with_success_return_date(self):
        assert isinstance(DateService.to_date(), datetime.date)
        assert isinstance(
            DateService.to_date("2019-03-18T11:16:34.786+01:00"), datetime.date
        )

    """
    is_between
    """

    def test_is_between_with_end_before_start_raise_runtime_error(self):
        with pytest.raises(RuntimeError):
            DateService.is_between("2018-03-05", "2018-03-05", "2018-02-07")

    def test_is_between_with_date_not_between_return_false(self):
        assert not DateService.is_between(DateService.now(), "2018-02-05", "2018-02-06")

    def test_is_between_with_success_return_true(self):
        assert DateService.is_between("2018-02-05", "2018-02-05", "2018-02-06")
        assert DateService.is_between("2018-02-06", "2018-02-05", "2018-02-06")
        assert DateService.is_between("2018-02-06", "2018-02-05", "2018-02-07")

    """
    range_day
    """

    def test_range_day_with_end_before_start_raise_runtime_error(self):
        with pytest.raises(RuntimeError):
            DateService.range_day("2018-03-05", "2018-02-07")

    def test_range_day_with_success_return_list(self):
        days = DateService.range_day("2018-02-05", "2018-02-07")
        self.assert_equals_resultset([DateService.to_mysql_date(d) for d in days])

    def test_range_day_with_only_week_end_return_list(self):
        days = DateService.range_day("2019-04-04", "2019-04-09", only_week_end=True)
        self.assert_equals_resultset([DateService.to_mysql_date(d) for d in days])

    """
    range_month
    """

    def test_range_month_with_end_before_start_raise_runtime_error(self):
        with pytest.raises(RuntimeError):
            DateService.range_month("2018-04-05", "2018-02-07")

    def test_range_month_with_success_return_list(self):
        months = DateService.range_month("2018-02-05", "2018-04-05")
        self.assert_equals_resultset([DateService.to_mysql_date(m) for m in months])

    """
    range_year
    """

    def test_range_year_with_end_before_start_raise_runtime_error(self):
        with pytest.raises(RuntimeError):
            DateService.range_year("2019-04-05", "2018-02-07")

    def test_range_year_with_success_return_list(self):
        years = DateService.range_year("2018-02-05", "2019-04-05")
        self.assert_equals_resultset([DateService.to_mysql_date(y) for y in years])

    """
    is_week_end
    """

    def test_is_week_end_with_date_outside_week_end_return_false(self):
        """Ensure date outside week end return False"""
        assert not DateService.is_week_end("2019-04-30")

    def test_is_week_end_with_date_inside_week_end_return_true(self):
        """Ensure date outside week end return False"""
        assert DateService.is_week_end("2019-04-27")
        assert DateService.is_week_end("2019-04-28")

        with date_test_helper.today_is("2019-04-28"):
            assert DateService.is_week_end()

    """
    add_days
    """

    def test_add_days_with_success_return_date(self):
        """Ensure adding nb days to a date succeed"""
        assert "2019-05-13" == DateService.add_days("2019-04-29", 14).format(
            "YYYY-MM-DD"
        )

    def test_add_days_with_excluding_we_return_date(self):
        """Ensure adding nb days to a date succeed"""
        assert "2019-05-17" == DateService.add_days(
            "2019-04-29", 14, exclude_we=True
        ).format("YYYY-MM-DD")

    """
    nb_days
    """

    def test_nb_days_with_success_return_int(self):
        """Ensure nb days succeed"""
        assert 5 == DateService.nb_days("2019-03-01", "2019-03-06")
        assert -3 == DateService.nb_days("2019-03-09", "2019-03-06")

    def test_nb_days_with_we_excluded_return_int(self):
        """Ensure nb days succeed"""
        assert 4 == DateService.nb_days("2019-03-01", "2019-03-06", True)
        assert -6 == DateService.nb_days("2019-03-11", "2019-03-04", True)

    """
    nb_years
    """

    def test_nb_years_with_success_return_int(self):
        """Ensure nb years succeed"""
        assert 4 == DateService.nb_years("2015-03-01", "2019-03-06")
        assert -3 == DateService.nb_years("2022-03-09", "2019-03-06")

    """
    shift
    """

    def test_shift_with_success_return_arrow(self):
        """Ensure shift succeed"""
        self.assert_equals_resultset(DateService.shift("2015-03-01", {"days": 4}))

    def test_shift_with_multiple_params_return_arrow(self):
        """Ensure shift succeed with multiple params"""
        self.assert_equals_resultset(
            DateService.shift("2015-03-01", {"days": 3, "months": 2})
        )

    def test_shift_with_bad_params_return_error(self):
        """Ensure shift fails with bad params"""
        with pytest.raises(ValueError) as e_info:
            DateService.shift("2015-03-01", {"year": 3, "months": 2})
        self.assert_equals_resultset(e_info)

    """
    to_str
    """

    def test_to_str_with_success_return_date_str(self):
        expected = "18 March 2019 11:16:34"

        with date_test_helper.today_is("2019-03-18T11:16:34.786+01:00"):
            assert DateService.to_str(date_format="DD MMMM YYYY HH:mm:ss") == expected

    def test_to_str_with_locale_return_date_str(self):
        DateService.set_locale("fr-fr")

        expected = "18 mars 2019 11:16:34"

        with date_test_helper.today_is("2019-03-18T11:16:34.786+01:00"):
            assert DateService.to_str(date_format="DD MMMM YYYY HH:mm:ss") == expected

    def test_to_str_with_locale_and_timezone_return_date_str(self):
        DateService.set_timezone("Europe/Paris")
        DateService.set_locale("fr-fr")

        expected = "19 mars 2019 00:18:36"

        with date_test_helper.today_is("2019-03-18 23:18:36.224469"):
            assert DateService.to_str(date_format="DD MMMM YYYY HH:mm:ss") == expected
