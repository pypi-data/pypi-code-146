"""BaseTest Class with helper methods common to all modules tests"""

import unittest


class ModuleBase(unittest.TestCase):
    def assert_create_success(self, module_name, receive, exp_data):
        msg = '{0} created successfully'.format(module_name)
        exp = {'success': True, 'info': msg, 'app_info': {}, 'data': exp_data}
        self.__assert_success(receive, exp)

    def assert_find_success(self, module_name, receive, exp_data):
        msg = 'Got {0} successfully'.format(module_name)
        exp = {'success': True, 'info': msg, 'app_info': {}, 'data': exp_data}
        self.__assert_success(receive, exp)

    def assert_update_success(self, module_name, receive, exp_data):
        msg = '{0} updated successfully'.format(module_name)
        exp = {'success': True, 'info': msg, 'app_info': {}, 'data': exp_data}
        self.__assert_success(receive, exp)

    def assert_delete_success(self, module_name, receive):
        msg = '{0} deleted successfully'.format(module_name)
        exp = {'success': True, 'info': msg, 'app_info': {}, 'data': {}}
        self.__assert_success(receive, exp)

    def assert_set_success(self, module_name, receive, exp_data):
        msg = '{0} set successfully'.format(module_name)
        exp = {'success': True, 'info': msg, 'app_info': {}, 'data': exp_data}
        self.__assert_success(receive, exp)

    def assert_create_error(self, module_name, receive, exp_info):
        msg = 'Error creating {0}'.format(module_name)
        exp = {'success': False, 'info': msg, 'app_info': exp_info, 'data': {}}
        self.__assert_error(receive, exp)

    def assert_find_error(self, module_name, receive, exp_info):
        msg = '{0} not found!'.format(module_name)
        exp = {'success': False, 'info': msg, 'app_info': exp_info, 'data': {}}
        self.__assert_error(receive, exp)

    def assert_update_error(self, module_name, receive, exp_info):
        msg = 'Error updating {0}'.format(module_name)
        exp = {'success': False, 'info': msg, 'app_info': exp_info, 'data': {}}
        self.__assert_error(receive, exp)

    def assert_delete_error(self, module_name, receive, exp_info):
        msg = 'Error deleting {0}'.format(module_name)
        exp = {'success': False, 'info': msg, 'app_info': exp_info, 'data': {}}
        self.__assert_error(receive, exp)

    def assert_set_error(self, module_name, receive, exp_info):
        msg = 'Error setting {0}'.format(module_name)
        exp = {'success': False, 'info': msg, 'app_info': exp_info, 'data': {}}
        self.__assert_error(receive, exp)

    def __assert_success(self, receive, expect):
        assert receive['app_info'] == {}

        # Validate all 'data' fields
        expect_data = expect['data']
        if type(expect_data) is list and len(expect_data) > 0:
            for i in range(0, len(expect_data)):
                self.fields_validation(receive['data'][i], expect['data'][i])
        elif type(expect_data) is dict and len(expect_data) > 0:
            self.fields_validation(receive['data'], expect['data'])

        assert receive['info'] == expect['info']
        assert receive['success'] == expect['success']

    def __assert_error(self, receive, expect):
        field = 'app_info'
        expect_app_info = expect[field]

        if type(expect_app_info) is dict and len(expect_app_info) > 0:
            for key, val in expect_app_info.items():
                assert receive[field][key] == expect_app_info[key]
        else:
            assert receive[field] == expect[field]

        assert receive['data'] == expect['data']
        assert receive['info'] == expect['info']
        assert receive['success'] == expect['success']
