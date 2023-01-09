import unittest
from unittest.mock import Mock, patch
from datetime import datetime

from ms_imputedhours_core.office import get_real_office_name


class TestSuite(unittest.TestCase): 
    def test_get_real_office_name_return_same_param_when_office_name_is_not_mapped(self):
        expected_result = 'Valencia'
        office_name = 'Valencia'
        
        result = get_real_office_name(office_name)

        self.assertEqual(result, expected_result)
  
    def test_get_real_office_name_return_real_office_name_when_is_mapped(self):
        expected_result = 'Madrid - Ingeniería'
        office_name = 'Madrid - Ing'
        
        result = get_real_office_name(office_name)

        self.assertEqual(result, expected_result)
  