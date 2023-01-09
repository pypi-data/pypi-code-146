"""DetectorTypeApi module class"""

import json

from ..common.base import Base
from ..common.config import *


class DetectorTypeApi(Base):
    def create_detector_type_api(self, detector_type):
        api_url = self.__get_api_url()
        return self.api_post(api_url, data=json.dumps(detector_type))

    def delete_detector_type_api(self, detector_type_id):
        api_url = self.__get_api_url(detector_type_id)
        return self.api_delete(api_url)

    def update_detector_type_api(self, detector_type_id, detector_type):
        api_url = self.__get_api_url(detector_type_id)
        return self.api_put(api_url, data=json.dumps(detector_type))

    def get_detector_type_by_id_api(self, parameter_id):
        api_url = self.__get_api_url(parameter_id)
        return self.api_get(api_url, params={})

    def get_all_detector_types_by_name_api(self, name,
                                           page=DEF_PAGE,
                                           page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'name': name,
                                             'page': page,
                                             'page_size': page_size})

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'detector_types/'
        return self.get_api_url(model_name, api_specifics)
