"""CalibrationApiTest class"""

import unittest
from http import HTTPStatus

import pytest

from .api_base import ApiBase
from ..common.generators import generate_unique_name
from ..common.config_test import *


@pytest.mark.usefixtures('client_cls')
class CalibrationApiTest(ApiBase, unittest.TestCase):
    def test_create_calibration_api(self):
        __unique_name = generate_unique_name('CalibrationApi')
        calibration = {
            'calibration': {
                'name': __unique_name,
                'unit_id': -1,
                'max_value': 10.0,
                'min_value': 1.0,
                'allowed_deviation': 0.1,
                'description': 'desc 01'
            }
        }

        expect = calibration['calibration']

        #
        # Create new entry (should succeed)
        #
        received = self.__create_entry_api(calibration, expect)

        calibration_id = received['id']
        calibration_name = received['name']

        try:
            # Create duplicated entry (should throw an error)
            self.__create_error_entry_uk_api(calibration)

            # Get entry by name
            self.__get_all_entries_by_name_api(calibration_name, expect)

            # Get entry by ID
            self.__get_entry_by_id_api(calibration_id, expect)

            # Put entry information (update some fields should succeed)
            self.__update_entry_api(calibration_id, expect)

        finally:
            # Delete entry (should succeed)
            # (test purposes only to keep the DB clean)
            del_resp = self.cal_client.delete_calibration_api(calibration_id)

        # Validate the response from deletion if nothing already error-ed
        self.get_and_validate_delete_entry_by_id(del_resp)

    def fields_validation(self, receive, expect):
        assert receive['name'] == expect['name']
        assert receive['unit_id'] == expect['unit_id']
        assert receive['max_value'] == expect['max_value']
        assert receive['min_value'] == expect['min_value']
        assert receive['allowed_deviation'] == expect['allowed_deviation']
        assert receive['description'] == expect['description']

    #
    # Internal private APIs methods
    #
    def __create_entry_api(self, entry_info, expect):
        response = self.cal_client.create_calibration_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __create_error_entry_uk_api(self, entry_info):
        response = self.cal_client.create_calibration_api(entry_info)
        receive = self.load_response_content(response)

        expect = {'info': {'name': ['has already been taken'],
                           'unit': ['has already been taken']}}

        assert receive == expect
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def __update_entry_api(self, entry_id, expect):
        unique_name = generate_unique_name('CalibrationApiUpd')
        calibration_upd = {
            'calibration': {
                'name': expect['name'],
                # 'unit_id': '-1',
                'max_value': 12.0,
                'min_value': 3.0,
                'allowed_deviation': 0.5,
                'description': 'desc 01 updated!'
            }
        }

        resp = self.cal_client.update_calibration_api(entry_id,
                                                      calibration_upd)
        receive = self.load_response_content(resp)

        # Add parameters not send to the update API
        calibration_upd['calibration']['unit_id'] = -1
        expect_upd = calibration_upd['calibration']

        self.fields_validation(receive, expect_upd)
        assert resp.status_code == HTTPStatus.OK

        assert expect['max_value'] != expect_upd['max_value']
        assert expect['min_value'] != expect_upd['min_value']
        assert expect['allowed_deviation'] != expect_upd['allowed_deviation']
        assert expect['description'] != expect_upd['description']

    def __get_all_entries_by_name_api(self, name, expect,
                                      page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        response = self.cal_client.get_all_calibrations_by_name_api(name, page, page_size)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.cal_client.get_calibration_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)


if __name__ == '__main__':
    unittest.main()
