import requests

from requests.exceptions import ConnectionError, ReadTimeout, RequestException

from .decorator import request_error_logging
from .exceptions import AuthenticationError
from .util import api_keyword_to_url


@request_error_logging
def post_request(api_keyword, payload):
    url = api_keyword_to_url(api_keyword)
    try:
        r = requests.post(url, payload)
    except ConnectionError as e:
        raise ConnectionError(e)
    except ReadTimeout as e:
        raise ReadTimeout(e)
    except RequestException as e:
        raise RequestException(e)
    return r


class Authentication:
    def __init__(self):
        self.username = None
        self.password = None
        self._token = None
        self._api_keyword = "get_token/"
        self._is_valid_token = False

    @property
    def token(self):
        if self._token is not None:
            return self._token
        elif self.is_username_and_password_valid():
            return self._token
        else:
            raise AuthenticationError("'username' and 'password' or 'token' may be no provided or invalid ")

    @token.setter
    def token(self, value):
        if self._is_valid_token:
            self._token = value
            self._is_valid_token = False
        else:
            res = post_request(self._api_keyword, {"token": value})
            if res and res.status_code == 200:
                self._is_valid_token = True

                self.token = res.json()["token"]

    def is_username_and_password_valid(self):
        if not self.username or not self.password:
            return False
        else:
            res = post_request(self._api_keyword, {"username": self.username, "password": self.password})
            if res and res.status_code == 200:
                self._is_valid_token = True
                self.token = eval(res.content.decode("utf-8")).get("token")
                return True
            else:
                return False

    def get_post_header(self):
        return {'Authorization': "Token %s" % self.token}


authentication = Authentication()
del Authentication
