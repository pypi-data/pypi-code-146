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

import httpx
import jwt
from starlette.requests import Request

from common.jwt_handler.jwt_handler_exception import JWTHandlerError
from common.jwt_handler.jwt_handler_exception import JWTHandlerException


class JWTHandler:
    def __init__(self, public_key: str) -> None:
        self.public_key = public_key

    def _get_token_from_authorization(self, request: Request) -> str:
        token = request.headers.get('Authorization')
        if token:
            return token.split()[0]

    def _get_token_from_cookies(self, request: Request) -> str:
        cookies = request.headers.get('cookie')
        if cookies:
            cookies = cookies.split(';')
            for cookie in cookies:
                if cookie.startswith('AUTH='):
                    return cookie[5:]

    def get_token(self, request: Request) -> str:
        token = self._get_token_from_authorization(request)
        if not token:
            token = self._get_token_from_cookies(request)
            if not token:
                raise JWTHandlerException(JWTHandlerError.GET_TOKEN_ERROR)
        return token

    def decode_validate_token(self, encoded_token: str) -> dict:
        try:
            expected_audience = ['minio', 'account']
            decoded_token = jwt.decode(
                jwt=encoded_token,
                key=self.public_key,
                algorithms='RS256',
                audience=expected_audience,
                options={
                    'verify_signature': True,  # cryptographic signature
                    'verify_aud': True,  # audience
                    'verify_iss': True,  # issuer
                    'verify_exp': True,  # expiration
                    'verify_iat': True,  # issued at
                    'verify_nbf': True,  # not before
                },
            )
            return decoded_token
        except Exception:
            raise JWTHandlerException(JWTHandlerError.VALIDATE_TOKEN_ERROR)

    def get_current_identity(self, auth_service: str, decoded_token: dict) -> dict:
        username: str = decoded_token.get('preferred_username')
        if not username:
            return None

        # get user data from Auth service
        response = httpx.get(f'{auth_service}/v1/admin/user', params={'username': username, 'exact': True})
        if response.status_code != 200:
            raise Exception(f'Error getting user {username} from Auth service: {response.json()}')
        user = response.json()['result']
        if not user or user['attributes'].get('status') != 'active':
            return None

        return {
            'user_id': user['id'],
            'username': username,
            'role': user['role'] if 'role' in user else None,
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'realm_roles': decoded_token['realm_access']['roles']
            if ('realm_access' in decoded_token and 'roles' in decoded_token['realm_access'])
            else [],
        }
