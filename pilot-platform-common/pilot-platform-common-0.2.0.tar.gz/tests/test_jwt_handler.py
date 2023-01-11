# Copyright (C) 2022 Indoc Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pytest

from common.jwt_handler import JWTHandler
from common.jwt_handler.jwt_handler_exception import JWTHandlerException


class TestJWTHandler:
    AUTH_SERVICE = 'http://AUTH_SERVICE'

    def test_get_token_from_authorization(self, mock_rsa_keys, mock_request_authorization):
        client = JWTHandler(mock_rsa_keys['public_key'])
        token = client.get_token(mock_request_authorization)
        assert token == 'test_token'

    def test_get_token_from_cookie(self, mock_rsa_keys, mock_request_cookie):
        client = JWTHandler(mock_rsa_keys['public_key'])
        token = client.get_token(mock_request_cookie)
        assert token == 'test_token'

    def test_get_token_no_headers(self, mock_rsa_keys, mock_request_no_headers):
        with pytest.raises(JWTHandlerException, match='Failed to get token'):
            client = JWTHandler(mock_rsa_keys['public_key'])
            client.get_token(mock_request_no_headers)

    def test_get_current_identity_admin(self, mock_jwt_admin, mock_get_user_from_auth):
        client = JWTHandler(mock_jwt_admin['public_key'])
        decoded_token = client.decode_validate_token(mock_jwt_admin['token'])
        current_identity = client.get_current_identity(auth_service=self.AUTH_SERVICE, decoded_token=decoded_token)
        assert current_identity['user_id']
        assert current_identity['username'] == 'test'
        assert current_identity['role']
        assert current_identity['email'] == 'test@test.com'
        assert current_identity['first_name'] == 'test'
        assert current_identity['last_name'] == 'test'
        assert current_identity['realm_roles'] == ['platform-admin']

    def test_get_current_identity_contributor(self, mock_jwt_contributor, mock_get_user_from_auth):
        client = JWTHandler(mock_jwt_contributor['public_key'])
        decoded_token = client.decode_validate_token(mock_jwt_contributor['token'])
        current_identity = client.get_current_identity(auth_service=self.AUTH_SERVICE, decoded_token=decoded_token)
        assert current_identity['user_id']
        assert current_identity['username'] == 'test'
        assert current_identity['role']
        assert current_identity['email'] == 'test@test.com'
        assert current_identity['first_name'] == 'test'
        assert current_identity['last_name'] == 'test'
        assert current_identity['realm_roles'] == ['testproject-contributor']

    def test_get_current_identity_collaborator(self, mock_jwt_collaborator, mock_get_user_from_auth):
        client = JWTHandler(mock_jwt_collaborator['public_key'])
        decoded_token = client.decode_validate_token(mock_jwt_collaborator['token'])
        current_identity = client.get_current_identity(auth_service=self.AUTH_SERVICE, decoded_token=decoded_token)
        assert current_identity['user_id']
        assert current_identity['username'] == 'test'
        assert current_identity['role']
        assert current_identity['email'] == 'test@test.com'
        assert current_identity['first_name'] == 'test'
        assert current_identity['last_name'] == 'test'
        assert current_identity['realm_roles'] == ['testproject-collaborator']

    def test_get_current_identity_admin_expired_token(self, mock_jwt_admin_expired):
        with pytest.raises(JWTHandlerException, match='Failed to validate token'):
            client = JWTHandler(mock_jwt_admin_expired['public_key'])
            client.decode_validate_token(mock_jwt_admin_expired['token'])
