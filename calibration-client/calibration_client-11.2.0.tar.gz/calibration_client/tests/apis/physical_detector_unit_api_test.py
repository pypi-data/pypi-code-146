"""PhysicalDetectorUnitApiTest class"""

import unittest
from http import HTTPStatus

import pytest

from .api_base import ApiBase
from ..common.config_test import *
from ..common.generators import generate_unique_name


@pytest.mark.usefixtures('client_cls')
class PhysicalDetectorUnitApiTest(ApiBase, unittest.TestCase):
    def test_create_physical_detector_unit_api(self):
        __unique_name = generate_unique_name('PhysicalDetectorUnitApi')
        physical_detector_unit = {
            PHYSICAL_DETECTOR_UNIT: {
                'physical_name': __unique_name,
                'karabo_da': __unique_name,
                'virtual_device_name': __unique_name,
                'detector_type_id': -1,
                'detector_id': -1,
                'uuid': 1000000000,
                'flg_available': True,
                'description': 'desc 01'
            }
        }

        expect = physical_detector_unit[PHYSICAL_DETECTOR_UNIT]

        # Create new entry (should succeed)
        received = self.__create_entry_api(physical_detector_unit, expect)

        physical_dev_id = received['id']
        pdu_phy_name = received['physical_name']
        physical_dev_det_id = received['detector_id']
        physical_dev_krb_da = received['karabo_da']

        try:
            # Create duplicated entry (should throw an error)
            self.__create_error_entry_uk_api(physical_detector_unit)

            # Get entry by name
            self.__get_all_entries_by_name_api(pdu_phy_name, expect)

            # Get entry by detector_id
            self.__get_all_entries_by_detector_id_api(physical_dev_det_id,
                                                      expect)

            # Get entry by detector_id
            self.__get_all_entries_by_detector_and_krbda_api(
                physical_dev_det_id, physical_dev_krb_da, expect)

            # Get entry by ID
            self.__get_entry_by_id_api(physical_dev_id, expect)

            # Put entry information (update some fields should succeed)
            self.__update_entry_api(physical_dev_id, expect)

        finally:
            # Delete entry (should succeed)
            # (test purposes only to keep the DB clean)
            del_resp = self.cal_client.delete_physical_detector_unit_api(
                physical_dev_id
            )

        # Validate the response from deletion if nothing already error-ed
        self.get_and_validate_delete_entry_by_id(del_resp)

    def fields_validation(self, receive, expect):
        assert receive['physical_name'] == expect['physical_name']
        assert receive['karabo_da'] == expect['karabo_da']
        assert receive['uuid'] == expect['uuid']
        assert receive['virtual_device_name'] == expect['virtual_device_name']
        assert receive['detector_type_id'] == expect['detector_type_id']
        assert receive['detector_id'] == expect['detector_id']
        assert receive['flg_available'] == expect['flg_available']
        assert receive['description'] == expect['description']

    def __create_entry_api(self, entry_info, expect):
        resp = self.cal_client.create_physical_detector_unit_api(entry_info)
        receive = self.get_and_validate_create_entry(resp)
        self.fields_validation(receive, expect)
        return receive

    def __create_error_entry_uk_api(self, entry_info):
        resp = self.cal_client.create_physical_detector_unit_api(entry_info)
        receive = self.load_response_content(resp)

        expect = {'info': {'physical_name': ['has already been taken'],
                           'karabo_da': ['has already been taken'],
                           'uuid': ['has already been taken']}}
        assert receive == expect
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def __update_entry_api(self, entry_id, expect):
        unique_name_upd = generate_unique_name('PhysicalDevApiUpd')
        physical_dev_upd = {
            PHYSICAL_DETECTOR_UNIT: {
                'physical_name': expect['physical_name'],
                'karabo_da': unique_name_upd,
                'virtual_device_name': unique_name_upd,
                'uuid': expect['uuid'],
                # 'detector_type_id': '-1',
                # 'detector_id': '-1',
                'flg_available': False,
                'description': 'desc 01 updated!!!'
            }
        }

        resp = self.cal_client.update_physical_detector_unit_api(
            entry_id, physical_dev_upd)
        receive = self.load_response_content(resp)

        # Add parameters not send to the update API
        physical_dev_upd[PHYSICAL_DETECTOR_UNIT]['detector_type_id'] = -1
        physical_dev_upd[PHYSICAL_DETECTOR_UNIT]['detector_id'] = -1
        expect_upd = physical_dev_upd[PHYSICAL_DETECTOR_UNIT]

        self.fields_validation(receive, expect_upd)
        assert resp.status_code == HTTPStatus.OK

        # assert expect['physical_name'] != expect_upd['physical_name']
        assert expect['karabo_da'] != expect_upd['karabo_da']
        assert expect['virtual_device_name'] != expect_upd[
            'virtual_device_name']
        assert expect['flg_available'] != expect_upd['flg_available']
        assert expect['description'] != expect_upd['description']

    def __get_all_entries_by_name_api(self, physical_name, expect,
                                      page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        resp = self.cal_client.get_all_physical_detector_units_by_physical_name_api(physical_name,
                                                                                    page, page_size)  # noqa
        receive = self.get_and_validate_all_entries_by_name(resp)
        self.fields_validation(receive, expect)

    def __get_all_entries_by_detector_id_api(self, detector_id, expect):
        resp = self.cal_client.get_all_physical_detector_units_by_detector_id_api(detector_id)  # noqa
        receive = self.get_and_validate_all_entries_by_name(resp)

        self.fields_validation(receive, expect)

    def __get_all_entries_by_detector_and_krbda_api(self, detector_id,
                                                    karabo_da, expect):
        resp = self.cal_client.get_all_physical_detector_units_by_det_and_krbda_api(detector_id, karabo_da)  # noqa
        receive = self.get_and_validate_all_entries_by_name(resp)
        self.fields_validation(receive, expect)

    def __get_entry_by_id_api(self, entry_id, expect):
        response = self.cal_client.get_physical_detector_unit_by_id_api(entry_id)  # noqa
        receive = self.get_and_validate_entry_by_id(response)
        self.fields_validation(receive, expect)


if __name__ == '__main__':
    unittest.main()
