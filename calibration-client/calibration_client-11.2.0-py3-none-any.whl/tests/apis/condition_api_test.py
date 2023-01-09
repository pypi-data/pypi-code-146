"""ConditionApiTest class"""

import unittest
from http import HTTPStatus

import pytest

from .api_base import ApiBase
from ..common.config_test import RESOURCE_NOT_FOUND


@pytest.mark.usefixtures('client_cls')
class ConditionApiTest(ApiBase, unittest.TestCase):
    __unique_name = 'CONDITION_TEST-1_DO_NOT_DELETE'

    def test_expected_condition(self):
        parameters_conditions_attr = [
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

        condition = {
            'condition': {
                'name': self.__unique_name,
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests',
                'parameters_conditions_attributes': parameters_conditions_attr
            }
        }

        expect = condition['condition']
        # expect_params_conditions = len(parameters_conditions_attr)

        response1 = self.cal_client.set_expected_condition(condition)
        receive = self.load_response_content(response1)

        #
        # This test cannot be done because this function can return
        # either one of the following messages:
        # 1) self.assert_eq_str(response_content['info'],
        #   'Condition was successfully created.')
        # 2) self.assert_eq_str(response_content['info'],
        #   'Condition was successfully found.')
        self.fields_validation(receive, expect)
        # assert response1.status_code == HTTPStatus.CREATED
        assert response1.status_code == HTTPStatus.OK

        response2 = self.cal_client.get_expected_condition(condition)
        receive = self.load_response_content(response2)

        self.fields_validation(receive, expect)
        assert response2.status_code == HTTPStatus.OK

    def test_possible_conditions_exact_values(self):
        parameters_conditions_attr = [
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

        condition = {
            'condition': {
                'name': self.__unique_name,
                'event_at': '2019-07-25 09:14:52',
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests',
                'parameters_conditions_attributes': parameters_conditions_attr
            }
        }

        expect = condition['condition']

        response = self.cal_client.get_possible_conditions(condition)
        receive = self.load_response_content(response)[0]

        assert response.status_code == HTTPStatus.OK
        self.fields_validation(receive, expect)

    def test_possible_conditions_near_values(self):
        parameters_conditions_attr = [
            {
                'parameter_id': -1,
                'value': 2.0,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5,
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests'
            },
            {
                'parameter_id': -2,
                'value': 1.999,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5,
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests'
            }
        ]

        condition = {
            'condition': {
                'name': self.__unique_name,
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests',
                'parameters_conditions_attributes': parameters_conditions_attr
            }
        }

        expect = condition['condition']
        # expect_params_conditions = len(parameters_conditions_attr)

        response = self.cal_client.get_possible_conditions(condition)
        receive = self.load_response_content(response)[0]

        self.fields_validation(receive, expect)
        assert response.status_code == HTTPStatus.OK

    def test_possible_conditions_outside_values(self):
        parameters_conditions_attr = [
            {
                'parameter_id': -1,
                'value': 2.0,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5,
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests'
            },
            {
                'parameter_id': -2,
                'value': 2.000001,  # Value outside bunderies
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5,
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests'
            }
        ]

        condition = {
            'condition': {
                'name': self.__unique_name,
                'flg_available': 'true',
                'description': '',
                'parameters_conditions_attributes': parameters_conditions_attr
            }
        }

        response = self.cal_client.get_possible_conditions(condition)
        receive = self.load_response_content(response)

        expect = {'info': RESOURCE_NOT_FOUND}
        assert receive == expect
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_expected_condition_text_param(self):
        parameters_conditions_attr = [
            {
                'parameter_id': -1,
                'value': 1.5,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5
            },
            {
                'parameter_id': -3,
                'value': ','.join(str(x) for x in list(range(0, 512)))
            }
        ]

        condition = {
            'condition': {
                'name': 'CONDITION_TEST-7_DO_NOT_DELETE',
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests',
                'parameters_conditions_attributes': parameters_conditions_attr
            }
        }
        
        # only one condition is expected to be retrieved with such exact parameters
        expect = condition['condition']

        # we call the API to set the condition but in reality we should just
        # retrieve the already existing one with the same exact parameters
        response = self.cal_client.set_expected_condition(condition)
        receive = self.load_response_content(response)

        assert response.status_code == HTTPStatus.OK
        self.fields_validation(receive, expect)

    def test_possible_condition_text_param(self):
        parameters_conditions_attr = [
            {
                'parameter_id': -1,
                'value': 1.3,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5
            },
            {
                'parameter_id': -3,
                'value': ','.join(str(x) for x in list(range(0, 250)))
            }
        ]

        condition_01 = {
            'condition': {
                'name': 'CONDITION_TEST-8_DO_NOT_DELETE',
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests',
                'parameters_conditions_attributes': parameters_conditions_attr
            }
        }

        condition_02 = {
            'condition': {
                'name': 'CONDITION_TEST-7_DO_NOT_DELETE',
                'flg_available': True,
                'description': 'Created automatically via seed:seed_tests',
                'parameters_conditions_attributes': parameters_conditions_attr
            }
        }

        # two possible conditions are expected to be valid with such parameters
        expect_01 = condition_01['condition']
        expect_02 = condition_02['condition']
        response = self.cal_client.get_possible_conditions(condition_01)
        receive = self.load_response_content(response)

        assert response.status_code == HTTPStatus.OK
        self.fields_validation(receive[0], expect_01)
        self.fields_validation(receive[1], expect_02)

    def test_possible_conditions_txt_params_outside_values(self):
        parameters_conditions_attr = [
            {
                'parameter_id': -1,
                'value': 1.5,
                'lower_deviation_value': 0.5,
                'upper_deviation_value': 0.5
            },
            {
                'parameter_id': -3,
                'value': ','.join(str(x) for x in list(range(0, 512)))[:1000] + ',unmatched text parameter'
            }
        ]

        condition = {
            'condition': {
                'name': self.__unique_name,
                'flg_available': 'true',
                'description': '',
                'parameters_conditions_attributes': parameters_conditions_attr
            }
        }

        response = self.cal_client.get_possible_conditions(condition)
        receive = self.load_response_content(response)

        expect = {'info': RESOURCE_NOT_FOUND}
        assert receive == expect
        assert response.status_code == HTTPStatus.NOT_FOUND

    def fields_validation(self, receive, expect):
        assert receive['name'] == expect['name']
        assert receive['flg_available'] == expect['flg_available']
        assert receive['description'] == expect['description']

        assert receive['num_parameters'] == len(
            expect['parameters_conditions_attributes']
        )


if __name__ == '__main__':
    unittest.main()
