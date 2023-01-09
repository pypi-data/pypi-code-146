"""ConditionTest class"""

import unittest

import pytest

from .module_base import ModuleBase
from ..common.config_test import CONDITION, RESOURCE_NOT_FOUND
from ..common.generators import generate_unique_name
from ...modules.condition import Condition

MODULE_NAME = CONDITION


@pytest.mark.usefixtures('client_cls')
class ConditionTest(ModuleBase, unittest.TestCase):
    def setUp(self):
        __parameters_conditions_attr_01 = [
            {
                'parameter_id': -1,
                'value': 2.5,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5,
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests'
            },
            {
                'parameter_id': -2,
                'value': 1.5,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5,
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests'
            }
        ]

        __parameters_conditions_attr_02 = [
            {
                'parameter_id': -1,
                'value': 2.4,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5,
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests'
            },
            {
                'parameter_id': -2,
                'value': 1.3,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5,
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests'
            }
        ]

        __parameters_conditions_attr_03 = [
            {
                'parameter_id': -1,
                'value': 2.7,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5,
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests'
            },
            {
                'parameter_id': -2,
                'value': 1.8,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5,
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests'
            }
        ]

        __parameters_conditions_attr_02 = [
            {
                'parameter_id': -1,
                'value': 2.4,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5,
                'flg_available': True,
                'description': 'Created automatically via seed:see_tests'
            },
            {
                'parameter_id': -2,
                'value': 1.3,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5,
                'flg_available': True,
                'description': 'Created automatically via seed:see_tests'
            }
        ]

        __parameters_conditions_attr_03 = [
            {
                'parameter_id': -1,
                'value': 2.7,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5,
                'flg_available': True,
                'description': 'Created automatically via seed:see_tests'
            },
            {
                'parameter_id': -2,
                'value': 1.8,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5,
                'flg_available': True,
                'description': 'Created automatically via seed:see_tests'
            }
        ]

        __unique_name = 'CONDITION_TEST-1_DO_NOT_DELETE'

        self.cond_01 = {
            'name': __unique_name,
            'flg_available': True,
            'event_at': '2019-07-20 09:14:52',
            'description': 'Created automatically via seed:seed_tests',
            'parameters_conditions_attributes': __parameters_conditions_attr_01
        }

        self.cond_02 = {
            'name': 'CONDITION_TEST-2_DO_NOT_DELETE',
            'flg_available': True,
            'event_at': '2019-07-20 09:14:52',
            'description': 'Created automatically via seed:seed_tests',
            'parameters_conditions_attributes': __parameters_conditions_attr_02
        }

        self.cond_03 = {
            'name': 'CONDITION_TEST-3_DO_NOT_DELETE',
            'flg_available': True,
            'event_at': '2019-07-20 09:14:52',
            'description': 'Created automatically via seed:seed_tests',
            'parameters_conditions_attributes': __parameters_conditions_attr_03
        }

        __unique_name_upd = generate_unique_name('ConditionUpd01')
        self.cond_01_upd = {
            'name': __unique_name,
            'flg_available': True,
            'event_at': '2019-07-20 09:14:52',
            'description': 'Created automatically via seed:seed_tests',
            'parameters_conditions_attributes': __parameters_conditions_attr_01
        }

    def test_create_condition(self):
        cond_01 = Condition(
            calibration_client=self.cal_client,
            name=self.cond_01['name'],
            flg_available=self.cond_01['flg_available'],
            event_at=None,
            parameters_conditions_attributes=self.cond_01[
                'parameters_conditions_attributes'],
            description=self.cond_01['description']
        )

        #
        # Set Condition (should succeed with existent)
        #
        result1 = cond_01.set_expected()
        self.assert_find_success(MODULE_NAME, result1, self.cond_01)

        condition = result1['data']
        condition_id = result1['data']['id']
        condition_name = result1['data']['name']

        #
        # Set duplicated Condition (should succeed with existent)
        #
        cond_01_dup = cond_01
        result2 = cond_01_dup.set_expected()
        self.assert_find_success(MODULE_NAME, result2, self.cond_01)

        #
        # Get expected
        #
        result3 = cond_01.get_expected()
        self.assert_find_success(MODULE_NAME, result3, self.cond_01)

        #
        # Get possible
        #
        res4 = cond_01.get_possible()
        possible_conditions_list = [self.cond_03, self.cond_02, self.cond_01]
        self.assert_find_success(MODULE_NAME, res4, possible_conditions_list)

        #
        # Get entry with non-existent Condition (should throw an error)
        #
        cond_01.parameters_conditions_attributes[0]['value'] = '200'

        result5 = cond_01.get_expected()
        self.assert_find_error(MODULE_NAME, result5, RESOURCE_NOT_FOUND)

    def test_create_condition_from_dict_success(self):
        __parameters_01 = [
            {
                'parameter_id': -1,
                'value': 2.5,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5,
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests'
            },
            {
                'parameter_id': -2,
                'value': 1.5,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5,
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests'
            }
        ]

        __unique_name = 'CONDITION_TEST-1_DO_NOT_DELETE'

        cond_dict = {
            'name': __unique_name,
            'flg_available': True,
            'description': 'Created automatically via seed:seed_tests',
            'parameters_conditions_attributes': __parameters_01
        }

        #
        # Set Condition from DICT (should succeed with existent)
        #
        resp = Condition.set_condition_from_dict(self.cal_client, cond_dict)

        expect = {'id': -1,
                  'flg_available': True,
                  'name': 'CONDITION_TEST-1_DO_NOT_DELETE',
                  'description': 'Created automatically via seed:seed_tests',
                  'num_parameters': 2}

        msg = 'Got {0} successfully'.format(MODULE_NAME)
        expect = {'success': True, 'info': msg, 'app_info': {}, 'data': expect}

        assert resp['app_info'] == {}
        assert resp['info'] == expect['info']
        assert resp['success'] == expect['success']

        # Validate all 'data' fields
        expect_data = expect['data']
        if type(expect_data) is dict and len(expect_data) > 0:
            for key, val in expect_data.items():
                assert resp['data'][key] == expect_data[key]
        else:
            assert resp['data'] == expect_data

    def test_create_condition_from_dict_error(self):
        __parameters_01 = [
            {
                'parameter_id': -1,
                'value': 100.5,
                'lower_deviation_value': 10.5,
                'upper_deviation_value': 10.5,
                'flg_available': 'True',
                'description': 'Created automatically via seed:seed_tests'
            }
        ]

        __unique_name = 'CONDITION_TEST-1_DO_NOT_DELETE'

        expect = {
            'name': __unique_name,
            'flg_available': True,
            'description': 'Created automatically via seed:seed_tests',
            'parameters_conditions_attributes': __parameters_01
        }

        #
        # Set Condition from DICT (should succeed with existent)
        #
        resp = Condition.set_condition_from_dict(self.cal_client, expect)

        expect_app_info = {'name': ['has already been taken']}
        self.assert_find_error(MODULE_NAME, resp, expect_app_info)

    #
    # fields_validation
    #
    def fields_validation(self, receive, expect):
        assert receive['name'] == expect['name']
        assert receive['flg_available'] == expect['flg_available']
        assert receive['description'] == expect['description']

        num_params = len(expect['parameters_conditions_attributes'])
        assert receive['num_parameters'] == num_params


if __name__ == '__main__':
    unittest.main()
