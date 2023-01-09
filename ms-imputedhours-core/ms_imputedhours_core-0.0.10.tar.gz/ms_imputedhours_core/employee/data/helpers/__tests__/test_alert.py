import unittest
from unittest.mock import patch
from datetime import datetime

from ms_imputedhours_core.employee.data.helpers.alert import should_exclude_employee


class TestSuite(unittest.TestCase):
    def test_should_exclude_employee_should_return_false_when_employee_hired_date_is_lower_than_date(self):
        date = datetime.strptime('02/28/22 00:00:00', '%m/%d/%y %H:%M:%S')
        hired_date = datetime.strptime(
            '01/01/22 00:00:00', '%m/%d/%y %H:%M:%S')
        end_date = None
        expected_result = False

        is_exclude_employee = should_exclude_employee(
            email='test@test.com',
            date=date,
            hired_date=hired_date,
            end_date=end_date,
        )

        self.assertEqual(is_exclude_employee, expected_result)

    def test_should_exclude_employee_should_return_true_when_employee_hired_date_is_greater_than_date(self):
        date = datetime.strptime('02/28/22 00:00:00', '%m/%d/%y %H:%M:%S')
        hired_date = datetime.strptime(
            '05/01/22 00:00:00', '%m/%d/%y %H:%M:%S')
        end_date = None
        expected_result = True

        is_exclude_employee = should_exclude_employee(
            email='test@test.com',
            date=date,
            hired_date=hired_date,
            end_date=end_date,
        )

        self.assertEqual(is_exclude_employee, expected_result)

    def test_should_exclude_employee_should_return_false_when_employee_end_date_is_greater_than_date(self):
        date = datetime.strptime('02/28/22 00:00:00', '%m/%d/%y %H:%M:%S')
        hired_date = datetime.strptime(
            '01/01/21 00:00:00', '%m/%d/%y %H:%M:%S')
        end_date = datetime.strptime('05/15/22 00:00:00', '%m/%d/%y %H:%M:%S')
        expected_result = False

        is_exclude_employee = should_exclude_employee(
            email='test@test.com',
            date=date,
            hired_date=hired_date,
            end_date=end_date,
        )

        self.assertEqual(is_exclude_employee, expected_result)

    def test_should_exclude_employee_should_return_true_when_employee_end_date_is_lower_than_date(self):
        date = datetime.strptime('02/28/22 00:00:00', '%m/%d/%y %H:%M:%S')
        hired_date = datetime.strptime(
            '01/01/21 00:00:00', '%m/%d/%y %H:%M:%S')
        end_date = datetime.strptime('01/15/22 00:00:00', '%m/%d/%y %H:%M:%S')
        expected_result = True

        is_exclude_employee = should_exclude_employee(
            email='test@test.com',
            date=date,
            hired_date=hired_date,
            end_date=end_date,
        )

        self.assertEqual(is_exclude_employee, expected_result)

    @patch('ms_imputedhours_core.employee.data.helpers.alert.EXCLUDE_ALERT_EMAILS', ['test@test.com'])
    def test_should_exclude_employee_should_return_true_when_employee_email_is_excluded(self):
        date = datetime.strptime('02/28/22 00:00:00', '%m/%d/%y %H:%M:%S')
        hired_date = datetime.strptime(
            '01/01/22 00:00:00', '%m/%d/%y %H:%M:%S')
        end_date = None
        expected_result = True
        
        from ..alert import should_exclude_employee

        is_exclude_employee = should_exclude_employee(
            email='jonathan.rodriguez@makingscience.com',
            date=date,
            hired_date=hired_date,
            end_date=end_date,
        )

        self.assertEqual(is_exclude_employee, expected_result)
