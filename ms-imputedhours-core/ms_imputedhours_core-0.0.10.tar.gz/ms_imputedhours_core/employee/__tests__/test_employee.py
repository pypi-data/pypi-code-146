import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from freezegun import freeze_time

from ms_imputedhours_core.employee import get_real_fte, calculate_real_capacity


DEFAULT_AGREEMENT_HOURS = {
    'totalHours': 150.0, 
    'days': {
        1: '0', 
        2: '8', 
        3: '8', 
        4: '5.5', 
        5: '0', 
        6: '0',
        7: '8', 
        8: '8', 
        9: '0', 
        10: '8', 
        11: '5.5', 
        12: '0',
        13: '0', 
        14: '8',
        15: '8',
        16: '8',
        17: '8', 
        18: '5.5',
        19: '0',
        20: '0', 
        21: '8', 
        22: '8', 
        23: '8', 
        24: '8',
        25: '5.5',
        26: '0', 
        27: '0', 
        28: '8',
        29: '8', 
        30: '8'
    }
}

class TestSuite(unittest.TestCase): 
    @freeze_time("2022-11-11")
    def test_get_real_fte_returns_successfactor_fte_when_date_is_not_future(self):
        expected_result = 1.0 ## 1.0 === 100%
        successfactor_data = {'FTE': 100}
        employeeFTE = {'fte': 50}
        date = Mock()
        date.year = 2021
        date.month = 10
        
        result = get_real_fte(successfactor_data, employeeFTE, date)

        self.assertEqual(result, expected_result)
    
    @freeze_time("2021-11-11")
    def test_get_real_fte_returns_employee_fte_when_date_is_for_future(self):
        expected_result = 0.5 # 50%
        successfactor_data = {'FTE': 100}
        employeeFTE = {'fte': 50}
        date = Mock()
        date.year = 2022
        date.month = 10
        
        result = get_real_fte(successfactor_data, employeeFTE, date)

        self.assertEqual(result, expected_result)

    @freeze_time("2022-11-11")
    def test_calculate_real_capacity_return_full_capacity_when_is_normal_month(self):
        """ 
        A normal month is a definition for a month where the employee 
        will work 100% of the hours of his agreement, and does not 
        coincide with any special date as the end or start 
        of the employment contract.
        """
        expected_result = 150.0
        hiring_date = datetime.strptime('17/09/2021', '%d/%m/%Y')
        end_date = None
        date = datetime.strptime('01/01/2022', '%d/%m/%Y')
        to_date = datetime.strptime('31/01/2022', '%d/%m/%Y')
        fte = 1.0 # 100%
        calculate_range = False
        
        result = calculate_real_capacity(DEFAULT_AGREEMENT_HOURS, hiring_date, end_date, date, to_date, fte, calculate_range)

        self.assertEqual(result, expected_result)

    @freeze_time("2022-11-11")
    def test_calculate_real_capacity_return_half_capacity_when_is_normal_month_and_fte_zero_point_five(self):
        """ 
        A normal month is a definition for a month where the employee 
        will work 100% of the hours of his agreement, and does not 
        coincide with any special date as the end or start 
        of the employment contract.
        """
        expected_result = 75.0
        hiring_date = datetime.strptime('17/09/2021', '%d/%m/%Y')
        end_date = None
        date = datetime.strptime('01/01/2022', '%d/%m/%Y')
        to_date = datetime.strptime('31/01/2022', '%d/%m/%Y')
        fte = 0.5 # 50%
        calculate_range = False
        
        result = calculate_real_capacity(DEFAULT_AGREEMENT_HOURS, hiring_date, end_date, date, to_date, fte, calculate_range)

        self.assertEqual(result, expected_result)

    @freeze_time("2022-11-11")
    def test_calculate_real_capacity_return_zero_when_date_is_before_hired(self):
        """ 
        A normal month is a definition for a month where the employee 
        will work 100% of the hours of his agreement, and does not 
        coincide with any special date as the end or start 
        of the employment contract.
        """
        expected_result = 0.0
        hiring_date = datetime.strptime('01/02/2022', '%d/%m/%Y')
        end_date = None
        date = datetime.strptime('01/01/2022', '%d/%m/%Y')
        to_date = datetime.strptime('31/01/2022', '%d/%m/%Y')
        fte = 0.5 # 50%
        calculate_range = False
        
        result = calculate_real_capacity(DEFAULT_AGREEMENT_HOURS, hiring_date, end_date, date, to_date, fte, calculate_range)

        self.assertEqual(result, expected_result)

    @freeze_time("2022-11-11")
    def test_calculate_real_capacity_return_only_work_days_when_employee_has_end_date(self):
        """ 
        A normal month is a definition for a month where the employee 
        will work 100% of the hours of his agreement, and does not 
        coincide with any special date as the end or start 
        of the employment contract.
        """
        expected_result = 33.5
        hiring_date = datetime.strptime('01/02/2021', '%d/%m/%Y')
        end_date = datetime.strptime('15/01/2022', '%d/%m/%Y')
        date = datetime.strptime('01/01/2022', '%d/%m/%Y')
        to_date = datetime.strptime('31/01/2022', '%d/%m/%Y')
        fte = 0.5 # 50%
        calculate_range = False
        
        result = calculate_real_capacity(DEFAULT_AGREEMENT_HOURS, hiring_date, end_date, date, to_date, fte, calculate_range)

        self.assertEqual(result, expected_result)
