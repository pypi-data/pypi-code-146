import json
import unittest

import mock
import requests
from six.moves import http_client


def _make_credentials():
    import google.auth.credentials

    return mock.Mock(spec=google.auth.credentials.Credentials)


def _make_connection(*responses):
    import google.cloud.storage._http
    from google.cloud.exceptions import NotFound

    mock_conn = mock.create_autospec(google.cloud.storage._http.Connection)
    mock_conn.user_agent = "testing 1.2.3"
    mock_conn.api_request.side_effect = list(responses) + [NotFound("miss")]
    return mock_conn


def _make_response(status=http_client.OK, content=b"", headers={}):
    response = requests.Response()
    response.status_code = status
    response._content = content
    response.headers = headers
    response.request = requests.Request()
    return response


def _make_json_response(data, status=http_client.OK, headers=None):
    headers = headers or {}
    headers["Content-Type"] = "application/json"
    return _make_response(
        status=status, content=json.dumps(data).encode("utf-8"), headers=headers
    )


def _make_requests_session(responses):
    session = mock.create_autospec(requests.Session, instance=True)
    session.request.side_effect = responses
    return session


class TestGCSClient(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from continual.python.blob.gcs import GoogleCloudStorage

        return GoogleCloudStorage

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_valid_resource_url(self):
        EMPTY_URL = ""
        self.assertFalse(self._get_target_class().is_valid_url(EMPTY_URL))

        with self.assertRaises(ValueError):
            client = self._make_one(EMPTY_URL)

        NO_BUCKET_URL = "gs://"
        self.assertFalse(self._get_target_class().is_valid_url(NO_BUCKET_URL))

        with self.assertRaises(ValueError):
            client = self._make_one(NO_BUCKET_URL)

        VALID_URL = "gs://bucket"
        self.assertTrue(self._get_target_class().is_valid_url(VALID_URL))

        client = self._make_one(VALID_URL)
        self.assertEqual(client.bucket_name, "bucket")

    def test_ctor_connection_type(self):
        from google.cloud._http import ClientInfo
        from google.cloud.storage._http import Connection

        PROJECT = "continual-fake"
        RESOURCE_URL = "gs://continual-test"
        credentials = _make_credentials()

        client = self._make_one(RESOURCE_URL, project=PROJECT, credentials=credentials)

        client = client.client

        self.assertEqual(client.project, PROJECT)
        self.assertIsInstance(client._connection, Connection)
        self.assertIs(client._connection.credentials, credentials)
        self.assertIsNone(client.current_batch)
        self.assertEqual(list(client._batch_stack), [])
        self.assertIsInstance(client._connection._client_info, ClientInfo)
        self.assertEqual(
            client._connection.API_BASE_URL, Connection.DEFAULT_API_ENDPOINT
        )


if __name__ == "__main__":
    # TODO(sahil): add testing for upload and download
    unittest.main()
