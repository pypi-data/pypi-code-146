"""DetectorTypeApiTest class"""

import unittest
from http import HTTPStatus

import pytest

from .api_base import ApiBase
from ..common.generators import generate_unique_name
from ..common.config_test import *


@pytest.mark.usefixtures('client_cls')
class DetectorTypeApiTest(ApiBase, unittest.TestCase):
    def test_create_detector_type_api(self):
        __unique_name = generate_unique_name('DetectorTypeApi')
        detector_type = {
            'detector_type': {
                'name': __unique_name,
                'flg_available': True,
                'description': 'desc 01'
            }
        }

        expect = detector_type['detector_type']

        # Create new entry (should succeed)
        received = self.__create_entry_api(detector_type, expect)

        detector_type_id = received['id']
        detector_type_name = received['name']

        try:
            # Create duplicated entry (should throw an error)
            self.__create_error_entry_uk_api(detector_type)

            # Get entry by name
            self.__get_all_entries_by_name_api(detector_type_name, expect)

            # Get entry by ID
            self.__get_entry_by_id_api(detector_type_id, expect)

            # Put entry information (update some fields should succeed)
            self.__update_entry_api(detector_type_id, expect)

        finally:
            # Delete entry (should succeed)
            # (test purposes only to keep the DB clean)
            del_resp = self.cal_client.delete_detector_type_api(
                detector_type_id)

        # Validate the response from deletion if nothing already error-ed
        self.get_and_validate_delete_entry_by_id(del_resp)

    def fields_validation(self, receive, expect):
        assert receive['name'] == expect['name']
        assert receive['flg_available'] == expect['flg_available']
        assert receive['description'] == expect['description']

    #
    # Internal private APIs methods
    #
    def __create_entry_api(self, entry_info, expect):
        response = self.cal_client.create_detector_type_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __create_error_entry_uk_api(self, entry_info):
        response = self.cal_client.create_detector_type_api(entry_info)
        receive = self.load_response_content(response)

        expect = {'info': {'name': ['has already been taken']}}
        assert receive == expect
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def __update_entry_api(self, entry_id, expect):
        unique_name_upd = generate_unique_name('DetectorTypeApiUpd')
        detector_type_upd = {
            'detector_type': {
                'name': unique_name_upd,
                'flg_available': False,
                'description': 'desc 01 updated!!!'
            }
        }

        response = self.cal_client.update_detector_type_api(entry_id,
                                                            detector_type_upd)
        receive = self.load_response_content(response)

        expect_upd = detector_type_upd['detector_type']

        self.fields_validation(receive, expect_upd)
        assert response.status_code == HTTPStatus.OK

        assert expect['name'] != expect_upd['name']
        assert expect['flg_available'] != expect_upd['flg_available']
        assert expect['description'] != expect_upd['description']

    def __get_all_entries_by_name_api(self, name, expect,
                                      page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        response = self.cal_client.get_all_detector_types_by_name_api(name, page, page_size)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.cal_client.get_detector_type_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)


if __name__ == '__main__':
    unittest.main()
