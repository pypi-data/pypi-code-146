"""PhysicalDetectorUnit module class"""

from http import HTTPStatus

from ..common.base import Base
from ..common.config import *

MODULE_NAME = PHYSICAL_DETECTOR_UNIT


class PhysicalDetectorUnit:
    def __init__(self, calibration_client,
                 physical_name, karabo_da, virtual_device_name,
                 uuid, detector_type_id, detector_id,
                 flg_available, description=''):
        self.calibration_client = calibration_client
        self.id = None
        self.physical_name = physical_name
        self.karabo_da = karabo_da
        self.virtual_device_name = virtual_device_name
        self.uuid = uuid
        self.detector_type_id = detector_type_id
        self.detector_id = detector_id
        self.flg_available = flg_available
        self.description = description

    def create(self):
        cal_client = self.calibration_client
        response = cal_client.create_physical_detector_unit_api(
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
        response = cal_client.delete_physical_detector_unit_api(self.id)

        Base.cal_debug(MODULE_NAME, DELETE, response)
        return Base.format_response(
            response, DELETE, HTTPStatus.NO_CONTENT, MODULE_NAME
        )

    def update(self):
        cal_client = self.calibration_client
        resp = cal_client.update_physical_detector_unit_api(
            self.id, self.__get_resource())

        Base.cal_debug(MODULE_NAME, UPDATE, resp)
        return Base.format_response(
            resp, UPDATE, HTTPStatus.OK, MODULE_NAME
        )

    @staticmethod
    def get_by_id(cal_client, physical_detector_unit_id):
        response = cal_client.get_physical_detector_unit_by_id_api(
            physical_detector_unit_id)

        Base.cal_debug(MODULE_NAME, 'get_by_id', response)
        return Base.format_response(response, GET, HTTPStatus.OK, MODULE_NAME)

    @staticmethod
    def get_all_by_name(cal_client, physical_name,
                        page=DEF_PAGE, page_size=DEF_PAGE_SIZE):

        resp = cal_client.get_all_physical_detector_units_by_physical_name_api(
            physical_name, page, page_size)

        Base.cal_debug(MODULE_NAME, 'get_all_by_name', resp)
        return Base.format_response(resp, GET, HTTPStatus.OK, MODULE_NAME)

    @staticmethod
    def get_all_by_detector_id(cal_client, det_id,
                               page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        resp = cal_client.get_all_physical_detector_units_by_detector_id_api(
            det_id, page, page_size)

        Base.cal_debug(MODULE_NAME, 'get_all_by_detector_id', resp)
        return Base.format_response(resp, GET, HTTPStatus.OK, MODULE_NAME)

    @staticmethod
    def get_all_by_detector_and_karabo_da(cal_client, det_id, krb_da,
                                          page=DEF_PAGE, page_size=DEF_PAGE_SIZE):

        resp = cal_client.get_all_physical_detector_units_by_det_and_krbda_api(
            det_id,
            krb_da,
            page,
            page_size)

        Base.cal_debug(MODULE_NAME, 'get_all_by_detector_and_karabo_da', resp)
        return Base.format_response(resp, GET, HTTPStatus.OK, MODULE_NAME)

    @staticmethod
    def get_all_by_detector(cal_client, detector_id, pdu_snapshot_at):
        resp = cal_client.get_all_by_detector_api(detector_id, pdu_snapshot_at)

        Base.cal_debug(MODULE_NAME, 'ccv >> get_all_by_detector', resp)
        return Base.format_response(resp, GET, HTTPStatus.OK, MODULE_NAME)

    @staticmethod
    def get_by_name(cal_client, physical_name):
        res = PhysicalDetectorUnit.get_all_by_name(cal_client, physical_name)

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
        physical_detector_unit = {
            PHYSICAL_DETECTOR_UNIT: {
                'physical_name': self.physical_name,
                'karabo_da': self.karabo_da,
                'virtual_device_name': self.virtual_device_name,
                'uuid': self.uuid,
                'detector_type_id': self.detector_type_id,
                'detector_id': self.detector_id,
                'flg_available': self.flg_available,
                'description': self.description
            }
        }

        return physical_detector_unit
