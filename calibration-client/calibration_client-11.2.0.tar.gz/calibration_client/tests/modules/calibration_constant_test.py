"""CalibrationConstantTest class"""

import unittest

import pytest

from .module_base import ModuleBase
from ..common.config_test import CALIBRATION_CONSTANT, RESOURCE_NOT_FOUND
from ..common.generators import generate_unique_name
from ...modules.calibration_constant import CalibrationConstant

MODULE_NAME = CALIBRATION_CONSTANT


@pytest.mark.usefixtures('client_cls')
class CalibrationConstantTest(ModuleBase, unittest.TestCase):
    def setUp(self):
        __unique_name1 = generate_unique_name('CalConst01')
        self.cc_01 = {
            'name': __unique_name1,
            'calibration_id': -2,
            'detector_type_id': -1,
            'condition_id': -1,
            'flg_auto_approve': True,
            'flg_available': True,
            'description': 'desc 01'
        }

        __unique_name_upd = generate_unique_name('CalConstUpd01')
        self.cc_01_upd = {
            'name': __unique_name_upd,
            'calibration_id': -2,
            'detector_type_id': -1,
            'condition_id': -1,
            'flg_auto_approve': False,
            'flg_available': False,
            'description': 'desc 01 updated!'
        }

    def test_create_calibration_constant(self):
        cc_01 = CalibrationConstant(
            calibration_client=self.cal_client,
            name=self.cc_01['name'],
            calibration_id=self.cc_01['calibration_id'],
            detector_type_id=self.cc_01['detector_type_id'],
            condition_id=self.cc_01['condition_id'],
            flg_auto_approve=self.cc_01['flg_auto_approve'],
            flg_available=self.cc_01['flg_available'],
            description=self.cc_01['description']
        )

        # Create new entry (should succeed)
        result1 = cc_01.create()
        self.assert_create_success(MODULE_NAME, result1, self.cc_01)

        calibration_constant = result1['data']
        cc_id = calibration_constant['id']
        cc_name = calibration_constant['name']
        cc_calibration_id = calibration_constant['calibration_id']
        cc_detector_type_id = calibration_constant['detector_type_id']
        cc_condition_id = calibration_constant['condition_id']

        # Create duplicated entry (should throw an error)
        try:
            result2 = cc_01.create()
            expect_app_info = {'name': ['has already been taken'],
                               'condition': ['has already been taken'],
                               'detector_type': ['has already been taken'],
                               'calibration': ['has already been taken']}
            self.assert_create_error(MODULE_NAME, result2, expect_app_info)

            # Get entry by name
            result3 = CalibrationConstant.get_by_name(self.cal_client, cc_name)
            self.assert_find_success(MODULE_NAME, result3, self.cc_01)

            # Get entry by ID
            result4 = CalibrationConstant.get_by_id(self.cal_client, cc_id)
            self.assert_find_success(MODULE_NAME, result4, self.cc_01)

            # Get entry with non-existent ID (should throw an error)
            cc_id = -666
            result5 = CalibrationConstant.get_by_id(self.cal_client, cc_id)
            self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)

            # Get entry by UK (should succeed)
            # (calibration_id, detector_type_id, condition_id)
            result_uk = CalibrationConstant.get_by_uk(self.cal_client,
                                                      cc_calibration_id,
                                                      cc_detector_type_id,
                                                      cc_condition_id)
            self.assert_find_success(MODULE_NAME, result_uk, self.cc_01)

            # Get entry by UK (should throw an error)
            # (calibration_id, detector_type_id, condition_id)
            calibration_id = -666
            detector_type_id = -666
            condition_id = -666
            res_uk_error = CalibrationConstant.get_by_uk(
                self.cal_client, calibration_id, detector_type_id, condition_id
            )
            self.assert_find_error(MODULE_NAME, res_uk_error,
                                   RESOURCE_NOT_FOUND)

            # Put entry information (update some fields should succeed)
            cc_01.name = self.cc_01_upd['name']
            cc_01.flg_auto_approve = self.cc_01_upd['flg_auto_approve']
            cc_01.flg_available = self.cc_01_upd['flg_available']
            cc_01.description = self.cc_01_upd['description']
            result6 = cc_01.update()
            self.assert_update_success(MODULE_NAME, result6, self.cc_01_upd)

            # Put entry information (update some fields should throw an error)
            wrong_name = "__THIS_NAME_IS_1_CHARACTERS_LONGER_THAN"  # 39 char
            wrong_name += "_THE_ALLOWED_MAX_NUM__"  # 22 char
            wrong_name += "_(NUM_CHARACTERS_IS_256)_"  # 25 char
            # 256 - (39 + 22 + 25) =
            wrong_name += "-->_{0}".format('Z' * 170)

            cc_01.name = wrong_name
            cc_01.flg_available = self.cc_01_upd['flg_available']
            cc_01.description = self.cc_01_upd['description']
            result7 = cc_01.update()

            expect_app_info = {
                'name': ['is too long (maximum is 255 characters)']}
            self.assert_update_error(MODULE_NAME, result7, expect_app_info)

        finally:
            # Delete entry (should succeed)
            # (test purposes only to keep the DB clean)
            result8 = cc_01.delete()

        # Check deletion worked if there isn't already an error to report
        self.assert_delete_success(MODULE_NAME, result8)

        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        result9 = cc_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def test_create_calibration_constant_from_dict(self):
        # Create new entry (should succeed)
        result1 = CalibrationConstant.set_from_dict(self.cal_client,
                                                    self.cc_01)
        self.assert_create_success(MODULE_NAME, result1, self.cc_01)

        calibration_constant = result1['data']
        cc_id = calibration_constant['id']

        try:
            # Create duplicated entry (should throw an error)
            result2 = CalibrationConstant.create_from_dict(self.cal_client,
                                                           self.cc_01)
            expect_app_info = {'name': ['has already been taken'],
                               'condition': ['has already been taken'],
                               'detector_type': ['has already been taken'],
                               'calibration': ['has already been taken']}
            self.assert_create_error(MODULE_NAME, result2, expect_app_info)

            # Set existing entry (should find item successfully)
            result3 = CalibrationConstant.set_from_dict(self.cal_client,
                                                        self.cc_01)
            self.assert_find_success(MODULE_NAME, result3, self.cc_01)

            # Get entry by UK (should succeed)
            # (calibration_id, detector_type_id, condition_id)
            result_uk = CalibrationConstant.set_from_dict(self.cal_client,
                                                          self.cc_01)
            self.assert_find_success(MODULE_NAME, result_uk, self.cc_01)

        finally:
            # Delete entry (should succeed)
            # (test purposes only to keep the DB clean)
            result8 = CalibrationConstant.delete_by_id(self.cal_client, cc_id)

        # Check deletion worked if there isn't already an error to report
        self.assert_delete_success(MODULE_NAME, result8)

        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        result9 = CalibrationConstant.delete_by_id(self.cal_client, cc_id)
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def fields_validation(self, receive, expect):
        assert receive['name'] == expect['name']
        assert receive['detector_type_id'] == expect['detector_type_id']
        assert receive['calibration_id'] == expect['calibration_id']
        assert receive['condition_id'] == expect['condition_id']
        assert receive['flg_auto_approve'] == expect['flg_auto_approve']
        assert receive['flg_available'] == expect['flg_available']
        assert receive['description'] == expect['description']


if __name__ == '__main__':
    unittest.main()
