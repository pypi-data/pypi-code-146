import base64
import json
import os

from mlsteam_model_sdk.core import envs
from mlsteam_model_sdk.core.exceptions import (
    MissingApiTokenException,
    InvalidApiTokenException,
)
from mlsteam_model_sdk.utils.config import (
    get_value,
    OPTION_API_TOKEN,
)


class Credential(object):
    def __init__(self, token):
        if token is None:
            token = self._get_token()
        token_dict = self._api_token_to_dict(token)
        if 'api_address' not in token_dict:
            raise InvalidApiTokenException()
        self._api_address = token_dict['api_address']
        self._api_token = token

    @classmethod
    def _get_token(cls):
        token = get_value(OPTION_API_TOKEN)
        if token is None:
            token = os.getenv(envs.API_TOKEN_ENV)
        if token is None:
            raise MissingApiTokenException()
        return token

    @classmethod
    def _api_token_to_dict(cls, api_token):
        try:
            tokend = {}
            tokens = api_token.split('.')
            if len(tokens) != 3:
                raise InvalidApiTokenException()
            tokend = cls._token_decode(tokens[0])
            tokend.update(cls._token_decode(tokens[1]))
            return tokend
        except Exception:
            raise InvalidApiTokenException()

    @classmethod
    def _token_decode(cls, token):
        try:
            tokenb = token.encode() + b'=' * (-len(token) % 4)
            return json.loads(base64.b64decode(tokenb).decode('utf-8'))
        except Exception:
            raise InvalidApiTokenException()

    @property
    def api_token(self):
        return self._api_token

    @property
    def api_address(self):
        return self._api_address
