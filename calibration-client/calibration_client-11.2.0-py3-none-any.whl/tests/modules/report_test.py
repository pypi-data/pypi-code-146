"""ReportTest class"""

import unittest

import pytest

from .module_base import ModuleBase
from ..common.config_test import REPORT, RESOURCE_NOT_FOUND
from ...modules.report import Report

MODULE_NAME = REPORT


@pytest.mark.usefixtures('client_cls')
class ReportTest(ModuleBase, unittest.TestCase):
    def setUp(self):
        __unique_name1 = 'Report01-Dynamic-TO_DELETED'
        self.report_01 = {
            'name': __unique_name1,
            'file_path': __unique_name1,
            'flg_available': True,
            'description': 'desc 01'
        }

        __unique_name_upd = 'Report01-Dynamic_UPD-TO_DELETED'
        self.report_01_upd = {
            'name': __unique_name_upd,
            'file_path': __unique_name_upd,
            'flg_available': False,
            'description': 'desc 01 Updated!'
        }

    def test_create_report(self):
        report_01 = Report(
            calibration_client=self.cal_client,
            name=self.report_01['name'],
            file_path=self.report_01['file_path'],
            flg_available=self.report_01['flg_available'],
            description=self.report_01['description'])

        #
        # Create new entry (should succeed)
        #
        result1 = report_01.create()

        try:
            self.assert_create_success(MODULE_NAME, result1, self.report_01)

            report_id = result1['data']['id']
            report_name = result1['data']['name']
            report_file_path = result1['data']['file_path']

            # Create duplicated entry (should throw an error)
            report_01_dup = report_01
            result2 = report_01_dup.create()
            expect_app_info = {'name': ['has already been taken'],
                               'file_path': ['has already been taken']}
            self.assert_create_error(MODULE_NAME, result2, expect_app_info)

            # Set duplicated entry
            # (should NOT throw an error and return the report from the DB)
            result3 = report_01_dup.set()
            self.assert_set_success(MODULE_NAME, result3, self.report_01)

            # Get entry by name & file_path
            result3 = Report.get_by_name_and_file_path(self.cal_client,
                                                       report_name,
                                                       report_file_path)
            self.assert_find_success(MODULE_NAME, result3, self.report_01)

            # Get entry by ID
            result4 = Report.get_by_id(self.cal_client, report_id)
            self.assert_find_success(MODULE_NAME, result4, self.report_01)

            # Get entry with non-existent ID (should throw an error)
            result5 = Report.get_by_id(self.cal_client, -666)
            self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)

            # Put entry information (update some fields should succeed)
            report_01.name = self.report_01_upd['name']
            report_01.file_path = self.report_01_upd['file_path']
            report_01.flg_available = self.report_01_upd['flg_available']
            report_01.description = self.report_01_upd['description']
            result6 = report_01.update()
            self.assert_update_success(MODULE_NAME, result6,
                                       self.report_01_upd)

            # Put entry information (update some fields should throw an error)
            report_01.name = '__THIS_NAME_IS_1_CHARACTERS_LONGER_THAN_THE_ALLOWED_MAX_NUM_1234__'  # noqa
            report_01.flg_available = self.report_01_upd['flg_available']
            report_01.description = self.report_01_upd['description']
            result7 = report_01.update()
            expect_app_info = {
                'name': ['is too long (maximum is 64 characters)']}
            self.assert_update_error(MODULE_NAME, result7, expect_app_info)

        finally:
            # Delete entry (should succeed)
            # (test purposes only to keep the DB clean)
            result8 = report_01.delete()

        # Check deletion worked if there isn't already an error to report
        self.assert_delete_success(MODULE_NAME, result8)

        # Delete entry (should throw an error)
        # (test purposes only to keep the DB clean)
        result9 = report_01.delete()
        self.assert_delete_error(MODULE_NAME, result9, RESOURCE_NOT_FOUND)

    def fields_validation(self, receive, expect):
        assert receive['name'] == expect['name']
        assert receive['file_path'] == expect['file_path']
        assert receive['flg_available'] == expect['flg_available']
        assert receive['description'] == expect['description']


if __name__ == '__main__':
    unittest.main()
