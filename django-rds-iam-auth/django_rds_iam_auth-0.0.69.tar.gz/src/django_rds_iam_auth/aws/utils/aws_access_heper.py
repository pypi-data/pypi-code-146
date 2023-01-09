import datetime

import boto3
import jwt
from dateutil.tz import tzlocal
from django.core.cache import caches


class RolesAndPermissionsCacheManager:
    _id_token = None
    _access_token = None
    _cached_access_data = None
    _identity_pool_id = None
    _user_pool_id = None


class CredentialsManager:
    _id_token = None
    _access_token = None
    _cached_access_data = None
    _identity_pool_id = None
    _user_pool_id = None
    _account_id = None

    def __init__(self, jwt_token=None, id_token=None, identity_pool_id=None, user_pool_id=None, session=None, account_id=None):
        self._cache = caches['token_cache']
        self._access_token = str.replace(jwt_token, 'Bearer ', '')
        self._id_token = id_token
        self._identity_pool_id = identity_pool_id
        self._user_pool_id = user_pool_id
        self._access_data = None
        self._account_id = account_id

    def get_credentials(self):
        if not self._access_token:
            return None
        try:
            credentials = self._cache.get(self._access_token, None)
            if not credentials or not isinstance(credentials, dict):
                raise Exception('no cached credentials')
        except Exception as ex:
            try:
                credentials = self._fetch_credentials(True)
            except Exception as ext:
                return None
        for cred_key in ('aws_access_key_id', 'aws_secret_access_key' , 'aws_session_token', 'expiry_time'):
            if cred_key not in credentials or not credentials.get(cred_key,None):
                return None
        return credentials

    def _fetch_credentials(self, require_expiry=True):
        boto_client = boto3.client('cognito-identity')
        token = jwt.decode(self._id_token, verify=False)
        provider = token.get('iss')
        provider = provider.replace('https://', '', 1)

        identity_pool_request_params = {
            'IdentityPoolId': self._identity_pool_id,
            'AccountId': self._account_id,
            'Logins': {
                provider: self._id_token
            }
        }
        identity_pool_data = boto_client.get_id(**identity_pool_request_params)
        identity_credentials_request_params = {
            'IdentityId': identity_pool_data.get('IdentityId'),
            'Logins': {
                provider: self._id_token
            }
        }
        user_credentials_data = boto_client.get_credentials_for_identity(**identity_credentials_request_params)
        credentials_dict = user_credentials_data.get('Credentials')

        delta = int((credentials_dict.get('Expiration') - datetime.datetime.now(tzlocal())).total_seconds())

        credentials = {
            'aws_access_key_id': credentials_dict.get('AccessKeyId'),
            'aws_secret_access_key': credentials_dict.get('SecretKey'),
            'aws_session_token': credentials_dict.get('SessionToken'),
            'expiry_time': delta
        }
        # self._cache.set(self._access_token, credentials)
        return credentials