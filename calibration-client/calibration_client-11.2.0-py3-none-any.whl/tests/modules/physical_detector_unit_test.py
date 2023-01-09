"""PhysicalDetectorUnitTest class"""

import unittest

import pytest

from .module_base import ModuleBase
from ..common.config_test import PHYSICAL_DETECTOR_UNIT, RESOURCE_NOT_FOUND
from ..common.generators import generate_unique_name
from ...modules.physical_detector_unit import PhysicalDetectorUnit

MODULE_NAME = PHYSICAL_DETECTOR_UNIT


@pytest.mark.usefixtures('client_cls')
class PhysicalDetectorUnitTest(ModuleBase, unittest.TestCase):
    def setUp(self):
        __unique_name1 = generate_unique_name('PhysicalDev01')
        self.pd_01 = {
            'physical_name': __unique_name1,
            'karabo_da': __unique_name1,
            'virtual_device_name': __unique_name1,
            'uuid': 1001,
            'detector_type_id': -1,
            'detector_id': -1,
            'flg_available': True,
            'description': 'desc 01'
        }

        __unique_name_upd = generate_unique_name('PhysicalDevUpd01')
        self.pd_01_upd = {
            'physical_name': __unique_name1,
            'karabo_da': __unique_name_upd,
            'virtual_device_name': __unique_name_upd,
            'detector_type_id': -1,
            'detector_id': -1,
            'flg_available': False,
            'description': 'desc 01 Updated!!!'
        }

    def test_create_physical_detector_unit(self):
        pd_01 = PhysicalDetectorUnit(
            calibration_client=self.cal_client,
            physical_name=self.pd_01['physical_name'],
            karabo_da=self.pd_01['karabo_da'],
            virtual_device_name=self.pd_01['virtual_device_name'],
            uuid=self.pd_01['uuid'],
            detector_type_id=self.pd_01['detector_type_id'],
            detector_id=self.pd_01['detector_id'],
            flg_available=self.pd_01['flg_available'],
            description=self.pd_01['description'])

        # Create new entry (should succeed)
        result1 = pd_01.create()
        self.assert_create_success(MODULE_NAME, result1, self.pd_01)

        physical_dev_id = result1['data']['id']
        pdu_phy_name = result1['data']['physical_name']

        try:
            # Create duplicated entry (should throw an error)
            result2 = pd_01.create()
            expect_app_info = {'physical_name': ['has already been taken'],
                               'karabo_da': ['has already been taken']}
            self.assert_create_error(MODULE_NAME, result2, expect_app_info)

            # Get entry by name
            res3 = PhysicalDetectorUnit.get_by_name(self.cal_client,
                                                    pdu_phy_name)
            self.assert_find_success(MODULE_NAME, res3, self.pd_01)

            # Get entry by ID
            result4 = PhysicalDetectorUnit.get_by_id(self.cal_client,
                                                     physical_dev_id)
            self.assert_find_success(MODULE_NAME, result4, self.pd_01)

            # Get entry with non-existent ID (should throw an error)
            physical_detector_unit_id = -666
            result5 = PhysicalDetectorUnit.get_by_id(self.cal_client,
                                                     physical_detector_unit_id)
            self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)

            # Put entry information (update some fields should succeed)
            pd_01.physical_name = self.pd_01_upd['physical_name']
            pd_01.karabo_da = self.pd_01_upd['karabo_da']
            pd_01.virtual_device_name = self.pd_01_upd['virtual_device_name']
            pd_01.flg_available = self.pd_01_upd['flg_available']
            pd_01.description = self.pd_01_upd['description']
            result6 = pd_01.update()
            self.assert_update_success(MODULE_NAME, result6, self.pd_01_upd)

            # Put entry information (update some fields should throw an error)
            pd_01.physical_name = '__THIS_NAME_CANNOT_BE_UPDATED'  # noqa
            pd_01.flg_available = self.pd_01_upd['flg_available']
            pd_01.description = self.pd_01_upd['description']
            result7 = pd_01.update()
            expect_app_info = {
                'physical_name': ['cannot be updated']}
            self.assert_update_error(MODULE_NAME, result7, expect_app_info)

        finally:
            # Delete entry (should succeed)
            # (test purposes only to keep the DB clean)
            result8 = pd_01.delete()

        # Check deletion worked if there isn't already an error to report
        self.assert_delete_success(MODULE_NAME, result8)

        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        result9 = pd_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def fields_validation(self, receive, expect):
        assert receive['physical_name'] == expect['physical_name']
        assert receive['karabo_da'] == expect['karabo_da']
        assert receive['virtual_device_name'] == expect['virtual_device_name']
        assert receive['detector_type_id'] == expect['detector_type_id']
        assert receive['detector_id'] == expect['detector_id']
        assert receive['flg_available'] == expect['flg_available']
        assert receive['description'] == expect['description']


if __name__ == '__main__':
    unittest.main()
