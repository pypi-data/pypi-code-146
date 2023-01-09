import unittest
import datetime
from unittest.mock import patch

from ..dates import get_first_day, get_last_day


class TestSuite(unittest.TestCase):
    def test_get_first_day_should_return_first_date_from_a_date(self):
        year = 2022
        month = 2
        day = 28
        date = datetime.date(year, month, day)
        expected_result = datetime.date(year, month, 1)

        first_date = get_first_day(date=date)

        self.assertEqual(first_date, expected_result)

    def test_get_last_day_should_return_last_date_from_a_date(self):
        year = 2022
        month = 2
        day = 10
        date = datetime.date(year, month, day)
        expected_result = datetime.date(year, month, 28)

        last_day = get_last_day(date=date)

        self.assertEqual(last_day, expected_result)
