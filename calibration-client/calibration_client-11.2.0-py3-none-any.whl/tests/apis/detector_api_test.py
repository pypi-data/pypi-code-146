"""DetectorApiTest class"""

import unittest
from http import HTTPStatus

import pytest

from .api_base import ApiBase
from ..common.config_test import *


@pytest.mark.usefixtures('client_cls')
class DetectorApiTest(ApiBase, unittest.TestCase):
    def test_create_detector_api(self):
        __unique_name = 'DetectorApi-Dynamic-TO_DELETED'
        detector = {
            'detector': {
                'name': __unique_name,
                'identifier': __unique_name,
                'karabo_name': __unique_name,
                'karabo_id_control': 'Q1M1',
                'flg_available': True,
                'description': 'desc 01'
            }
        }

        expect = detector['detector']

        # Create new entry (should succeed)
        # received = self.__create_entry_api(detector, expect)

        created_entry_resp = self.cal_client.create_detector_api(detector)

        created_entry_received = self.get_and_validate_create_entry(
            created_entry_resp)

        detector_id = created_entry_received['id']
        det_name = created_entry_received['name']
        det_identifier = created_entry_received['identifier']

        try:
            # Check that expected creation result was received
            self.fields_validation(created_entry_received, expect)

            # Create duplicated entry (should throw an error)
            self.__create_error_entry_uk_api(detector)

            # Get entry by name
            self.__get_all_entries_by_name_api(det_name, expect)

            # Get entry by identifier
            self.__get_all_entries_by_identifier_api(det_identifier, expect)

            # Get entry by ID
            self.__get_entry_by_id_api(detector_id, expect)

            # Put entry information (update some fields should succeed)
            self.__update_entry_api(detector_id, expect)

        finally:
            # Delete entry (should succeed)
            # (test purposes only to keep the DB clean)
            del_resp = self.cal_client.delete_detector_api(detector_id)

        # Validate the response from deletion if nothing already error-ed
        self.get_and_validate_delete_entry_by_id(del_resp)

    def fields_validation(self, receive, expect):
        assert receive['name'] == expect['name']
        assert receive['identifier'] == expect['identifier']
        assert receive['karabo_name'] == expect['karabo_name']
        assert receive['karabo_id_control'] == expect['karabo_id_control']
        assert receive['flg_available'] == expect['flg_available']
        assert receive['description'] == expect['description']

    #
    # Internal private APIs methods
    #
    def __create_entry_api(self, entry_info, expect):
        response = self.cal_client.create_detector_api(entry_info)

        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)
        return receive

    def __create_error_entry_uk_api(self, entry_info):
        response = self.cal_client.create_detector_api(entry_info)
        receive = self.load_response_content(response)

        expect = {'info': {'name': ['has already been taken'],
                           'identifier': ['has already been taken'],
                           'karabo_name': ['has already been taken']}}
        assert receive == expect
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def __update_entry_api(self, entry_id, expect):
        unique_name_upd = 'DetApi-Dynamic_UPD-TO_DELETED'
        detector_upd = {
            'detector': {
                'name': unique_name_upd,
                'identifier': expect['identifier'],
                'karabo_name': unique_name_upd,
                'karabo_id_control': 'Q1M2',
                'flg_available': False,
                'description': 'desc 01 updated!!!'
            }
        }

        response = self.cal_client.update_detector_api(entry_id,
                                                       detector_upd)
        receive = self.load_response_content(response)

        expect_upd = detector_upd['detector']

        self.fields_validation(receive, expect_upd)
        assert response.status_code == HTTPStatus.OK

        assert expect['name'] != expect_upd['name']
        # identifier is immutable in detector model
        assert receive['identifier'] == expect['identifier']
        assert receive['karabo_name'] != expect['karabo_name']
        assert receive['karabo_id_control'] != expect['karabo_id_control']
        assert expect['flg_available'] != expect_upd['flg_available']
        assert expect['description'] != expect_upd['description']

    def __update_entry_api_immutable(self, entry_id, expect):
        unique_name_upd = 'DetApi-Dynamic_UPD-TO_DELETED'
        detector_upd = {
            'detector': {
                'name': unique_name_upd,
                'identifier': unique_name_upd,
                'karabo_name': unique_name_upd,
                'karabo_id_control': 'Q1M2',
                'flg_available': False,
                'description': 'desc 01 updated!!!'
            }
        }

        response = self.cal_client.update_detector_api(entry_id,
                                                       detector_upd)
        receive = self.load_response_content(response)

        expect = {'info': {'identifier': ['cannot be updated']}}
        assert receive == expect
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def __get_all_entries_by_name_api(self, name, expect,
                                      page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        response = self.cal_client.get_all_detectors_by_name_api(name, page, page_size)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_all_entries_by_identifier_api(self, identifier, expect):
        resp = self.cal_client.get_all_detectors_by_identifier_api(identifier)
        receive = self.get_and_validate_all_entries_by_name(resp)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.cal_client.get_detector_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)


if __name__ == '__main__':
    unittest.main()
