"""CalibrationConstantApiTest class"""

import unittest
from http import HTTPStatus

import pytest

from .api_base import ApiBase
from ..common.generators import generate_unique_name
from ..common.config_test import *


@pytest.mark.usefixtures('client_cls')
class CalibrationConstantApiTest(ApiBase, unittest.TestCase):
    db_cal_const1 = {
        'calibration_constant': {
            'name': 'CALIBRATION_CONSTANT_TEST-1_DO_NOT_DELETE',
            'calibration_id': -1,
            'detector_type_id': -1,
            'condition_id': -1,
            'description': 'Created automatically via seed:seed_tests'
        }
    }
    db_cal_const2 = {
        'calibration_constant': {
            'name': 'CALIBRATION_CONSTANT_TEST-2_DO_NOT_DELETE',
            'calibration_id': -1,
            'detector_type_id': -1,
            'condition_id': -2,
            'description': 'Created automatically via seed:seed_tests'
        }
    }

    def test_create_calibration_constant_api(self):
        __unique_name = generate_unique_name('CConstantApi')
        calibration_const = {
            'calibration_constant': {
                'name': __unique_name,
                'calibration_id': -2,
                'detector_type_id': -1,
                'condition_id': -1,
                'flg_auto_approve': True,
                'flg_available': True,
                'description': 'desc 01'
            }
        }

        expect = calibration_const['calibration_constant']

        expect_db_all = [self.db_cal_const1['calibration_constant'],
                         self.db_cal_const2['calibration_constant']]

        # Create new entry (should succeed)
        create_entry_resp = self.cal_client.create_calibration_constant_api(
            calibration_const)

        create_entry_received = self.get_and_validate_create_entry(
            create_entry_resp)

        cal_constant_id = create_entry_received['id']
        cal_constant_name = create_entry_received['name']

        try:
            # Check that expected creation result was received
            self.fields_validation(create_entry_received, expect)

            # Create duplicated entry (should throw an error)
            self.__create_error_entry_uk_api(calibration_const)

            # Get entry by all calibration constants (should succeed)
            condition_ids = [
                self.db_cal_const1['calibration_constant']['condition_id'],
                self.db_cal_const2['calibration_constant']['condition_id']]

            self.__get_all_calibration_constants_by_conditions_api(
                self.db_cal_const1['calibration_constant']['calibration_id'],
                self.db_cal_const1['calibration_constant']['detector_type_id'],
                condition_ids,
                expect_db_all)

            # Get entry by it's Unique Key (UK) (should succeed)
            self.__get_entry_by_uk_api(calibration_const, expect)

            # Get entry by it's Unique Key (UK) (should not_found)
            self.__get_entry_by_uk_api_not_found_api()

            # Get entry by name
            self.__get_all_entries_by_name_api(cal_constant_name, expect)

            # Get entry by ID
            self.__get_entry_by_id_api(cal_constant_id, expect)

            # Put entry information (update some fields should succeed)
            self.__update_entry_api(cal_constant_id, expect)

        finally:
            # Delete entry (should succeed)
            # (test purposes only to keep the DB clean)
            del_resp = self.cal_client.delete_calibration_constant_api(
                cal_constant_id
            )

        # Validate the response from deletion if nothing already error-ed
        self.get_and_validate_delete_entry_by_id(del_resp)

    def fields_validation(self, receive, expect):
        assert receive['name'] == expect['name']
        assert receive['detector_type_id'] == expect['detector_type_id']
        assert receive['calibration_id'] == expect['calibration_id']
        assert receive['condition_id'] == expect['condition_id']
        assert receive['flg_auto_approve'] == expect['flg_auto_approve']
        assert receive['flg_available'] == expect['flg_available']
        assert receive['description'] == expect['description']

    def __create_error_entry_uk_api(self, entry_info):
        response = self.cal_client.create_calibration_constant_api(
            entry_info)
        receive = self.load_response_content(response)

        expect = {
            'info': {
                'name': ['has already been taken'],
                'detector_type': ['has already been taken'],
                'calibration': ['has already been taken'],
                'condition': ['has already been taken']
            }
        }

        assert receive == expect
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def __update_entry_api(self, entry_id, expect):
        unique_name = generate_unique_name('CConstantApiUpd')
        calibration_const_upd = {
            'calibration_constant': {
                'name': unique_name,
                # 'calibration_id': '-2',
                # 'detector_type_id': '-1',
                # 'condition_id': '-1',
                'flg_auto_approve': False,
                'flg_available': False,
                'description': 'desc 01 updated!'
            }
        }

        resp = self.cal_client.update_calibration_constant_api(
            entry_id,
            calibration_const_upd
        )

        receive = self.load_response_content(resp)

        # Add parameters not send to the update API
        calibration_const_upd['calibration_constant']['calibration_id'] = -2
        calibration_const_upd['calibration_constant']['detector_type_id'] = -1
        calibration_const_upd['calibration_constant']['condition_id'] = -1
        expect_upd = calibration_const_upd['calibration_constant']

        self.fields_validation(receive, expect_upd)
        assert resp.status_code == HTTPStatus.OK

        assert expect['name'] != expect_upd['name']
        assert expect['flg_auto_approve'] != expect_upd['flg_auto_approve']
        assert expect['flg_available'] != expect_upd['flg_available']
        assert expect['description'] != expect_upd['description']

    def __get_all_entries_by_name_api(self, name, expect,
                                      page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        resp = self.cal_client.get_all_calibration_constants_by_name_api(
            name, page, page_size
        )

        receive = self.get_and_validate_all_entries_by_name(resp)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        resp = self.cal_client.get_calibration_constant_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(resp)
        self.fields_validation(receive, expect)

    def __get_entry_by_uk_api(self, entry, expect):
        resp = self.cal_client.get_calibration_constant_by_uk_api(
            entry['calibration_constant']['calibration_id'],
            entry['calibration_constant']['detector_type_id'],
            entry['calibration_constant']['condition_id'])

        receive = self.load_response_content(resp)

        self.fields_validation(receive, expect)
        assert resp.status_code == HTTPStatus.OK

    def __get_entry_by_uk_api_not_found_api(self):
        calibration_id = -99
        dev_type_id = -99
        cond_id = -99

        resp = self.cal_client.get_calibration_constant_by_uk_api(
            calibration_id,
            dev_type_id,
            cond_id
        )

        self.get_and_validate_resource_not_found(resp)

    def __get_all_calibration_constants_by_conditions_api(self,
                                                          calibration_id,
                                                          detector_type_id,
                                                          condition_ids,
                                                          expect):
        resp = self.cal_client.get_all_calibration_constants_by_conds_api(
            calibration_id, detector_type_id, condition_ids)

        receive = self.load_response_content(resp)

        assert [c['name'] for c in receive] == [
            self.db_cal_const2['calibration_constant']['name'],
            self.db_cal_const1['calibration_constant']['name'],
        ]

        assert resp.status_code == HTTPStatus.OK


if __name__ == '__main__':
    unittest.main()
