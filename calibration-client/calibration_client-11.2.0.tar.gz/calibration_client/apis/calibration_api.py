"""CalibrationApi module class"""

import json

from ..common.base import Base
from ..common.config import *


class CalibrationApi(Base):
    def create_calibration_api(self, calibration):
        api_url = self.__get_api_url()
        return self.api_post(api_url, data=json.dumps(calibration))

    def delete_calibration_api(self, calibration_id):
        api_url = self.__get_api_url(calibration_id)
        return self.api_delete(api_url)

    def update_calibration_api(self, calibration_id, calibration):
        api_url = self.__get_api_url(calibration_id)
        return self.api_put(api_url, data=json.dumps(calibration))

    def get_calibration_by_id_api(self, calibration_id):
        api_url = self.__get_api_url(calibration_id)
        return self.api_get(api_url, params={})

    def get_all_calibrations_by_name_api(self, name,
                                         page=DEF_PAGE,
                                         page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'name': name,
                                             'page': page,
                                             'page_size': page_size})

    #
    def get_all_calibration_constants_by_conds_api(self, calibration_id,
                                                   dev_type_id, cond_ids):
        api_action_name = '/get_all_calibration_constants'
        api_relative_url = '{0}{1}'.format(calibration_id, api_action_name)
        api_url = self.__get_api_url(api_relative_url)

        params = {'calibration_id': str(calibration_id),
                  'detector_type_id': str(dev_type_id),
                  'condition_ids': str(cond_ids)}

        return self.api_get(api_url, params=params)

    #
    def get_calibration_constant_by_uk_api(self, calibration_id,
                                           dev_type_id, cond_id):
        api_action_name = '/get_calibration_constant'
        api_relative_url = '{0}{1}'.format(calibration_id, api_action_name)
        api_url = self.__get_api_url(api_relative_url)

        params = {'calibration_id': str(calibration_id),
                  'detector_type_id': str(dev_type_id),
                  'condition_id': str(cond_id)}

        return self.api_get(api_url, params=params)

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'calibrations/'
        return self.get_api_url(model_name, api_specifics)
