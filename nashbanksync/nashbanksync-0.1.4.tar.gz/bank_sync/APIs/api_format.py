import json
import requests
from rest_framework import status
try:
    from django.conf import settings
except Exception as e:
    pass
# This is a class that is designed to include all methods and functions one needs to make an A.P.I. call
class API(object):

    _base_url = "https://dev.bankingservices.nashglobal.co/api/banks"
    _base_url_third_party_banking = "https://dev.3p.bankingservices.nashglobal.co/api"

    _auth_token_url = None
    _client_id = None
    _client_secret = None
    _identity_token = None
    _auth_scope = None

    try:
        _client_id = getattr(
            settings, 'OAUTH2_CLIENT_ID', _client_id)
        _client_secret = getattr(
            settings, 'CLIENT_SECRET', _client_secret)
        _auth_token_url = getattr(
            settings, 'OAUTH2_TOKEN_URL', _auth_token_url)
        _auth_scope = getattr(
            settings, 'OAUTH2_SCOPE', _auth_scope)
    except Exception as e:
        pass

    _full_url = ""

    # Most API calls require headers, params and payloads
    _headers = None
    _params = None
    _payload = None

    # You always expect a response from A.P.I. calls
    _response = {}

    # When using this class to create an A.P.I. class, each API should have an optional name and code
    # but must have headers and any required parameters
    def __init__(self, name=None, headers=None, params=None, code=None):
        self._name = name
        self._code = code

        self._headers = headers
        self._params = params

        requests.packages.urllib3.disable_warnings()

    def set_identity_token(self,identity_token):
        self._identity_token = identity_token
        return self

    def refresh_identity_token(self):
        _payload = {
            'grant_type': 'client_credentials',
            'scope': self._auth_scope,
            'client_id': self._client_id,
            'client_secret': self._client_secret
        }
        self._identity_token = requests.request(
            "POST", self._auth_token_url, data=_payload)

    # There are 3 types of API requests that most APIs use, POST, GET and PUT
    # This method will take the payload or data to be sent and send it to the required API url
    # using the desired method and returns the response
    def api_request(self, payload, method, verify = False, files = None):
        
        if payload == "null":
            self._payload=json.dumps({})
        else:
            self._payload = payload
        
        if self._headers is not None and self.get_identity_token is not None:
            if self.get_identity_token.status_code == 200:
                self._headers.update({
                    'Authorization':f"Bearer {self.get_identity_token.json().get('access_token',None)}"
                })
        
        try:
            if method == 'POST':
                self._response = requests.post(self.get_full_url(), headers=self._headers, params=self._params,
                                           data=self._payload, json=self._payload, verify=verify,files=files)
            elif method == 'PUT':
                self._response = requests.put(self.get_full_url(), headers=self._headers, params=self._params,
                                           data=self._payload, json=self._payload, verify=verify)
            elif method == 'GET':
                self._response = requests.get(self.get_full_url(), headers=self._headers, params=self._params,
                                           data=self._payload, json=self._payload, verify=verify)
            elif method == 'DELETE':
                self._response = requests.delete(self.get_full_url(), headers=self._headers, params=self._params,
                                           data=self._payload, json=self._payload, verify=verify)

            try:
                if self._response.status_code == status.HTTP_200_OK:
                    self._response = json.loads(self._response.text)
                else:
                    if status.is_server_error(self._response.status_code):
                        self._response['error'] = f'Internal Server Error: HTTP Error Code {self._response.status_code}'
                    elif status.is_client_error(self._response.status_code):
                        self._response['error'] = f'Client Server Error: HTTP Error Code {self._response.status_code}: {self.get_full_url()}'
            except ValueError as e:
                self._response['error'] = self._response.text

        except Exception as e:
            self._response['error'] = f'Internal Server Error: {e}'
        finally:
            return self._response

    # Method used to get the repsonse returned by an API instead of calling the API again
    def get_response(self):
        return self._response

    def set_headers(self, headers):
        self._headers = headers
        return self

    def get_headers(self):
        return self._headers

    def set_params(self, params):
        self._params = params
        return self

    def set_full_url(self, full_url):
        self._full_url = full_url
        return self

    def get_params(self):
        return self._params

    def get_full_url(self):
        return self._full_url

    def get_payload(self):
        return self._payload

    def get_base_url(self):
        return self._base_url

    def get_base_url_third_party_banking(self):
        return self._base_url_third_party_banking

    @property
    def get_identity_token(self):
        return self._identity_token