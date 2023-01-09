import unittest
from unittest.mock import Mock, patch
from datetime import datetime


class TestSuite(unittest.TestCase):
    def _create_GSheet_mock():
        service_mock = Mock()
        
        read_gsheet_mock = Mock()
        read_gsheet_mock.read_gsheet.return_value = {'values': [
            ['10/09/2022', '0'],
            ['11/09/2022', '0'],
            ['12/09/2022', '8'],
            ['13/09/2022', '8'],
            ['14/09/2022', '8'],
            ['15/09/2022', '8'],
            ['16/09/2022', '5.5'],
            ['17/09/2022', '0'],
            ['18/09/2022', '0'],
            ['19/09/2022', '8'],
        ]}
        read_gsheet_mock.get_sheetnames.return_value = {'sheets': [
            { 
                'properties': {
                    'title': 'Summary'
                }
            },
             { 
                'properties': {
                    'title': 'Sheet 1'
                }
            },
              { 
                'properties': {
                    'title': 'Sheet 2'
                }
            }
        ]}
        service_mock.return_value = read_gsheet_mock
        return service_mock

    @patch('ms_imputedhours_core.agreements.GSheet', new=_create_GSheet_mock())
    def test_read_gsheet_should_call_google_api_with_credentials_and_correct_params(self):
        expected_result = {'totalHours': 45.5, 'days': {10: '0', 11: '0', 12: '8', 13: '8', 14: '8', 15: '8', 16: '5.5', 17: '0', 18: '0', 19: '8'}}
        spreadsheet_id = '111111'
        sheet_name = 'SHEET_NAME_TEST'
        month = 9
        year = 2022
        
        from ms_imputedhours_core.agreements import Agreements
        
        response = Agreements(spreadsheet_id).get_hours_by_month(month, year, sheet_name)

        self.assertEqual(response, expected_result)

    @patch('ms_imputedhours_core.agreements.GSheet', new=_create_GSheet_mock())
    def test_get_hours_by_range_return_agreement_hours_by_range(self):
        expected_result = {'days': {'12-9': '8', '13-9': '8', '14-9': '8', '15-9': '8', '16-9': '5.5', '17-9': '0'}, 'totalHours': 37.5}
        spreadsheet_id = '111111'
        from_date = datetime.strptime('12/09/2022', '%d/%m/%Y')
        to_date = datetime.strptime('17/09/2022', '%d/%m/%Y')
        sheet_name = 'SHEET_NAME_TEST'
        
        from ms_imputedhours_core.agreements import Agreements
        
        response = Agreements(spreadsheet_id).get_hours_by_range(from_date, to_date, sheet_name)

        self.assertEqual(response, expected_result)

    @patch('ms_imputedhours_core.agreements.GSheet', new=_create_GSheet_mock())
    def test_get_all_office_names_returns_all_sheet_names(self):
        expected_result = ['Sheet 1', 'Sheet 2']
        spreadsheet_id = '111111'
        
        from ms_imputedhours_core.agreements import Agreements
        
        response = Agreements(spreadsheet_id).get_all_office_names()

        self.assertEqual(response, expected_result)
