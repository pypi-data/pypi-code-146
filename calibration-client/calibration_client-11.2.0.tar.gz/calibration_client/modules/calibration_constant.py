"""CalibrationConstant module class"""

import logging
from http import HTTPStatus

from ..common.base import Base
from ..common.config import *

MODULE_NAME = CALIBRATION_CONSTANT


class CalibrationConstant:
    def __init__(self, calibration_client,
                 name, calibration_id, detector_type_id, condition_id,
                 flg_available, flg_auto_approve,
                 description=''):
        self.calibration_client = calibration_client
        self.id = None
        self.name = name
        self.calibration_id = calibration_id
        self.detector_type_id = detector_type_id
        self.condition_id = condition_id
        self.flg_available = flg_available
        self.flg_auto_approve = flg_auto_approve
        self.description = description

    def create(self):
        cal_client = self.calibration_client
        response = cal_client.create_calibration_constant_api(
            self.__get_resource())

        Base.cal_debug(MODULE_NAME, CREATE, response)
        res = Base.format_response(
            response, CREATE, HTTPStatus.CREATED, MODULE_NAME
        )

        if res['success']:
            self.id = res['data']['id']

        return res

    def delete(self):
        cal_client = self.calibration_client
        response = cal_client.delete_calibration_constant_api(self.id)
        Base.cal_debug(MODULE_NAME, DELETE, response)

        return Base.format_response(
            response, DELETE, HTTPStatus.NO_CONTENT, MODULE_NAME
        )

    def update(self):
        cal_client = self.calibration_client
        response = cal_client.update_calibration_constant_api(
            self.id,
            self.__get_resource()
        )

        Base.cal_debug(MODULE_NAME, UPDATE, response)
        return Base.format_response(
            response, UPDATE, HTTPStatus.OK, MODULE_NAME
        )

    @staticmethod
    def create_from_dict(cal_client, cc):
        new_cc = CalibrationConstant(calibration_client=cal_client,
                                     name=cc['name'],
                                     calibration_id=cc['calibration_id'],
                                     detector_type_id=cc['detector_type_id'],
                                     condition_id=cc['condition_id'],
                                     flg_auto_approve=cc['flg_auto_approve'],
                                     flg_available=cc['flg_available'],
                                     description=cc['description'])

        resp = new_cc.create()
        return resp

    @staticmethod
    def set_from_dict(cal_client, cc):
        resp = CalibrationConstant.get_by_uk(cal_client,
                                             cc['calibration_id'],
                                             cc['detector_type_id'],
                                             cc['condition_id'])

        if resp['success']:
            logging.debug('Got already existent calibration_constant')
        else:
            logging.debug('calibration_constant does not exist')
            resp = CalibrationConstant.create_from_dict(cal_client, cc)

        return resp

    @staticmethod
    def delete_by_id(cal_client, cc_id):
        resp = cal_client.delete_calibration_constant_api(cc_id)
        Base.cal_debug(MODULE_NAME, DELETE, resp)

        return Base.format_response(
            resp, DELETE, HTTPStatus.NO_CONTENT, MODULE_NAME
        )

    @staticmethod
    def get_by_id(cal_client, calibration_constant_id):
        response = cal_client.get_calibration_constant_by_id_api(
            calibration_constant_id)

        Base.cal_debug(MODULE_NAME, 'get_by_id', response)
        return Base.format_response(response, GET, HTTPStatus.OK, MODULE_NAME)

    @staticmethod
    def get_all_by_name(cal_client, name, page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        response = cal_client.get_all_calibration_constants_by_name_api(name, page, page_size)

        Base.cal_debug(MODULE_NAME, 'get_all_by_name', response)
        return Base.format_response(response, GET, HTTPStatus.OK, MODULE_NAME)

    @staticmethod
    def get_by_name(cal_client, name):
        res = CalibrationConstant.get_all_by_name(cal_client, name)

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

    @staticmethod
    def get_all_by_conditions(cal_client, calibration_id, detector_type_id,
                              condition_ids):
        res = cal_client.get_all_calibration_constants_by_conds_api(
            calibration_id, detector_type_id, condition_ids)

        Base.cal_debug(MODULE_NAME,
                       'cc >> get_all_calibration_constants_by_conds_api',
                       res)
        return Base.format_response(res, GET, HTTPStatus.OK, MODULE_NAME)

    @staticmethod
    def get_by_uk(cal_client, calibration_id, detector_type_id, condition_id):
        res = cal_client.get_calibration_constant_by_uk_api(calibration_id,
                                                            detector_type_id,
                                                            condition_id)

        Base.cal_debug(MODULE_NAME, 'cc >> get_by_uk', res)
        return Base.format_response(res, GET, HTTPStatus.OK, MODULE_NAME)

    def __get_resource(self):
        calibration_constant = {
            CALIBRATION_CONSTANT: {
                'name': self.name,
                'calibration_id': self.calibration_id,
                'detector_type_id': self.detector_type_id,
                'condition_id': self.condition_id,
                'flg_available': self.flg_available,
                'flg_auto_approve': self.flg_auto_approve,
                'description': self.description
            }
        }

        return calibration_constant
