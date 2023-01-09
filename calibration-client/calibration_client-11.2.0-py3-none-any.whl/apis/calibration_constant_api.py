"""CalibrationConstantApi class"""

import json

from ..common.base import Base
from ..common.config import *


class CalibrationConstantApi(Base):
    def create_calibration_constant_api(self, cal_constant):
        api_url = self.__get_api_url()
        return self.api_post(api_url, data=json.dumps(cal_constant))

    def delete_calibration_constant_api(self, cal_constant_id):
        api_url = self.__get_api_url(cal_constant_id)
        return self.api_delete(api_url)

    def update_calibration_constant_api(self, cal_constant_id, cal_constant):
        api_url = self.__get_api_url(cal_constant_id)
        return self.api_put(api_url, data=json.dumps(cal_constant))

    def get_calibration_constant_by_id_api(self, cal_constant_id):
        api_url = self.__get_api_url(cal_constant_id)
        return self.api_get(api_url, params={})

    def get_all_calibration_constants_by_name_api(self, name,
                                                  page=DEF_PAGE,
                                                  page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'name': name,
                                             'page': page,
                                             'page_size': page_size})

    #
    def get_calibration_constant_version_by_uk_api(self,
                                                   calibration_constant_id,
                                                   physical_detector_unit_id,
                                                   event_at,
                                                   snapshot_at):
        api_action_name = '/get_version'
        api_relative_url = '{0}{1}'.format(calibration_constant_id,
                                           api_action_name)
        api_url = self.__get_api_url(api_relative_url)

        params = {'physical_detector_unit_id': str(physical_detector_unit_id),
                  'event_at': event_at,
                  'snapshot_at': snapshot_at}

        return self.api_get(api_url, params=params)

    #
    def get_prior_in_time_calibration_constant_version_api(self,
                                                           calibration_constant_ids,
                                                           physical_detector_unit_id,
                                                           event_at,
                                                           snapshot_at):
        api_action_name = '/get_prior_in_time_version'
        api_relative_url = '{0}{1}'.format(calibration_constant_ids[0],
                                           api_action_name)
        api_url = self.__get_api_url(api_relative_url)

        params = {'calibration_constant_ids': str(calibration_constant_ids),
                  'physical_detector_unit_id': str(physical_detector_unit_id),
                  'event_at': event_at,
                  'snapshot_at': snapshot_at}

        return self.api_get(api_url, params=params)

    #
    def get_closest_calibration_constant_version_api(self,
                                                     calibration_constant_ids,
                                                     physical_detector_unit_id,
                                                     event_at,
                                                     snapshot_at):
        api_action_name = '/get_closest_version'
        api_relative_url = '{0}{1}'.format(calibration_constant_ids[0],
                                           api_action_name)
        api_url = self.__get_api_url(api_relative_url)

        params = {'calibration_constant_ids': str(calibration_constant_ids),
                  'physical_detector_unit_id': str(physical_detector_unit_id),
                  'event_at': event_at,
                  'snapshot_at': snapshot_at}

        return self.api_get(api_url, params=params)

    #
    def get_closest_calibration_constant_version_by_detector_api(
            self, calibration_constant_ids, detector_id, karabo_da,
            event_at, snapshot_at):
        api_action_name = '/get_closest_version_by_detector'
        api_relative_url = '{0}{1}'.format(calibration_constant_ids[0],
                                           api_action_name)
        api_url = self.__get_api_url(api_relative_url)

        params = {'calibration_constant_ids': str(calibration_constant_ids),
                  'detector_id': str(detector_id),
                  'karabo_da': str(karabo_da),
                  'event_at': event_at,
                  'snapshot_at': snapshot_at}

        return self.api_get(api_url, params=params)

    #
    def get_all_calibration_constant_versions_api(self,
                                                  calibration_constant_ids,
                                                  physical_detector_unit_id,
                                                  event_at,
                                                  snapshot_at):
        api_action_name = '/get_all_versions'
        api_relative_url = '{0}{1}'.format(calibration_constant_ids[0],
                                           api_action_name)
        api_url = self.__get_api_url(api_relative_url)

        params = {'calibration_constant_ids': str(calibration_constant_ids),
                  'physical_detector_unit_id': str(physical_detector_unit_id),
                  'event_at': event_at,
                  'snapshot_at': snapshot_at}

        return self.api_get(api_url, params=params)

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'calibration_constants/'
        return self.get_api_url(model_name, api_specifics)
