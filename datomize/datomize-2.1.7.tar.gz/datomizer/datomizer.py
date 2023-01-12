import atexit
from datomizer.helpers.authentication.authentication_helper import *
from datomizer.utils.exceptions import InvalidResponse
from datomizer.utils.general import ACCESS_TOKEN, REFRESH_TOKEN, AUTHORIZATION, BEARER_TOKEN, D_REALM


class Datomizer(object):
    domain: str
    realm: str
    access_token: str
    refresh_token: str
    auth_headers: dict

    def __init__(self, username: str, password: str, env: str = 'app'):
        """Create an authentication object and register Datomize on it using the Datomizer constructor

        Args:
            username: your username
            password: your password
        Returns:
            Datomizer Authentication object"""
        self.domain = get_domain_by_username(username=username, env=env)
        self.realm = get_realm_by_domain(domain=self.domain)
        token_response = post_token(realm=self.realm, domain=self.domain,
                                    username=username, password=password)
        self.config_token(token_response)
        atexit.register(self.__close)

    def refresh_token_headers(self):
        token_response = post_refresh_token(realm=self.realm,
                                            domain=self.domain,
                                            token=self.refresh_token)
        self.config_token(token_response)

    def config_token(self, token_response):
        try:
            self.access_token = token_response[ACCESS_TOKEN]
            self.refresh_token = token_response[REFRESH_TOKEN]
            self.auth_headers = {AUTHORIZATION: BEARER_TOKEN % self.access_token, D_REALM: self.realm}
        except Exception as ex:
            print(f"token res:{token_response}")
            raise ex

    def get_response_json(self, method: requests.Request,
                          url: str, headers: {} = {}, url_params: [] = [], **kwargs) -> requests.Response:
        return self.api_request(method=method, url=url, headers=headers, url_params=url_params, **kwargs).json()

    def api_request(self, method: requests.Request,
                    url: str, headers: {} = {}, url_params: [] = [], **kwargs) -> requests.Response:
        kwargs['url'] = url % (self.domain, *url_params)

        headers.update(self.auth_headers)
        kwargs['headers'] = headers
        response: requests.Response = method(**kwargs)

        # refresh token and retry on unauthorized or forbidden request
        if response.status_code in [401, 403]:
            self.refresh_token_headers()
            headers.update(self.auth_headers)
            response = method(**kwargs)

        self.validate_response(response)
        return response

    def base_validation(self):
        if not (self.realm and self.domain):
            raise Exception("missing base properties")

    def next_step_validation(self):
        if not self.access_token:
            raise Exception("access token is not configured")

    @staticmethod
    def validate_response(response: requests.Response, not_valid_message: str = "Status is not OK"):
        if response.status_code != 200:
            raise InvalidResponse(response, not_valid_message)

    def __close(self):
        post_log_out(realm=self.realm, domain=self.domain,
                     token=self.access_token, refresh_token=self.refresh_token)
