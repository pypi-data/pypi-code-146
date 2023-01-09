# This file contains variables.

class Constants():
    OAUTH2_DEL = 'oauth2'
    JWT_KEY_DEL = 'jwtKey'
    API_KEY_DEL = 'apiKey'
    GRANT_TYPE = 'password'
    GRANT_TYPE_REFRESH_TOKEN = 'refresh_token'

class AuthVariables():
    def __init__(self):
        self._INSTANCE = None
        self._AUTH_TYPE = None
        self._ACCESS_TOKEN = None
        self._REFRESH_TOKEN = None
        self._JWT_TOKEN = None
        self._API_TOKEN = None
        self._CLIENT_ID = None
        self._SECRETS = None

    @property
    def INSTANCE(self):
        return self._INSTANCE

    @property
    def AUTH_TYPE(self):
        return self._AUTH_TYPE

    @property
    def ACCESS_TOKEN(self):
        return self._ACCESS_TOKEN

    @property
    def REFRESH_TOKEN(self):
        return self._REFRESH_TOKEN

    @property
    def JWT_TOKEN(self):
        return self._JWT_TOKEN

    @property
    def API_TOKEN(self):
        return self._API_TOKEN
        
    @property
    def CLIENT_ID(self):
        return self._CLIENT_ID

    @property
    def SECRETS(self):
        return self._SECRETS

    @INSTANCE.setter
    def INSTANCE(self, value):
        self._INSTANCE = value

    @AUTH_TYPE.setter
    def AUTH_TYPE(self, value):
        self._AUTH_TYPE = value

    @ACCESS_TOKEN.setter
    def ACCESS_TOKEN(self, value):
        self._ACCESS_TOKEN = value

    @REFRESH_TOKEN.setter
    def REFRESH_TOKEN(self, value):
        self._REFRESH_TOKEN = value

    @JWT_TOKEN.setter
    def JWT_TOKEN(self, value):
        self._JWT_TOKEN = value

    @API_TOKEN.setter
    def API_TOKEN(self, value):
        self._API_TOKEN = value
        
    @CLIENT_ID.setter
    def CLIENT_ID(self, value):
        self._CLIENT_ID = value

    @SECRETS.setter
    def SECRETS(self, value):
        self._SECRETS = value