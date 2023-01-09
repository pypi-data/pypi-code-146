"""Condition module class"""

import logging
from datetime import datetime
from http import HTTPStatus

from ..common.base import Base
from ..common.config import *
from ..common.util import Util

MODULE_NAME = CONDITION


class Condition:
    def __init__(self, calibration_client, name, flg_available, event_at,
                 parameters_conditions_attributes, description=''):
        self.calibration_client = calibration_client
        self.id = None
        self.name = name
        self.flg_available = flg_available

        if event_at is None:
            self.event_at = datetime.today()
        else:
            self.event_at = event_at

        self.parameters_conditions_attributes = parameters_conditions_attributes  # noqa
        self.description = description

    def set_expected(self):
        cal_client = self.calibration_client
        response = cal_client.set_expected_condition(self.__get_resource())

        if response.status_code == HTTPStatus.CREATED:
            Base.cal_debug(MODULE_NAME, CREATE, response)
            res = Base.format_response(
                response, CREATE, HTTPStatus.CREATED, MODULE_NAME
            )

            if res['success']:
                self.id = res['data']['id']

        else:
            Base.cal_debug(MODULE_NAME, 'GET >> set_expected', response)
            res = Base.format_response(
                response, GET, HTTPStatus.OK, MODULE_NAME
            )

        return res

    # return the list of possible conditions order by the time distance
    # between the condition mesurement and the received event_at datetime
    def get_possible(self):
        cal_client = self.calibration_client
        response = cal_client.get_possible_conditions(self.__get_resource())

        Base.cal_debug(MODULE_NAME, 'get_possible', response)
        return Base.format_response(response, GET, HTTPStatus.OK, MODULE_NAME)

    def get_expected(self):
        cal_client = self.calibration_client
        response = cal_client.get_expected_condition(self.__get_resource())

        Base.cal_debug(MODULE_NAME, 'get_expected', response)
        return Base.format_response(response, GET, HTTPStatus.OK, MODULE_NAME)

    @staticmethod
    def set_condition_from_dict(cal_client, condition_h):
        new_cond = Condition(
            calibration_client=cal_client,
            name=condition_h['name'],
            flg_available=condition_h['flg_available'],
            event_at=None,
            parameters_conditions_attributes=condition_h[
                'parameters_conditions_attributes'],
            description=condition_h['description']
        )

        resp = new_cond.set_expected()
        logging.debug('Build condition successfully: {0}'.format(resp))

        return resp

    def __get_resource(self):
        condition = {
            CONDITION: {
                'name': self.name,
                'flg_available': self.flg_available,
                'event_at': Util.datetime_converter(self.event_at),
                'parameters_conditions_attributes':
                    self.parameters_conditions_attributes,
                'description': self.description
            }
        }

        return condition
