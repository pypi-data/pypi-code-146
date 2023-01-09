#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/3/11 15:42
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : credentials.py
@Desc    : 
"""

import base64
import json
import logging
import os
from waveletai.constants import ANONYMOUS, ANONYMOUS_API_TOKEN
from waveletai import envs
from waveletai.exceptions import InvalidApiKey
from waveletai.exceptions import MissingApiTokenException

_logger = logging.getLogger(__name__)


class Credentials(object):
    """It formats your Neptune api token to the format that can be understood by the Neptune Client.

    A constructor allowing you to pass the NeptuneNeptune API token.

    Args:
        api_token(str): This is a secret API key that you can retrieve by running
            `$ waveletai account api-token get`

    Attributes:
        api_token:  This is a secret API key that was passed at instantiation.

    Examples:

        >>> from waveletai.backends.credentials import Credentials
        >>> credentials=Credentials('YOUR_API_KEY')

        Alternatively you can create an environment variable by running:

        $ export WAVELETAI_API_TOKEN=YOUR_API_TOKEN

        which will allow you to use the same method without `api_token` parameter provided.

        >>> credentials=Credentials()

    Note:
        For security reasons it is recommended to provide api_token through environment variable `WAVELETAI_API_TOKEN`.
        You can do that by going to your console and running:

        $ export WAVELETAI_API_TOKEN=YOUR_API_TOKEN`

        Token provided through environment variable takes precedence over `api_token` parameter.
    """

    def __init__(self, api_token=None):
        if api_token is None:
            api_token = os.getenv(envs.API_TOKEN_ENV_NAME)

        if api_token == ANONYMOUS:
            api_token = ANONYMOUS_API_TOKEN

        self._api_token = api_token
        if self.api_token is None:
            raise MissingApiTokenException()

        token_dict = self._api_token_to_dict(self.api_token)
        self._token_origin_address = token_dict['api_address']
        self._api_url = token_dict['api_url'] if 'api_url' in token_dict else None

    @property
    def api_token(self):
        return self._api_token

    @property
    def token_origin_address(self):
        return self._token_origin_address

    @property
    def api_url_opt(self):
        return self._api_url

    @staticmethod
    def _api_token_to_dict(api_token):
        try:
            return json.loads(base64.b64decode(api_token.encode()).decode("utf-8"))
        except Exception:
            raise InvalidApiKey()
