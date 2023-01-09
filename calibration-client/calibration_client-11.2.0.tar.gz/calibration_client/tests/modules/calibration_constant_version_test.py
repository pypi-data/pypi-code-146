"""CalibrationConstantVersionTest class"""

import unittest

import pytest
from dateutil.parser import parse as parse_dt

from .module_base import ModuleBase
from ..common import generators
from ..common.config_test import (
    CALIBRATION_CONSTANT_VERSION, PHYSICAL_DETECTOR_UNIT, RESOURCE_NOT_FOUND
)
from ...modules.calibration_constant_version import CalibrationConstantVersion

MODULE_NAME = CALIBRATION_CONSTANT_VERSION


@pytest.mark.usefixtures('client_cls')
class CalibrationConstantVersionTest(ModuleBase, unittest.TestCase):
    def setUp(self):
        __unique_name = generators.generate_unique_name('CCV_01')
        __unique_file_name = generators.generate_unique_file_name()
        __begin_at = generators.generate_timestamp_str(0)

        self.ccv_01 = {
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
            'report_id': '',
            'description': 'desc version 01'
        }

        __unique_name_upd = generators.generate_unique_name('CCVersionUpd01')
        __unique_file_name_upd = generators.generate_unique_file_name()
        __new_begin_at = -(60 * 60 * 24)  # Minus 1 day
        __begin_at_upd = generators.generate_timestamp_str(__new_begin_at)

        self.ccv_01_upd = {
            'name': __unique_name_upd,
            'file_name': __unique_file_name_upd,
            'path_to_file': 'path_to_file_1_upd',
            'data_set_name': 'data_set_name_1_upd',
            'calibration_constant_id': -3,
            'physical_detector_unit_id': -1,
            'flg_deployed': False,
            'flg_good_quality': False,
            'begin_validity_at': '2014-06-25T08:30:00.000+02:00',
            'end_validity_at': '2025-11-25T08:30:00.000+01:00',
            'begin_at': __begin_at_upd,
            'start_idx': 0,
            'end_idx': 1,
            'raw_data_location': 'XFEL/metadata/bck/',
            'report_id': '',
            'description': 'desc version 01 Updated!'
        }

        self.expected_db_01 = {
            'id': -1,
            'name': 'CALIBRATION_CONSTANT_VERSION_TEST-1_DO_NOT_DELETE',
            'file_name': 'cal.r0001.c0002.h5',
            'path_to_file': '/usr/local/cal_repo/',
            'data_set_name': 'exp001.cal001',
            'flg_deployed': True,
            'flg_good_quality': True,
            'begin_validity_at': '2014-05-20T10:30:14.000+02:00',
            'end_validity_at': '2029-06-24T00:00:00.000+02:00',
            'begin_at': '2014-05-20T12:00:00.000+02:00',
            'start_idx': None,
            'end_idx': None,
            'raw_data_location': None,
            'description': None,
            # 'calibration_constant': {
            #     'id': -1,
            #     'name': 'CALIBRATION_CONSTANT_TEST-1_DO_NOT_DELETE',
            #     'flg_auto_approve': True,
            #     'flg_available': True,
            #     'description': 'Created automatically via seed:seed_tests',
            #     'detector_type_id': -1,
            #     'calibration_id': -1,
            #     'condition_id': -1},
            'calibration_constant_id': -1,
            # 'physical_detector_unit': {
            #     'id': -1,
            #     'name': 'PHYSICAL_DETECTOR_UNIT-1_DO_NOT_DELETE',
            #     'detector_type_id': -1,
            #     'flg_available': True,
            #     'description': 'Created automatically via seed:seed_tests'}
            'physical_detector_unit_id': -1}

        self.expected_db_02 = {
            'id': -2,
            'name': 'CALIBRATION_CONSTANT_VERSION_TEST-2_DO_NOT_DELETE',
            'file_name': 'cal.r0001.c0002.h5',
            'path_to_file': '/usr/local/cal_repo/',
            'data_set_name': 'exp001.cal001',
            'flg_deployed': True,
            'flg_good_quality': True,
            'begin_validity_at': '2014-05-25T10:30:14.000+02:00',
            'end_validity_at': '2029-06-24T00:00:00.000+02:00',
            'begin_at': '2014-05-26T12:00:00.000+02:00',
            'start_idx': None,
            'end_idx': None,
            'raw_data_location': None,
            'description': 'Created automatically via seed:seed_tests',
            # 'calibration_constant': {
            #     'id': -1,
            #     'name': 'CALIBRATION_CONSTANT_TEST-1_DO_NOT_DELETE',
            #     'flg_auto_approve': True,
            #     'flg_available': True,
            #     'description': 'Created automatically via seed:seed_tests',
            #     'detector_type_id': -1,
            #     'calibration_id': -1,
            #     'condition_id': -1},
            'calibration_constant_id': -1,
            # 'physical_detector_unit': {
            #     'id': -1,
            #     'name': 'PHYSICAL_DETECTOR_UNIT-1_DO_NOT_DELETE',
            #     'detector_type_id': -1,
            #     'flg_available': True,
            #     'description': 'Created automatically via seed:seed_tests'}
            'physical_detector_unit_id': -1}

        self.expected_db_04 = {
            'id': -4,
            'name': 'CALIBRATION_CONSTANT_VERSION_TEST-4_DO_NOT_DELETE',
            'file_name': 'cal.r0001.c0002.h5',
            'path_to_file': '/usr/local/cal_repo/',
            'data_set_name': 'exp001.cal001',
            'flg_deployed': True,
            'flg_good_quality': True,
            'begin_validity_at': '2015-05-25T10:30:14.000+02:00',
            'end_validity_at': '2029-06-24T00:00:00.000+02:00',
            'begin_at': '2015-05-26T12:00:00.000+02:00',
            'start_idx': None,
            'end_idx': None,
            'raw_data_location': None,
            'description': 'Created automatically via seed:seed_tests',
            # 'calibration_constant': {
            #     'id': -2,
            #     'name': 'CALIBRATION_CONSTANT_TEST-2_DO_NOT_DELETE',
            #     'flg_auto_approve': True,
            #     'flg_available': True,
            #     'description': 'Created automatically via seed:seed_tests',
            #     'detector_type_id': -1,
            #     'calibration_id': -1,
            #     'condition_id': -2},
            'calibration_constant_id': -2,
            # 'physical_detector_unit': {
            #     'id': -1,
            #     'name': 'PHYSICAL_DETECTOR_UNIT-1_DO_NOT_DELETE',
            #     'detector_type_id': -1,
            #     'flg_available': True,
            #     'description': 'Created automatically via seed:seed_tests'}
            'physical_detector_unit_id': -1}

    def test_create_calibration_constant_version(self):
        __begin_at = generators.generate_timestamp_str(0)

        __new_begin_at = -(60 * 60 * 24)  # Minus 1 day
        __begin_at_upd = generators.generate_timestamp_str(__new_begin_at)

        ccv_01 = CalibrationConstantVersion(
            calibration_client=self.cal_client,
            name=self.ccv_01['name'],
            file_name=self.ccv_01['file_name'],
            path_to_file=self.ccv_01['path_to_file'],
            data_set_name=self.ccv_01['data_set_name'],
            calibration_constant_id=self.ccv_01['calibration_constant_id'],
            physical_detector_unit_id=self.ccv_01['physical_detector_unit_id'],
            flg_deployed=self.ccv_01['flg_deployed'],
            flg_good_quality=self.ccv_01['flg_good_quality'],
            begin_validity_at=self.ccv_01['begin_validity_at'],
            end_validity_at=self.ccv_01['end_validity_at'],
            begin_at=__begin_at,
            start_idx=self.ccv_01['start_idx'],
            end_idx=self.ccv_01['end_idx'],
            raw_data_location=self.ccv_01['raw_data_location'],
            report_id=self.ccv_01['report_id'],
            description=self.ccv_01['description']
        )

        #
        # Create new entry (should succeed)
        #
        result1 = ccv_01.create()
        self.assert_create_success(MODULE_NAME, result1, self.ccv_01)

        calibration_constant_vers = result1['data']
        ccv_id = calibration_constant_vers['id']
        ccv_name = calibration_constant_vers['name']
        ccv_cc_id = calibration_constant_vers['calibration_constant']['id']
        ccv_pd_id = calibration_constant_vers['physical_detector_unit']['id']

        #
        # Create duplicated entry (should throw an error)
        #
        ccv_01_dup = ccv_01
        result2 = ccv_01_dup.create()
        expect_app_info = {'name': ['has already been taken']}
        self.assert_create_error(MODULE_NAME, result2, expect_app_info)

        #
        # Get entry by name
        #
        result3 = CalibrationConstantVersion.get_by_name(self.cal_client,
                                                         ccv_name)
        self.assert_find_success(MODULE_NAME, result3, self.ccv_01)

        #
        # Get entry by ID
        #
        result4 = CalibrationConstantVersion.get_by_id(self.cal_client, ccv_id)
        self.assert_find_success(MODULE_NAME, result4, self.ccv_01)

        #
        # Get entry with non-existent ID (should throw an error)
        #
        ccv_id = -666
        result5 = CalibrationConstantVersion.get_by_id(self.cal_client, ccv_id)
        self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)

        #
        # Get entry by UK (should succeed)
        # (calibration_constant_id,
        #  physical_detector_unit_id,
        #  event_at,
        #  snapshot_at)
        #
        ccv_event_at = calibration_constant_vers['begin_at']
        ccv_snapshot_at = ''  # '' == Now()

        result_uk = CalibrationConstantVersion.get_by_uk(self.cal_client,
                                                         ccv_cc_id,
                                                         ccv_pd_id,
                                                         ccv_event_at,
                                                         ccv_snapshot_at)
        self.assert_find_success(MODULE_NAME, result_uk, self.ccv_01)

        #
        # Get entry by UK (should throw an error)
        # (calibration_constant_id,
        #  physical_detector_unit_id,
        #  event_at,
        #  snapshot_at)
        #
        calibration_constant_id = -666
        physical_detector_unit_id = -666
        ccv_event_at = ''  # '' == Now()
        ccv_snapshot_at = ''  # '' == Now()

        res_uk_error = CalibrationConstantVersion.get_by_uk(
            self.cal_client,
            calibration_constant_id,
            physical_detector_unit_id,
            ccv_event_at,
            ccv_snapshot_at
        )
        self.assert_find_error(MODULE_NAME, res_uk_error, RESOURCE_NOT_FOUND)

        #
        # Put entry information (update some fields should succeed)
        #
        ccv_01.name = self.ccv_01_upd['name']
        ccv_01.file_name = self.ccv_01_upd['file_name']
        ccv_01.path_to_file = self.ccv_01_upd['path_to_file']
        ccv_01.data_set_name = self.ccv_01_upd['data_set_name']
        ccv_01.flg_deployed = self.ccv_01_upd['flg_deployed']
        ccv_01.flg_good_quality = self.ccv_01_upd['flg_good_quality']
        ccv_01.begin_validity_at = self.ccv_01_upd['begin_validity_at']
        ccv_01.end_validity_at = self.ccv_01_upd['end_validity_at']
        ccv_01.begin_at = __begin_at_upd
        ccv_01.start_idx = self.ccv_01_upd['start_idx']
        ccv_01.end_idx = self.ccv_01_upd['end_idx']
        ccv_01.raw_data_location = self.ccv_01_upd['raw_data_location']
        ccv_01.description = self.ccv_01_upd['description']
        result6 = ccv_01.update()
        self.assert_update_success(MODULE_NAME, result6, self.ccv_01_upd)

        #
        # Put entry information (update some fields should throw an error)
        #
        ccv_01.name = '__THIS_NAME_IS_1_CHARACTERS_LONGER_THAN_THE_ALLOWED_MAX_NUM__'  # noqa
        result7 = ccv_01.update()
        expect_app_info = {'name': ['is too long (maximum is 60 characters)']}
        self.assert_update_error(MODULE_NAME, result7, expect_app_info)

        #
        # Delete entry (should succeed)
        # (test purposes only to keep the DB clean)
        #
        # result8 = ccv_01.delete()
        # self.assert_delete_success(MODULE_NAME, result8)

        #
        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        #
        # result9 = ccv_01.delete()
        # self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def test_create_calibration_constant_version_from_dict(self):
        #
        # Create new entry (should succeed)
        #
        result1 = CalibrationConstantVersion.create_from_dict(self.cal_client,
                                                              self.ccv_01)
        self.assert_create_success(MODULE_NAME, result1, self.ccv_01)

        calibration_constant_version = result1['data']
        ccv_id = calibration_constant_version['id']
        ccv_name = calibration_constant_version['name']

        #
        # Create duplicated entry (should throw an error)
        #
        result2 = CalibrationConstantVersion.create_from_dict(self.cal_client,
                                                              self.ccv_01)
        expect_app_info = {'name': ['has already been taken']}
        self.assert_create_error(MODULE_NAME, result2, expect_app_info)

        #
        # Get entry by name
        #
        result3 = CalibrationConstantVersion.get_by_name(self.cal_client,
                                                         ccv_name)
        self.assert_find_success(MODULE_NAME, result3, self.ccv_01)

        #
        # Get entry by ID
        #
        result4 = CalibrationConstantVersion.get_by_id(self.cal_client, ccv_id)
        self.assert_find_success(MODULE_NAME, result4, self.ccv_01)

    def test_calibration_constants_get_closest_version_now(self):
        #
        # Search for the closest version
        #
        calibration_constant_ids = [-1, -2]
        physical_detector_unit_id = -1
        event_at = None
        snapshot_at = None

        result1 = CalibrationConstantVersion.get_closest_by_time(
            self.cal_client, calibration_constant_ids,
            physical_detector_unit_id,
            event_at, snapshot_at)

        # result1 ==>
        # {'success': True,
        #  'info': 'Got calibration_constant_version successfully',
        #  'app_info': {},
        #  'data': {
        #       'id': -4,
        #       'name': 'CALIBRATION_CONSTANT_VERSION_TEST-4_DO_NOT_DELETE',
        #       'file_name': 'cal.r0001.c0002.h5',
        #       'path_to_file': '/usr/local/cal_repo/',
        #       'data_set_name': 'exp001.cal001',
        #       'flg_deployed': True,
        #       'flg_good_quality': True,
        #       'begin_validity_at': '2015-05-25T10:30:14.000+02:00',
        #       'end_validity_at': '2029-06-24T00:00:00.000+02:00',
        #       'begin_at': '2015-05-26T12:00:00.000+02:00',
        #       'start_idx': None,
        #       'end_idx': None,
        #       'raw_data_location': None,
        #       'description': None,
        #       'calibration_constant': {
        #           'id': -2,
        #           'name': 'CALIBRATION_CONSTANT_TEST-2_DO_NOT_DELETE',
        #           'flg_auto_approve': True,
        #           'flg_available': True,
        #           'description': 'Created automatically via seed:seed_tests',
        #           'detector_type_id': -1,
        #           'calibration_id': -1,
        #           'condition_id': -2},
        #       'physical_detector_unit': {
        #           'id': -1,
        #           'name': 'PHYSICAL_DETECTOR_UNIT-1_DO_NOT_DELETE',
        #           'detector_type_id': -1,
        #           'flg_available': True,
        #           'description': 'Created automatically via seed:seed_tests'}
        # }}

        self.assert_find_success(MODULE_NAME, result1, self.expected_db_04)

    def test_calibration_constants_get_closest_version_in_the_past(self):
        #
        # Search for the closest version
        #
        calibration_constant_ids = [-1, -2]
        physical_detector_unit_id = -1
        event_at = '2014-05-24T12:00:00.000+02:00'
        snapshot_at = None

        result1 = CalibrationConstantVersion.get_closest_by_time(
            self.cal_client, calibration_constant_ids,
            physical_detector_unit_id,
            event_at, snapshot_at)

        # result1 ==>
        # {'success': True,
        #  'info': 'Got calibration_constant_version successfully',
        #  'app_info': {},
        #  'data': {
        #       'id': -2,
        #       'name': 'CALIBRATION_CONSTANT_VERSION_TEST-2_DO_NOT_DELETE',
        #       'file_name': 'cal.r0001.c0002.h5',
        #       'path_to_file': '/usr/local/cal_repo/',
        #       'data_set_name': 'exp001.cal001',
        #       'flg_deployed': True,
        #       'flg_good_quality': True,
        #       'begin_validity_at': '2014-05-25T10:30:14.000+02:00',
        #       'end_validity_at': '2029-06-24T00:00:00.000+02:00',
        #       'begin_at': '2014-05-26T12:00:00.000+02:00',
        #       'start_idx': None,
        #       'end_idx': None,
        #       'raw_data_location': None,
        #       'description': None,
        #       'calibration_constant': {
        #           'id': -1,
        #           'name': 'CALIBRATION_CONSTANT_TEST-1_DO_NOT_DELETE',
        #           'flg_auto_approve': True,
        #           'flg_available': True,
        #           'description': 'Created automatically via seed:seed_tests',
        #           'detector_type_id': -1,
        #           'calibration_id': -1,
        #           'condition_id': -1},
        #       'physical_detector_unit': {
        #           'id': -1,
        #           'name': 'PHYSICAL_DETECTOR_UNIT-1_DO_NOT_DELETE',
        #           'detector_type_id': -1,
        #           'flg_available': True,
        #           'description': 'Created automatically via seed:seed_tests'}
        # }}

        self.assert_find_success(MODULE_NAME, result1, self.expected_db_02)

    def test_calibration_constants_get_prior_in_time(self):
        #
        # Search for the valid version among many
        #
        calibration_constant_ids = [-1, -2, -3, -4]
        physical_detector_unit_id = -1
        event_at = '2014-05-26T09:00:00.000+02:00'
        snapshot_at = None

        result1 = CalibrationConstantVersion.get_prior_in_time(
            self.cal_client, calibration_constant_ids,
            physical_detector_unit_id,
            event_at, snapshot_at)

        self.assert_find_success(MODULE_NAME, result1, self.expected_db_01)

    def test_calibration_constants_get_all_versions_now(self):
        #
        # Search for all the version
        #
        calibration_constant_ids = [-1, -2]
        physical_detector_unit_id = -1
        event_at = None
        snapshot_at = None

        result1 = CalibrationConstantVersion.get_all_versions(
            self.cal_client, calibration_constant_ids,
            physical_detector_unit_id,
            event_at, snapshot_at)

        assert [(d['id'], d['name']) for d in result1['data']] == [
            (-4, self.expected_db_04['name']),
            (-3, 'CALIBRATION_CONSTANT_VERSION_TEST-3_DO_NOT_DELETE'),
            (-2, self.expected_db_02['name']),
            (-1, 'CALIBRATION_CONSTANT_VERSION_TEST-1_DO_NOT_DELETE'),
        ]

    def test_calibration_constants_get_all_versions_in_the_past(self):
        #
        # Search for all the version
        #
        calibration_constant_ids = [-1, -2]
        physical_detector_unit_id = -1
        event_at = '2014-05-26T12:00:00.000+02:00'
        snapshot_at = None

        result1 = CalibrationConstantVersion.get_all_versions(
            self.cal_client, calibration_constant_ids,
            physical_detector_unit_id,
            event_at, snapshot_at)

        assert [(d['id'], d['name']) for d in result1['data']] == [
            (-2, self.expected_db_02['name']),
            (-1, 'CALIBRATION_CONSTANT_VERSION_TEST-1_DO_NOT_DELETE'),
            (-3, 'CALIBRATION_CONSTANT_VERSION_TEST-3_DO_NOT_DELETE'),
            (-4, self.expected_db_04['name']),
        ]

    def test_calibration_constant_versions_by_detector_conditions(self):
        calibration_ids = [-1, -2]
        detector_identifier = 'TEST_DET_CI-2'
        condition = {
            "parameters_conditions_attributes": [{"parameter_id": "-1",
                                                  "value": "2.5"},
                                                 {"parameter_id": "-2",
                                                  "value": "1.5"}]}

        results = CalibrationConstantVersion.get_closest_by_time_by_detector_conditions(  # noqa
            self.cal_client, detector_identifier,
            calibration_ids,
            condition)

        # sort results
        data_sorted = sorted(results['data'], key=lambda d: -d['id'])

        assert [(d['id'], d['name'],
                 d['physical_detector_unit']['physical_name']) for d in
                data_sorted] == [
                   (-7, 'CALIBRATION_CONSTANT_VERSION_TEST-7_DO_NOT_DELETE',
                    'PHYSICAL_DETECTOR_UNIT-1_DO_NOT_DELETE'),
                   (-8, 'CALIBRATION_CONSTANT_VERSION_TEST-8_DO_NOT_DELETE',
                    'PHYSICAL_DETECTOR_UNIT-2_DO_NOT_DELETE'),
                   (-9, 'CALIBRATION_CONSTANT_VERSION_TEST-9_DO_NOT_DELETE',
                    'PHYSICAL_DETECTOR_UNIT-3_DO_NOT_DELETE'),
                   (-10, 'CALIBRATION_CONSTANT_VERSION_TEST-10_DO_NOT_DELETE',
                    'PHYSICAL_DETECTOR_UNIT-1_DO_NOT_DELETE'),
                   (-11, 'CALIBRATION_CONSTANT_VERSION_TEST-11_DO_NOT_DELETE',
                    'PHYSICAL_DETECTOR_UNIT-2_DO_NOT_DELETE'),
                   (-12, 'CALIBRATION_CONSTANT_VERSION_TEST-12_DO_NOT_DELETE',
                    'PHYSICAL_DETECTOR_UNIT-3_DO_NOT_DELETE')
               ]

    #
    # fields_validation
    #

    def fields_validation(self, receive, expect):
        assert receive['name'] == expect['name']
        assert receive['file_name'] == expect['file_name']
        assert receive['path_to_file'] == expect['path_to_file']
        assert receive['data_set_name'] == expect['data_set_name']
        assert receive['flg_deployed'] == expect['flg_deployed']
        assert receive['flg_good_quality'] == expect['flg_good_quality']

        # datetime fields
        assert parse_dt(receive['begin_at']) == parse_dt(expect['begin_at'])
        assert parse_dt(receive['begin_validity_at']) \
               == parse_dt(expect['begin_validity_at'])
        assert parse_dt(receive['end_validity_at']) \
               == parse_dt(expect['end_validity_at'])

        assert receive['start_idx'] == expect['start_idx']
        assert receive['end_idx'] == expect['end_idx']
        assert receive['raw_data_location'] == expect['raw_data_location']
        assert receive['description'] == expect['description']

        receive_cc_id = receive['calibration_constant']['id']
        assert receive_cc_id == expect['calibration_constant_id']

        receive_cc_id = receive[PHYSICAL_DETECTOR_UNIT]['id']
        assert receive_cc_id == expect['physical_detector_unit_id']


if __name__ == '__main__':
    unittest.main()
