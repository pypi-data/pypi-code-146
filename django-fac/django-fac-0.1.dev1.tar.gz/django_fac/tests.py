from django.test import TestCase
from .core.utils import format_expiry_date
# Create your tests here.

class FacUnitTest(TestCase):
    def test_health(self):
        # self.assertEqual(expected, total)
        pass


class UtilsTest(TestCase):

    def test_correctly_formatting_expiry_date(self):
        date = '09/45'
        expected = '4509'
        formatted_date = format_expiry_date(date)

        self.assertEqual(expected, formatted_date)

    def test_incorrect_expiry_date_data_type_as_parameter(self):
        date = '21/09/2045'
        result = False
        try:
            format_expiry_date(date)
        except ValueError:
            result = True

        self.assertEqual(True, result)

    def test_incorrectly_formatted_expiry_date_as_parameter(self):
        result = False
        try:
            format_expiry_date(234)
        except ValueError:
            result = True

        self.assertEqual(True, result)