"""DetectorTypeTest class"""

import unittest

import pytest

from .module_base import ModuleBase
from ..common.config_test import DETECTOR_TYPE, RESOURCE_NOT_FOUND
from ..common.generators import generate_unique_name
from ...modules.detector_type import DetectorType

MODULE_NAME = DETECTOR_TYPE


@pytest.mark.usefixtures('client_cls')
class DetectorTypeTest(ModuleBase, unittest.TestCase):
    def setUp(self):
        __unique_name1 = generate_unique_name('DetectorType01')
        self.dev_typ_01 = {
            'name': __unique_name1,
            'flg_available': True,
            'description': 'desc 01'
        }

        __unique_name_upd = generate_unique_name('DetectorTypeUpd01')
        self.dev_typ_01_upd = {
            'name': __unique_name_upd,
            'flg_available': False,
            'description': 'desc 01 Updated!'
        }

    def test_create_detector_type(self):
        dev_typ_01 = DetectorType(calibration_client=self.cal_client,
                                  name=self.dev_typ_01['name'],
                                  flg_available=self.dev_typ_01[
                                      'flg_available'],
                                  description=self.dev_typ_01['description'])

        #
        # Create new entry (should succeed)
        #
        result1 = dev_typ_01.create()
        self.assert_create_success(MODULE_NAME, result1, self.dev_typ_01)

        detector_type_id = result1['data']['id']
        detector_type_name = result1['data']['name']

        try:
            # Create duplicated entry (should throw an error)
            dev_typ_01_dup = dev_typ_01
            result2 = dev_typ_01_dup.create()
            expect_app_info = {'name': ['has already been taken']}
            self.assert_create_error(MODULE_NAME, result2, expect_app_info)

            # Get entry by name
            result3 = DetectorType.get_by_name(self.cal_client,
                                               detector_type_name)
            self.assert_find_success(MODULE_NAME, result3, self.dev_typ_01)

            # Get entry by ID
            result4 = DetectorType.get_by_id(self.cal_client, detector_type_id)
            self.assert_find_success(MODULE_NAME, result4, self.dev_typ_01)

            # Get entry with non-existent ID (should throw an error)
            result5 = DetectorType.get_by_id(self.cal_client, -666)
            self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)

            # Put entry information (update some fields should succeed)
            dev_typ_01.name = self.dev_typ_01_upd['name']
            dev_typ_01.flg_available = self.dev_typ_01_upd['flg_available']
            dev_typ_01.description = self.dev_typ_01_upd['description']
            result6 = dev_typ_01.update()
            self.assert_update_success(MODULE_NAME, result6,
                                       self.dev_typ_01_upd)

            # Put entry information (update some fields should throw an error)
            dev_typ_01.name = '__THIS_NAME_IS_1_CHARACTERS_LONGER_THAN_THE_ALLOWED_MAX_NUM__'  # noqa
            dev_typ_01.flg_available = self.dev_typ_01_upd['flg_available']
            dev_typ_01.description = self.dev_typ_01_upd['description']
            result7 = dev_typ_01.update()
            expect_app_info = {
                'name': ['is too long (maximum is 60 characters)']}
            self.assert_update_error(MODULE_NAME, result7, expect_app_info)

        finally:
            # Delete entry (should succeed)
            # (test purposes only to keep the DB clean)
            result8 = dev_typ_01.delete()

        # Check deletion worked if there isn't already an error to report
        self.assert_delete_success(MODULE_NAME, result8)

        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        result9 = dev_typ_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def fields_validation(self, receive, expect):
        assert receive['name'] == expect['name']
        assert receive['flg_available'] == expect['flg_available']
        assert receive['description'] == expect['description']


if __name__ == '__main__':
    unittest.main()
