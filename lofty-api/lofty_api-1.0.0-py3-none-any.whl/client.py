import requests

from .constants import LoftyApi
from .client_auth import ClientAuth
from .responses.auth import AwsCredentials
from .pagination_options import PaginationOptions

class LoftyAiApi:
    def __init__(
            self,
            verbose: bool = False,
            api_host_override: str = None
    ):
        """
        Initializes the API client.

        Parameters:
        verbose (bool): Whether to print messages to the console verbosely.
        api_host_override (str): An override for the API Host defined in API Constants - only override for testing.
        """
        self._verbose: bool = verbose

        self._api_constants: LoftyApi = LoftyApi(api_host_override)
        self._client_auth: ClientAuth = ClientAuth(
            verbose,
            api_host_override
        )

    def _request(self, method: str, path: str, params=None):
        url = self._api_constants.api_endpoint + path
        if self._verbose:
            print(method, url)

        s = requests.Session()
        response = s.request(
            method,
            url,
            auth=self._client_auth,
            headers={
                'Cache-Control': 'no-cache'
            },
            params=params
        )

        if response.status_code == 200:
            return response.json()
        elif response.content:
            raise Exception(str(response.status_code) + ": " + response.reason + ": " + str(response.content))
        else:
            raise Exception(str(response.status_code) + ": " + response.reason)

    # Returns a token if properly authenticated
    def login(self, username: str, password: str) -> AwsCredentials:
        return self._client_auth.login(username, password)

    def get_user(self) -> dict:
        return self._request('GET', '/users/v2/get')

    def get_user_bank_data(self) -> dict:
        return self._request('GET', '/users/v2/getbdata')

    def get_user_countries(self) -> dict:
        return self._request('GET', '/users/v2/countries')

    def get_user_status_summary(self) -> dict:
        return self._request('GET', '/users/v2/status-summary')

    def get_payment_methods(self) -> dict:
        return self._request('GET', '/payments/v2/list-payment-methods')

    def get_transactions(self, pagination_options: PaginationOptions) -> dict:
        return self._request('GET', '/transactions/v2/getbyuser', params=pagination_options.to_params())

    # Many more endpoints to come! Stay tuned!
