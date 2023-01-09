"""DetectorApi module class"""

import json

from ..common.base import Base
from ..common.config import *


class DetectorApi(Base):
    def create_detector_api(self, detector):
        api_url = self.__get_api_url()
        return self.api_post(api_url, data=json.dumps(detector))

    def delete_detector_api(self, detector_id):
        api_url = self.__get_api_url(detector_id)
        return self.api_delete(api_url)

    def update_detector_api(self, detector_id, detector):
        api_url = self.__get_api_url(detector_id)
        return self.api_put(api_url, data=json.dumps(detector))

    def get_detector_by_id_api(self, parameter_id):
        api_url = self.__get_api_url(parameter_id)
        return self.api_get(api_url, params={})

    def get_all_detectors_by_name_api(self, name,
                                      page=DEF_PAGE,
                                      page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'name': name,
                                             'page': page,
                                             'page_size': page_size})

    def get_all_detectors_by_identifier_api(self, identifier):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'identifier': identifier})

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'detectors/'
        return self.get_api_url(model_name, api_specifics)
