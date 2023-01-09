"""BaseApiTest Class with helper methods common to all modules tests"""

import unittest
from http import HTTPStatus

from calibration_client.common.base import Base
from ..common.config_test import RESOURCE_NOT_FOUND


class ApiBase(unittest.TestCase):
    @staticmethod
    def load_response_content(response):
        return Base.load_json_from_content(response)

    def get_and_validate_create_entry(self, response):
        assert response.status_code == HTTPStatus.CREATED

        return self.load_response_content(response)

    def get_and_validate_set_entry(self, response):
        assert response.status_code in [HTTPStatus.CREATED, HTTPStatus.OK]

        return self.load_response_content(response)

    def get_and_validate_all_entries_by_name(self, response):
        assert response.status_code == HTTPStatus.OK

        resp_content = self.load_response_content(response)
        return resp_content[0]

    def get_and_validate_entry_by_id(self, response):
        assert response.status_code == HTTPStatus.OK

        return self.load_response_content(response)

    def get_and_validate_delete_entry_by_id(self, response):
        assert response.status_code == HTTPStatus.NO_CONTENT

        assert self.load_response_content(response) == {}

    def get_and_validate_resource_not_found(self, response):
        receive = self.load_response_content(response)
        expect = {'info': RESOURCE_NOT_FOUND}

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert receive == expect
