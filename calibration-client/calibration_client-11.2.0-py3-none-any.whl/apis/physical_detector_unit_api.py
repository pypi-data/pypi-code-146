"""PhysicalDetectorUnitApi module class"""

import json

from ..common.base import Base
from ..common.config import *


class PhysicalDetectorUnitApi(Base):
    def create_physical_detector_unit_api(self, physical_detector_unit):
        api_url = self.__get_api_url()
        return self.api_post(api_url, data=json.dumps(physical_detector_unit))

    def delete_physical_detector_unit_api(self, physical_detector_unit_id):
        api_url = self.__get_api_url(physical_detector_unit_id)
        return self.api_delete(api_url)

    def update_physical_detector_unit_api(self, physical_detector_unit_id,
                                          physical_detector_unit):
        api_url = self.__get_api_url(physical_detector_unit_id)
        return self.api_put(api_url, data=json.dumps(physical_detector_unit))

    def get_physical_detector_unit_by_id_api(self, physical_detector_unit_id):
        api_url = self.__get_api_url(physical_detector_unit_id)
        return self.api_get(api_url, params={})

    def get_all_physical_detector_units_by_physical_name_api(self, name,
                                                             page=DEF_PAGE,
                                                             page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'physical_name': name,
                                             'page': page,
                                             'page_size': page_size})

    def get_all_physical_detector_units_by_detector_id_api(self, detector_id,
                                                           page=DEF_PAGE,
                                                           page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'detector_id': detector_id,
                                             'page': page,
                                             'page_size': page_size})

    def get_all_physical_detector_units_by_det_and_krbda_api(self,
                                                             detector_id,
                                                             karabo_da,
                                                             page=DEF_PAGE,
                                                             page_size=DEF_PAGE_SIZE):
        api_url = self.__get_api_url()
        return self.api_get(api_url, params={'detector_id': detector_id,
                                             'karabo_da': karabo_da,
                                             'page': page,
                                             'page_size': page_size})

    #
    def get_all_by_detector_api(self, detector_id, pdu_snapshot_at):
        api_action_name = '/get_all_by_detector'
        api_url = self.__get_api_url(api_action_name)

        params = {'detector_id': str(detector_id),
                  'pdu_snapshot_at': pdu_snapshot_at}

        return self.api_get(api_url, params=params)

    #
    # Private Methods
    #
    def __get_api_url(self, api_specifics=''):
        model_name = 'physical_detector_units/'
        return self.get_api_url(model_name, api_specifics)
