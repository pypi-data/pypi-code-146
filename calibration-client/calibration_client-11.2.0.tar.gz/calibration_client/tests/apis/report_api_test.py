"""ReportApiTest class"""

import unittest
from http import HTTPStatus

import pytest

from .api_base import ApiBase
from ..common.config_test import *


@pytest.mark.usefixtures('client_cls')
class ReportApiTest(ApiBase, unittest.TestCase):
    def test_create_report_api(self):
        __unique_name = 'ReportApi-Dynamic-TO_DELETED'
        report = {
            'report': {
                'name': __unique_name,
                'file_path': __unique_name,
                'flg_available': True,
                'description': 'desc 01'
            }
        }

        expect = report['report']

        # Create new entry (should succeed)
        # received = self.__create_entry_api(report, expect)

        created_entry_resp = self.cal_client.create_report_api(report)

        created_entry_received = self.get_and_validate_create_entry(
            created_entry_resp)

        report_id = created_entry_received['id']
        repo_name = created_entry_received['name']
        repo_file_path = created_entry_received['file_path']

        try:
            # Check that expected creation result was received
            self.fields_validation(created_entry_received, expect)

            # Create duplicated entry (should throw an error)
            self.__create_error_entry_uk_api(report)

            # Set duplicated entry
            # (should NOT throw an error and return the report from the DB)
            self.__set_failsafe_duplicate_entry_uk_api(report, expect)

            # Get entry by name
            self.__get_all_entries_by_name_api(repo_name, expect)

            # Get entry by identifier
            self.__get_all_entries_by_name_and_path_api(repo_name,
                                                        repo_file_path,
                                                        expect)

            # Get entry by ID
            self.__get_entry_by_id_api(report_id, expect)

            # Put entry information (update some fields should succeed)
            self.__update_entry_api(report_id, expect)

        finally:
            # Delete entry (should succeed)
            # (test purposes only to keep the DB clean)
            del_resp = self.cal_client.delete_report_api(report_id)

        # Validate the response from deletion if nothing already error-ed
        self.get_and_validate_delete_entry_by_id(del_resp)

    def fields_validation(self, receive, expect):
        assert receive['name'] == expect['name']
        assert receive['file_path'] == expect['file_path']
        assert receive['flg_available'] == expect['flg_available']
        assert receive['description'] == expect['description']

    #
    # Internal private APIs methods
    #
    def __create_entry_api(self, entry_info, expect):
        response = self.cal_client.create_report_api(entry_info)

        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __create_error_entry_uk_api(self, entry_info):
        response = self.cal_client.create_report_api(entry_info)
        receive = self.load_response_content(response)
        expect = {'info': {'name': ['has already been taken'],
                           'file_path': ['has already been taken']}}
        assert receive == expect
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def __set_failsafe_duplicate_entry_uk_api(self, entry_info, expect):
        response = self.cal_client.set_report_api(entry_info)
        receive = self.get_and_validate_set_entry(response)
        self.fields_validation(receive, expect)

    def __update_entry_api(self, entry_id, expect):
        unique_name_upd = 'ReportApi-Dynamic_UPD-TO_DELETED'
        report_upd = {
            'report': {
                'name': unique_name_upd,
                'file_path': unique_name_upd,
                'flg_available': False,
                'description': 'desc 01 updated!!!'
            }
        }

        response = self.cal_client.update_report_api(entry_id,
                                                     report_upd)
        receive = self.load_response_content(response)

        expect_upd = report_upd['report']

        self.fields_validation(receive, expect_upd)
        assert response.status_code == HTTPStatus.OK

        assert expect['name'] != expect_upd['name']
        assert receive['file_path'] != expect['file_path']
        assert expect['flg_available'] != expect_upd['flg_available']
        assert expect['description'] != expect_upd['description']

    def __get_all_entries_by_name_api(self, name, expect,
                                      page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        response = self.cal_client.get_all_reports_by_name_api(name, page, page_size)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_all_entries_by_name_and_path_api(self, name, file_path, expect):
        resp = self.cal_client.get_all_reports_by_name_and_file_path_api(
            name, file_path)
        receive = self.get_and_validate_all_entries_by_name(resp)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.cal_client.get_report_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)


if __name__ == '__main__':
    unittest.main()
