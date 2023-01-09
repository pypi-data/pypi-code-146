"""CalibrationConstantVersionApi class"""

import json

from ..common.base import Base
from ..common.config import *


class CalibrationConstantVersionApi(Base):
    def create_calibration_constant_version_api(self, ccv):
        api_url = self.__get_api_url()
        return self.api_post(api_url, data=json.dumps(ccv))

    #
    # Delete CalibrationConstantVersion instances is not allowed by the server,
    # and consequently this action isn't provided to the user!
    #
    # def delete_calibration_constant_version_api(self, ccv_id):
    #     api_url = self.__get_api_url(ccv_id)
    #     return self.api_delete(api_url)

    def update_calibration_constant_version_api(self, ccv_id, ccv):
        api_url = self.__get_api_url(ccv_id)
        return self.api_put(api_url, data=json.dumps(ccv))

    def get_calibration_constant_version_by_id_api(self, ccv_id):
        api_url = self.__get_api_url(ccv_id)
        return self.api_get(api_url, params={})

    def get_all_calibration_constant_versions_by_name_api(self, name,
                                                          page=DEF_PAGE,
                                                          page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'name': name,
                                             'page': page,
                                             'page_size': page_size})

    def get_calibration_constant_versions_by_detector_conditions_api(
            self,
            detector_identifier,
            calibration_id,
            condition,
            karabo_da='',
            event_at=None,
            pdu_snapshot_at=None):
        api_url = self.__get_api_url('get_by_detector_conditions')
        params = {'detector_identifier': detector_identifier,
                  'calibration_id': str(calibration_id),
                  'karabo_da': karabo_da,
                  'event_at': event_at,
                  'pdu_snapshot_at': pdu_snapshot_at}

        return self.api_get(api_url,
                            params=params,
                            data=json.dumps(condition))

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'calibration_constant_versions/'
        return self.get_api_url(model_name, api_specifics)
