"""Parameter module class"""

from http import HTTPStatus

from ..common.base import Base
from ..common.config import *

MODULE_NAME = PARAMETER


class Parameter:
    def __init__(self, calibration_client,
                 name, unit_id, flg_available, flg_logarithmic, flg_text,
                 def_lower_deviation_value, def_upper_deviation_value,
                 description=''):
        self.calibration_client = calibration_client
        self.id = None
        self.name = name
        self.unit_id = unit_id
        self.flg_available = flg_available
        self.flg_logarithmic = flg_logarithmic
        self.flg_text = flg_text
        self.def_lower_deviation_value = def_lower_deviation_value
        self.def_upper_deviation_value = def_upper_deviation_value
        self.description = description

    def create(self):
        cal_client = self.calibration_client
        response = cal_client.create_parameter_api(self.__get_resource())

        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(
            response, CREATE, HTTPStatus.CREATED, MODULE_NAME
        )

        if res['success']:
            self.id = res['data']['id']

        return res

    def delete(self):
        cal_client = self.calibration_client
        response = cal_client.delete_parameter_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)

        return Base.format_response(
            response, DELETE, HTTPStatus.NO_CONTENT, MODULE_NAME
        )

    def update(self):
        cal_client = self.calibration_client
        response = cal_client.update_parameter_api(self.id,
                                                   self.__get_resource())

        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(
            response, UPDATE, HTTPStatus.OK, MODULE_NAME
        )

    @staticmethod
    def get_by_id(cal_client, parameter_id):
        response = cal_client.get_parameter_by_id_api(parameter_id)

        Base.cal_debug(MODULE_NAME, 'get_by_id', response)
        return Base.format_response(response, GET, HTTPStatus.OK, MODULE_NAME)

    @staticmethod
    def get_all_by_name(cal_client, name, page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        response = cal_client.get_all_parameters_by_name_api(name, page, page_size)

        Base.cal_debug(MODULE_NAME, 'get_all_by_name', response)
        return Base.format_response(response, GET, HTTPStatus.OK, MODULE_NAME)

    @staticmethod
    def get_by_name(cal_client, name):
        res = Parameter.get_all_by_name(cal_client, name)

        if res['success']:
            if res['data'] == []:
                resp_data = []
            else:
                resp_data = res['data'][0]

            res = {'success': res['success'],
                   'info': res['info'],
                   'app_info': res['app_info'],
                   'data': resp_data}

        return res

    def __get_resource(self):
        parameter = {
            PARAMETER: {
                'name': self.name,
                'unit_id': self.unit_id,
                'flg_available': self.flg_available,
                'flg_logarithmic': self.flg_logarithmic,
                'flg_text': self.flg_text,
                'def_lower_deviation_value': self.def_lower_deviation_value,
                'def_upper_deviation_value': self.def_upper_deviation_value,
                'description': self.description
            }
        }

        return parameter
