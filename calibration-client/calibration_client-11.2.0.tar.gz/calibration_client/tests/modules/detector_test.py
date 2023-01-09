"""DetectorTest class"""

import unittest

import pytest

from .module_base import ModuleBase
from ..common.config_test import DETECTOR, RESOURCE_NOT_FOUND
from ...modules.detector import Detector

MODULE_NAME = DETECTOR


@pytest.mark.usefixtures('client_cls')
class DetectorTest(ModuleBase, unittest.TestCase):
    def setUp(self):
        __unique_name1 = 'Detector01-Dynamic-TO_DELETED'
        self.detector_1 = {
            'name': __unique_name1,
            'identifier': __unique_name1,
            'karabo_name': __unique_name1,
            'karabo_id_control': 'Q1M1',
            'flg_available': True,
            'description': 'desc 01'
        }

        __unique_name_upd = 'Det01-Dynamic_UPD-TO_DELETED'
        self.detector_1_upd = {
            'name': __unique_name_upd,
            'identifier': __unique_name_upd,
            'karabo_name': __unique_name_upd,
            'karabo_id_control': 'Q1M2',
            'flg_available': False,
            'description': 'desc 01 Updated!'
        }

    def test_create_detector(self):

        print('*' * 100)
        print('detector_01[name] =>', str(self.detector_1['name']))
        print('detector_01[identifier] =>', str(self.detector_1['identifier']))
        print('detector_01[karabo_name] =>',
              str(self.detector_1['karabo_name']))
        print('detector_01[karabo_id_control] =>',
              str(self.detector_1['karabo_id_control']))
        print('*' * 100)

        detector_01 = Detector(
            calibration_client=self.cal_client,
            name=self.detector_1['name'],
            identifier=self.detector_1['identifier'],
            karabo_name=self.detector_1['karabo_name'],
            karabo_id_control=self.detector_1['karabo_id_control'],
            flg_available=self.detector_1['flg_available'],
            description=self.detector_1['description'])

        #
        # Create new entry (should succeed)
        #
        result1 = detector_01.create()

        try:
            self.assert_create_success(MODULE_NAME, result1, self.detector_1)

            detector_id = result1['data']['id']
            detector_name = result1['data']['name']

            # Create duplicated entry (should throw an error)
            detector_01_dup = detector_01
            result2 = detector_01_dup.create()
            expect_app_info = {'name': ['has already been taken'],
                               'identifier': ['has already been taken'],
                               'karabo_name': ['has already been taken']}
            self.assert_create_error(MODULE_NAME, result2, expect_app_info)

            # Get entry by name
            result3 = Detector.get_by_name(self.cal_client, detector_name)
            self.assert_find_success(MODULE_NAME, result3, self.detector_1)

            # Get entry by ID
            result4 = Detector.get_by_id(self.cal_client, detector_id)
            self.assert_find_success(MODULE_NAME, result4, self.detector_1)

            # Get entry with non-existent ID (should throw an error)
            result5 = Detector.get_by_id(self.cal_client, -666)
            self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)

            # Put entry information (update some fields should succeed)
            detector_01.name = self.detector_1_upd['name']
            detector_01.flg_available = self.detector_1_upd['flg_available']
            detector_01.description = self.detector_1_upd['description']
            result6 = detector_01.update()
            self.assert_update_success(MODULE_NAME, result6,
                                       self.detector_1_upd)

            # Put entry information (update some fields should throw an error)
            detector_01.name = '__THIS_NAME_IS_1_CHARACTERS_LONGER_THAN_THE_ALLOWED_MAX_NUM_1234__'  # noqa
            detector_01.flg_available = self.detector_1_upd['flg_available']
            detector_01.description = self.detector_1_upd['description']
            result7 = detector_01.update()
            expect_app_info = {
                'name': ['is too long (maximum is 64 characters)']}
            self.assert_update_error(MODULE_NAME, result7, expect_app_info)

        finally:
            # Delete entry (should succeed)
            # (test purposes only to keep the DB clean)
            result8 = detector_01.delete()

        # Check deletion worked if there isn't already an error to report
        self.assert_delete_success(MODULE_NAME, result8)

        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        result9 = detector_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def fields_validation(self, receive, expect):
        assert receive['name'] == expect['name']
        assert receive['flg_available'] == expect['flg_available']
        assert receive['description'] == expect['description']


if __name__ == '__main__':
    unittest.main()
