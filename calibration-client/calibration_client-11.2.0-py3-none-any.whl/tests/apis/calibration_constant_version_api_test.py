"""CalibrationConstantVersionApiTest class"""

import unittest
from http import HTTPStatus

import pytest
from dateutil.parser import parse as parse_dt

from .api_base import ApiBase
from ..common import generators
from ..common.config_test import *


@pytest.mark.usefixtures('client_cls')
class CalibrationConstantVersionApiTest(ApiBase, unittest.TestCase):
    __unique_name = generators.generate_unique_name('CCVersionApi')
    __unique_file_name = generators.generate_unique_file_name()
    __begin_at = generators.generate_timestamp_str(0)

    __calibration_constant_version_01 = {
        'calibration_constant_version': {
            'name': __unique_name,
            'file_name': __unique_file_name,
            'path_to_file': 'path_to_file_1',
            'data_set_name': 'data_set_name_1',
            'calibration_constant_id': -3,
            'physical_detector_unit_id': -1,
            'flg_deployed': True,
            'flg_good_quality': True,
            'begin_validity_at': '2014-05-25T08:30:00.000+02:00',
            'end_validity_at': '2025-12-25T08:30:00.000+01:00',
            'begin_at': __begin_at,
            'start_idx': 1,
            'end_idx': 2,
            'raw_data_location': 'XFEL/metadata/',
            'description': 'desc version 01'
        }
    }

    def test_create_calibration_constant_version_api(self):
        ccv = self.__calibration_constant_version_01
        expect = ccv['calibration_constant_version']

        # Create new entry (should succeed)
        received = self.__create_entry_api(ccv, expect)

        ccv_id = received['id']
        ccv_name = received['name']

        # Create duplicated entry (should throw an error)
        self.__create_error_entry_uk_api(ccv)

        # event_at == expected_hash['begin_at']
        # This is necessary, because the CalibrationConstantVersionApi.begin_at
        # current_DATETIME + Random(60 seconds) is part of the Unique Key that
        # identifies uniquely a Calibration Constant Version entry
        self.__test_get_version_int(expect['begin_at'],
                                    expect_ccv_id=ccv_id)

        # Get entry by name
        self.__get_all_entries_by_name_api(ccv_name, expect)

        # Get entry by ID
        self.__get_entry_by_id_api(ccv_id, expect)

        # Put entry information (update some fields should succeed)
        self.__update_entry_api(ccv_id, expect)

    def fields_validation(self, receive, expect):
        assert receive['name'] == expect['name']
        assert receive['file_name'] == expect['file_name']
        assert receive['path_to_file'] == expect['path_to_file']
        assert receive['data_set_name'] == expect['data_set_name']
        assert receive['flg_deployed'] == expect['flg_deployed']
        assert receive['flg_good_quality'] == expect['flg_good_quality']
        assert parse_dt(receive['begin_at']) == parse_dt(expect['begin_at'])
        assert parse_dt(receive['begin_validity_at']) \
               == parse_dt(expect['begin_validity_at'])
        assert parse_dt(receive['end_validity_at']) \
               == parse_dt(expect['end_validity_at'])

        receive_cc_id = receive['calibration_constant']['id']
        assert receive_cc_id == expect['calibration_constant_id']

        receive_cc_id = receive[PHYSICAL_DETECTOR_UNIT]['id']
        assert receive_cc_id == expect['physical_detector_unit_id']

    def __create_entry_api(self, entry_info, expect):
        response = self.cal_client.create_calibration_constant_version_api(
            entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __create_error_entry_uk_api(self, entry_info):
        response = self.cal_client.create_calibration_constant_version_api(
            entry_info)
        receive = self.load_response_content(response)

        expect = {'info': {'name': ['has already been taken'],
                           'calibration_constant_id': [
                               'has already been taken'
                           ],
                           'physical_detector_unit_id': [
                               'has already been taken'],
                           'begin_at': ['has already been taken']}}

        assert receive == expect
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def __test_get_version_int(self, event_at, expect_ccv_id=None):
        ccv = self.__calibration_constant_version_01
        expect = ccv['calibration_constant_version']

        calibration_constant_id = expect['calibration_constant_id']
        physical_detector_unit_id = expect['physical_detector_unit_id']
        # event_at = '' #'2014-10-13T09:13:26.000+02:00'
        snapshot_at = ''

        resp = self.cal_client.get_calibration_constant_version_by_uk_api(
            calibration_constant_id, physical_detector_unit_id, event_at,
            snapshot_at)
        receive = self.load_response_content(resp)

        self.fields_validation(receive, expect)
        assert resp.status_code == HTTPStatus.OK

        if expect_ccv_id is not None:
            assert receive['id'] == expect_ccv_id

    def __get_all_entries_by_name_api(self, name, expect, page=DEF_PAGE,
                                      page_size=DEF_PAGE_SIZE):
        resp = self.cal_client. \
            get_all_calibration_constant_versions_by_name_api(name, page, page_size)

        receive = self.get_and_validate_all_entries_by_name(resp)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        resp = self.cal_client.get_calibration_constant_version_by_id_api(
            entry_id)
        receive = self.get_and_validate_entry_by_id(resp)
        self.fields_validation(receive, expect)

    def __update_entry_api(self, entry_id, expect):
        __unique_name = generators.generate_unique_name('CCVersionApiUpd')
        __unique_file_name = generators.generate_unique_file_name()
        __begin_at = generators.generate_timestamp_str(1)
        ccv_upd = {
            'calibration_constant_version': {
                'name': __unique_name,
                'file_name': __unique_file_name,
                'path_to_file': 'path_to_file_2',
                'data_set_name': 'data_set_name_2',
                # 'calibration_constant_id': '-1',
                # 'physical_detector_unit_id': '-1',
                'flg_deployed': False,
                'flg_good_quality': False,
                'begin_validity_at': '2014-05-25T08:31:00.000+02:00',
                'end_validity_at': '2025-12-25T08:31:00.000+01:00',
                'begin_at': __begin_at,
                'start_idx': 10,
                'end_idx': 20,
                'raw_data_location': 'XFEL/metadata_bck/',
                'description': 'desc version 01 UPDATED!'
            }
        }

        response = self.cal_client.update_calibration_constant_version_api(
            entry_id,
            ccv_upd)

        receive = self.load_response_content(response)

        # Add parameters not send to the update API
        expect_upd = ccv_upd['calibration_constant_version']
        expect_upd['calibration_constant_id'] = -3
        expect_upd['physical_detector_unit_id'] = -1

        self.fields_validation(receive, expect_upd)
        assert response.status_code == HTTPStatus.OK

        assert expect['name'] != expect_upd['name']
        assert expect['file_name'] != expect_upd['file_name']
        assert expect['path_to_file'] != expect_upd['path_to_file']
        assert expect['data_set_name'] != expect_upd['data_set_name']
        assert expect['flg_deployed'] != expect_upd['flg_deployed']
        assert expect['flg_good_quality'] != expect_upd['flg_good_quality']
        assert expect['begin_validity_at'] != expect_upd['begin_validity_at']
        assert expect['end_validity_at'] != expect_upd['end_validity_at']
        assert expect['begin_at'] != expect_upd['begin_at']
        assert expect['start_idx'] != expect_upd['start_idx']
        assert expect['end_idx'] != expect_upd['end_idx']
        assert expect['raw_data_location'] != expect_upd['raw_data_location']
        assert expect['description'] != expect_upd['description']


if __name__ == '__main__':
    unittest.main()
