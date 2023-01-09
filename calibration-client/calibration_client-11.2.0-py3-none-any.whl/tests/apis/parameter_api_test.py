"""ParameterApiTest class"""

import unittest
from http import HTTPStatus

import pytest

from .api_base import ApiBase
from ..common.config_test import *
from ..common.generators import generate_unique_name


@pytest.mark.usefixtures('client_cls')
class ParameterApiTest(ApiBase, unittest.TestCase):
    def test_create_parameter_api(self):
        __unique_name = generate_unique_name('ParameterApi')
        parameter = {
            PARAMETER: {
                'name': __unique_name,
                'unit_id': -1,
                'flg_available': True,
                'flg_logarithmic': False,
                'flg_text': False,
                'def_lower_deviation_value': 1.0,
                'def_upper_deviation_value': 1.2,
                'description': 'desc 01'
            }
        }

        expect = parameter[PARAMETER]

        # Create new entry (should succeed)
        received = self.__create_entry_api(parameter, expect)

        parameter_id = received['id']
        parameter_name = received['name']

        try:
            # Create duplicated entry (should throw an error)
            self.__create_error_entry_uk_api(parameter)

            # Get entry by name
            self.__get_all_entries_by_name_api(parameter_name, expect)

            # Get entry by ID
            self.__get_entry_by_id_api(parameter_id, expect)

            # Put entry information (update some fields should succeed)
            self.__update_entry_api(parameter_id, expect)

        finally:
            # Delete entry (should succeed)
            # (test purposes only to keep the DB clean)
            del_resp = self.cal_client.delete_parameter_api(parameter_id)

        # Validate the response from deletion if nothing already error-ed
        self.get_and_validate_delete_entry_by_id(del_resp)

    def fields_validation(self, receive, expect):
        assert receive['name'] == expect['name']
        assert receive['unit_id'] == expect['unit_id']
        assert receive['flg_available'] == expect['flg_available']
        assert receive['flg_logarithmic'] == expect['flg_logarithmic']
        assert receive['flg_text'] == expect['flg_text']
        assert receive['def_lower_deviation_value'] \
               == expect['def_lower_deviation_value']
        assert receive['def_upper_deviation_value'] \
               == expect['def_upper_deviation_value']
        assert receive['description'] == expect['description']

    def __create_entry_api(self, entry_info, expect):
        response = self.cal_client.create_parameter_api(entry_info)
        receive = self.get_and_validate_create_entry(response)
        self.fields_validation(receive, expect)

        return receive

    def __create_error_entry_uk_api(self, entry_info):
        response = self.cal_client.create_parameter_api(entry_info)
        receive = self.load_response_content(response)

        expect = {'info': {'name': ['has already been taken']}}
        assert receive == expect
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def __update_entry_api(self, entry_id, expect):
        unique_name_upd = generate_unique_name('ParameterApiUpd')
        # name, unit_id and flg_text cannot be updated
        parameter_upd = {
            PARAMETER: {
                'flg_available': False,
                'flg_logarithmic': True,
                'def_lower_deviation_value': 0.0,
                'def_upper_deviation_value': 10.2,
                'description': 'desc 01 updated!!!'
            }
        }

        res = self.cal_client.update_parameter_api(entry_id, parameter_upd)
        receive = self.load_response_content(res)

        # Add parameters not sent to the update API
        parameter_upd[PARAMETER]['unit_id'] = -1
        parameter_upd[PARAMETER]['name'] = expect['name']
        parameter_upd[PARAMETER]['flg_text'] = expect['flg_text']

        expect_upd = parameter_upd[PARAMETER]

        self.fields_validation(receive, expect_upd)
        assert res.status_code == HTTPStatus.OK

        assert expect['flg_available'] != expect_upd['flg_available']
        assert expect['flg_logarithmic'] != expect_upd['flg_logarithmic']
        assert expect['def_lower_deviation_value'] \
               != expect_upd['def_lower_deviation_value']
        assert expect['def_upper_deviation_value'] \
               != expect_upd['def_upper_deviation_value']
        assert expect['description'] != expect_upd['description']

    def __get_all_entries_by_name_api(self, name, expect,
                                      page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        response = self.cal_client.get_all_parameters_by_name_api(name, page, page_size)
        receive = self.get_and_validate_all_entries_by_name(response)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.cal_client.get_parameter_by_id_api(entry_id)
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)


if __name__ == '__main__':
    unittest.main()
