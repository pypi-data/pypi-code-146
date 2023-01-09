"""Report module class"""

from http import HTTPStatus

from ..common.base import Base
from ..common.config import *

MODULE_NAME = REPORT


class Report:
    def __init__(self, calibration_client,
                 name, file_path, flg_available, description=''):
        self.calibration_client = calibration_client
        self.id = None
        self.name = name
        self.file_path = file_path
        self.flg_available = flg_available
        self.description = description

    def create(self):
        cal_client = self.calibration_client
        response = cal_client.create_report_api(self.__get_resource())

        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(
            response, CREATE, HTTPStatus.CREATED, MODULE_NAME
        )

        if res['success']:
            self.id = res['data']['id']

        return res

    def set(self):
        cal_client = self.calibration_client
        response = cal_client.set_report_api(self.__get_resource())

        Base.cal_debug(MODULE_NAME, SET, response)
        res = Base.format_response(
            response, SET, HTTPStatus.CREATED, MODULE_NAME
        )

        if res['success']:
            self.id = res['data']['id']

        return res

    def delete(self):
        cal_client = self.calibration_client
        response = cal_client.delete_report_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)

        return Base.format_response(
            response, DELETE, HTTPStatus.NO_CONTENT, MODULE_NAME
        )

    def update(self):
        cal_client = self.calibration_client
        response = cal_client.update_report_api(self.id,
                                                self.__get_resource())

        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(
            response, UPDATE, HTTPStatus.OK, MODULE_NAME
        )

    @staticmethod
    def get_by_id(cal_client, report_id):
        response = cal_client.get_report_by_id_api(report_id)

        Base.cal_debug(MODULE_NAME, 'get_by_id', response)
        return Base.format_response(response, GET, HTTPStatus.OK, MODULE_NAME)

    @staticmethod
    def get_all_by_name(cal_client, name, page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        response = cal_client.get_all_reports_by_name_api(name, page, page_size)

        Base.cal_debug(MODULE_NAME, 'get_all_by_name', response)
        return Base.format_response(response, GET, HTTPStatus.OK, MODULE_NAME)

    @staticmethod
    def get_all_by_name_and_file_path(cal_client, name, file_path,
                                      page=DEF_PAGE, page_size=DEF_PAGE_SIZE):

        resp = cal_client.get_all_reports_by_name_and_file_path_api(name,
                                                                    file_path,
                                                                    page,
                                                                    page_size)

        Base.cal_debug(MODULE_NAME, 'get_all_by_name_and_file_path', resp)
        return Base.format_response(resp, GET, HTTPStatus.OK, MODULE_NAME)

    @staticmethod
    def get_by_name_and_file_path(cal_client, name, file_path):
        res = Report.get_all_by_name_and_file_path(cal_client, name, file_path)

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
        report = {
            REPORT: {
                'name': self.name,
                'file_path': self.file_path,
                'flg_available': self.flg_available,
                'description': self.description
            }
        }

        return report
