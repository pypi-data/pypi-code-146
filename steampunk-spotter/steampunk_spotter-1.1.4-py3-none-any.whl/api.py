"""Provide API client."""

import sys
from typing import Optional, Tuple, Dict, Any

import requests

from spotter.storage import Storage
from spotter.utils import get_current_cli_version


class ApiClient:
    """A client interface for interacting with the API."""

    DEFAULT_ENDPOINT = "https://api.spotter.steampunk.si/api"
    DEFAULT_HEADERS = {
        "Accept": "application/json",
        "User-Agent": f"steampunk-spotter/{get_current_cli_version()}"
    }
    DEFAULT_TIMEOUT = 10

    def __init__(self, base_url: str, storage: Storage, username: Optional[str], password: Optional[str]):
        """
        Construct ApiClient object.

        :param base_url: Base API endpoint url
        :param storage: Storage object, where tokens are stored
        :param username: Username
        :param password: Password
        """
        self._base_url = base_url.rstrip("/")
        self._storage = storage
        self._username = username
        self._password = password

        self._storage_tokens_path = "tokens" if self._storage.exists("tokens") else "tokens.json"
        if self._storage_tokens_path == "tokens":
            self._old_tokens_fallback()

    def _url(self, path: str) -> str:
        """Construct the full API endpoint URL based on the base path."""
        return self._base_url + path

    def _get_tokens(self) -> Tuple[str, str]:
        """
        Retrieve tokens (access and refresh token) from storage.

        :return: tokens as tuple of strings (access token, refresh token)
        """
        if not self._storage.exists(self._storage_tokens_path):
            print("You are not logged in!\nTo log in, you should provide your username and password:\n\n"
                  "    - using spotter login command;\n"
                  "    - via --username/-u and --password/-p optional arguments;\n"
                  "    - by setting SPOTTER_USERNAME and SPOTTER_PASSWORD environment variables.\n")
            sys.exit(1)

        tokens = self._storage.read_json(self._storage_tokens_path)
        endpoint_tokens = tokens.get(self._base_url, {})

        if not endpoint_tokens:
            print(f"Error: No {self._base_url} endpoint in {self._storage.path / self._storage_tokens_path}.")
            sys.exit(1)

        if not isinstance(endpoint_tokens, dict):
            print(f"Error: The {self._base_url} JSON entry from {self._storage.path / self._storage_tokens_path} "
                  f"should be of type dict, but is '{type(endpoint_tokens)}'.")
            sys.exit(1)

        access_token = endpoint_tokens.get("access", None)
        refresh_token = endpoint_tokens.get("refresh", None)

        if not access_token:
            print(f"Error: No access token in {self._storage.path / self._storage_tokens_path}.")
            sys.exit(1)
        if not refresh_token:
            print(f"Error: No refresh token in {self._storage.path / self._storage_tokens_path}.")
            sys.exit(1)

        return access_token, refresh_token

    def _old_tokens_fallback(self) -> None:
        """Execute a fallback mechanism to ensure that users with old tokens path have the same JSON tokens format."""
        tokens = self._storage.read_json(self._storage_tokens_path)

        access_token = tokens.get("access", None)
        refresh_token = tokens.get("refresh", None)

        if self._base_url not in tokens and access_token and refresh_token:
            self._storage.write_json({self._base_url: tokens}, self._storage_tokens_path)

    def login(self, timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Login user to the API using username and password and store tokens to storage.

        :param timeout: Request timeout
        """
        # login - generate tokens (access and refresh token) and then save them to storage
        # note that we do not use self._request to prevent possible cyclic recursion errors
        response = requests.post(self._url("/v2/token/"), headers=self.DEFAULT_HEADERS.copy(),
                                 json={"username": self._username, "password": self._password}, timeout=timeout)
        if response.ok:
            self._storage.update_json({self._base_url: response.json()}, self._storage_tokens_path)
        else:
            print(self._format_api_error(response))
            sys.exit(1)

    def _refresh_login(self, timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Login user to the API using the tokens (access and refresh token) from storage.

        :param timeout: Request timeout
        """
        # get existing tokens and then refresh access token and save it to local storage
        # note that we do not use self._request to prevent possible cyclic recursion errors
        _, refresh_token = self._get_tokens()
        response_token_refresh = requests.post(self._url("/v2/token/refresh/"), headers=self.DEFAULT_HEADERS.copy(),
                                               json={"refresh": refresh_token}, timeout=timeout)
        if response_token_refresh.ok:
            refreshed_access_token = response_token_refresh.json().get("access", None)
            if not refreshed_access_token:
                print("Error: Refreshing access token failed.")
                sys.exit(1)

            access_token = refreshed_access_token
            self._storage.update_json({
                self._base_url: {
                    "access": access_token,
                    "refresh": refresh_token
                }
            }, self._storage_tokens_path)
        else:
            print(self._format_api_error(response_token_refresh))
            sys.exit(1)

    # pylint: disable=too-many-arguments
    def _request(self, method: str, path: str, authorize: Optional[bool] = True,
                 headers: Optional[Dict[str, str]] = None, payload: Optional[Dict[str, Any]] = None,
                 timeout: int = DEFAULT_TIMEOUT, allow_auth_retry: bool = True) -> requests.Response:
        """
        Send HTTP request.

        :param path: API endpoint path
        :param authorize: Add Authorization header to authorize request (True/False)
        :param headers: Request headers (JSON payload dict)
        :param payload: Request payload (JSON payload dict)
        :param timeout: Request timeout
        :param allow_auth_retry: Whether to allow reauthenticating and retrying the request
        :return: Response object
        """
        # initiate login from start if username and password have been provided and tokens do not exist yet
        if self._username and self._password and not self._storage.exists("tokens"):
            self._storage.remove("tokens")
            self.login()

        # initiate login from start if endpoint does not exist in tokens
        if self._storage.exists(self._storage_tokens_path):
            tokens = self._storage.read_json(self._storage_tokens_path)
            endpoint_tokens = tokens.get(self._base_url, None)
            if not endpoint_tokens:
                self.login()

        # combine request headers (default + authorization + others)
        request_headers = self.DEFAULT_HEADERS.copy()
        if authorize:
            access_token, _ = self._get_tokens()
            request_headers.update({"Authorization": f"Bearer {access_token}"})
        request_headers.update(headers if headers is not None else {})

        # try to make a request
        try:
            response = requests.request(
                method, self._url(path),
                headers=request_headers, json=payload if payload is not None else {}, timeout=timeout
            )
        except requests.exceptions.RequestException as e:
            print(f"API error: {str(e)}")
            sys.exit(1)

        # if request fails for one time try to login and make a request again
        if response.status_code == 401:
            if allow_auth_retry:
                self._refresh_login(timeout)
                # retry, but don't allow any more auth retries
                return self._request(method, path, authorize, headers, payload, timeout, allow_auth_retry=False)

            print("Request error after reauthenticating.")
            sys.exit(1)
        else:
            # check if response is ok and can be converted to JSON
            if response.ok:
                try:
                    response.json()
                    return response
                except ValueError as e:
                    print(f"Error: {e}")
                    sys.exit(1)
            else:
                print(self._format_api_error(response))
                sys.exit(1)

    def get(self, path: str, authorize: Optional[bool] = True, headers: Optional[Dict[str, str]] = None,
            timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
        """
        Send GET request.

        :param path: API endpoint path
        :param authorize: Add Authorization header to authorize request (True/False)
        :param headers: Request headers (JSON payload dict)
        :param timeout: Request timeout
        :return: Response object
        """
        return self._request("GET", path, authorize=authorize, headers=headers, timeout=timeout)

    def post(self, path: str, authorize: Optional[bool] = True, headers: Optional[Dict[str, str]] = None,
             payload: Optional[Dict[str, Any]] = None, timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
        """
        Send POST request.

        :param path: API endpoint path
        :param authorize: Add Authorization header to authorize request (True/False)
        :param headers: Request headers (JSON payload dict)
        :param payload: Request payload (JSON payload dict)
        :param timeout: Request timeout in seconds
        :return: Response object
        """
        return self._request("POST", path, authorize, headers, payload, timeout)

    def patch(self, path: str, authorize: Optional[bool] = True, headers: Optional[Dict[str, str]] = None,
              payload: Optional[Dict[str, Any]] = None, timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
        """
        Send PATCH request.

        :param path: API endpoint path
        :param authorize: Add Authorization header to authorize request (True/False)
        :param headers: Request headers (JSON payload dict)
        :param payload: Request payload (JSON payload dict)
        :param timeout: Request timeout in seconds
        :return: Response object
        """
        return self._request("PATCH", path, authorize, headers, payload, timeout)

    def put(self, path: str, authorize: Optional[bool] = True, headers: Optional[Dict[str, str]] = None,
            payload: Optional[Dict[str, Any]] = None, timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
        """
        Send PUT request.

        :param path: API endpoint path
        :param authorize: Add Authorization header to authorize request (True/False)
        :param headers: Request headers (JSON payload dict)
        :param payload: Request payload (JSON payload dict)
        :param timeout: Request timeout in seconds
        :return: Response object
        """
        return self._request("PUT", path, authorize, headers, payload, timeout)

    def delete(self, path: str, authorize: Optional[bool] = True, headers: Optional[Dict[str, str]] = None,
               timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
        """
        Send DELETE request.

        :param path: API endpoint path
        :param authorize: Add Authorization header to authorize request (True/False)
        :param headers: Request headers (JSON payload dict)
        :param timeout: Request timeout in seconds
        :return: Response object
        """
        return self._request("DELETE", path, authorize=authorize, headers=headers, timeout=timeout)

    def _format_api_error(self, response: requests.Response) -> str:
        """
        Format API error.

        :param response: Response object
        :return: Formatted API error as string
        """
        try:
            try:
                return f"API error: {response.status_code} - {response.json()['message']}"
            except KeyError:
                return f"API error: {response.status_code} - {response.json()['detail']}"
        except (ValueError, KeyError):
            return f"API error: {response.status_code}"
