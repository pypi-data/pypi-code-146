"""UserApiTest class"""

import unittest
from http import HTTPStatus

import pytest

from .api_base import ApiBase
from ..common.secrets import USER_INFO


@pytest.mark.usefixtures('client_cls')
class UserApiTest(ApiBase, unittest.TestCase):
    __current_user_info_01 = {
        'email': USER_INFO['EMAIL'],
        'first_name': USER_INFO['FIRST_NAME'],
        'last_name': USER_INFO['LAST_NAME'],
        'name': USER_INFO['NAME'],
        'nickname': USER_INFO['NICKNAME'],
        'provider': USER_INFO['PROVIDER'],
        'uid': USER_INFO['UID']
    }

    def test_user_info(self):
        current_user = self.__current_user_info_01

        resp = self.cal_client.get_current_user()
        receive = self.load_response_content(resp)

        # Debug Response
        # debug_response(response)

        self.fields_validation(receive, current_user)
        assert resp.status_code == HTTPStatus.OK

    def fields_validation(self, receive, expect):
        assert receive['email'] == expect['email']
        assert receive['first_name'] == expect['first_name']
        assert receive['last_name'] == expect['last_name']
        assert receive['name'] == expect['name']
        assert receive['nickname'] == expect['nickname']
        assert receive['provider'] == expect['provider']
        assert receive['uid'] == expect['uid']


if __name__ == '__main__':
    unittest.main()
