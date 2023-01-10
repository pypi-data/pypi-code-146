import unittest, time
from kcapi import OpenID, RestURL
from .testbed import KcBaseTestCase


class Testing_User_API(KcBaseTestCase):

    def test_adding_credentials_with_wrong_params(self):
        users = self.testbed.getKeycloak().build('users', self.REALM)
        user_info = {'key': 'username', 'value': 'batman'}
        user_credentials = {'temporary': False, 'passwordWrongParam': '12345'}
        try:
            state = users.updateCredentials(user_info, user_credentials).isOk()
        except Exception as E:
            self.assertEqual("Missing parameter: value" in str(E), True)

    def test_adding_credentials_to_user(self):

        users = self.testbed.getKeycloak().build('users', self.REALM)
        user_info = {'key': 'username', 'value': 'batman'}
        user_credentials = {'temporary': False, 'value': '12345'}
        state = users.updateCredentials(user_info, user_credentials).isOk()
        self.assertTrue(state)

        oid_client = OpenID({
            "client_id": "dc",
            "username": "batman",
            "password": "12345",
            "grant_type": "password",
            "realm": self.REALM
        }, self.testbed.ENDPOINT)

        token = oid_client.getToken()
        self.assertNotEqual(token, None)


if __name__ == '__main__':
    unittest.main()
