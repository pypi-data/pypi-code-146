#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import boto3

_CLIENT_ID = '4pe1qvk2c0sr7hf90a1auv8ak1'
_REGION_NAME = 'eu-west-3'

if 'COMAP_SMART_HOME_USERNAME' in os.environ and 'COMAP_SMART_HOME_PASSWORD' in os.environ:
    _USERNAME = os.environ['COMAP_SMART_HOME_USERNAME']
    _PASSWORD = os.environ['COMAP_SMART_HOME_PASSWORD']
else:
    print('No COMAP Smart Home credentials available.\nPlease add your credentials to your environment. ')


class ClientAuth(object):
    client_id = _CLIENT_ID
    region_name = _REGION_NAME
    # TODO refresh token expiration ??

    def __init__(self, username=_USERNAME, password=_PASSWORD):
        self.username = username
        self.password = password
        self._token = None
        self._refresh_token = None
        self._token_expiration = None
        self._refresh_token_expiration = None

        self.cidp = boto3.client('cognito-idp', region_name=self.region_name)

        self._get_new_token()

    @property
    def token(self):
        if time.time() > self._token_expiration:
            self._refresh_current_token()
        return self._token

    def _get_new_token(self):
        response = self.cidp.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': self.username,
                'PASSWORD': self.password},
            ClientId=self.client_id
        )

        self._token = response['AuthenticationResult']["AccessToken"]
        self._token_expiration = time.time() + response['AuthenticationResult']["ExpiresIn"]
        self._refresh_token = response['AuthenticationResult']["RefreshToken"]

    def _refresh_current_token(self):
        if self._token:
            response = self.cidp.initiate_auth(
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={
                    'REFRESH_TOKEN': self._refresh_token
                },
                ClientId=self.client_id
            )

            self._token = response['AuthenticationResult']['AccessToken']
            self._token_expiration = time.time() + response['AuthenticationResult']['ExpiresIn']
            print('new token')


if __name__ == '__main__':
    auth = ClientAuth()
