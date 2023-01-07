from http.client import HTTPMessage
from typing import Optional
from unittest.mock import ANY, Mock, call, patch

from urllib3 import Retry

from the_spymaster_util.http_client import BaseHttpClient


class ExampleClient(BaseHttpClient):
    def __init__(self, retry_strategy: Optional[Retry] = None):
        super().__init__(base_url="https://jsonplaceholder.typicode.com", retry_strategy=retry_strategy)

    def users(self, **kwargs):
        return self._get("users", {}, **kwargs)

    def dummy(self):
        return self._get("dummy", data={}, parse=False)


def test_basic_call_succeed():
    client = ExampleClient()
    response = client.users()
    assert isinstance(response, list)
    assert len(response) == 10


def test_basic_call_without_log_data():
    client = ExampleClient()
    response = client.users(log_http_data=False)
    assert isinstance(response, list)
    assert len(response) == 10


@patch("urllib3.connectionpool.HTTPConnectionPool._get_conn")
def test_retry_request(mock_get_conn):
    mock_get_conn.return_value.getresponse.side_effect = [
        Mock(status=429, msg=HTTPMessage()),  # Retry #0 (initial)
        Mock(status=429, msg=HTTPMessage()),  # Retry #1
        Mock(status=500, msg=HTTPMessage()),  # Retry #2
        Mock(status=200, msg=HTTPMessage()),  # Retry #3 (last, success)
        Mock(status=200, msg=HTTPMessage()),  # We won't get to this one.
    ]

    retry_strategy = Retry(
        total=3,
        backoff_factor=0.01,
        status_forcelist=[429, 500, 502, 503, 504],  # The HTTP response codes to retry on
        allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS"],  # The HTTP methods to retry on
    )
    client = ExampleClient(retry_strategy=retry_strategy)
    client.dummy()

    actual_calls = mock_get_conn.return_value.request.mock_calls
    assert actual_calls == [
        call("GET", "/dummy", body=None, headers=ANY),
        call("GET", "/dummy", body=None, headers=ANY),
        call("GET", "/dummy", body=None, headers=ANY),
        call("GET", "/dummy", body=None, headers=ANY),
    ]
