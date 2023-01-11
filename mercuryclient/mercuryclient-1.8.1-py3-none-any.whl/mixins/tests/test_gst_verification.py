from unittest import mock
from unittest import TestCase

from mercuryclient.api import MercuryApi


class GstVerifyMixinTest(TestCase):
    def setUp(self):

        self.client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )

        self.expected_dict = {
            "profile": "some_profile",
            "provider": "some_provider",
            "gstin_number": "random_numbers",
        }

        self.post_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._post_json_http_request"
        ).start()
        self.addCleanup(self.post_api_mock.stop)
        self.get_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._get_json_http_request"
        ).start()
        self.addCleanup(self.post_api_mock.stop)

    def test_request_verify_gstin(self):

        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        self.client.verify_gstin("random_numbers", "some_provider", "some_profile")
        self.post_api_mock.assert_called_with(
            path="api/v1/gst_verification/",
            data=self.expected_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.verify_gstin("random_numbers", "some_provider", "some_profile")

    def test_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_id = self.client.verify_gstin(
            "random_numbers", "some_provider", "some_profile"
        )
        self.assertEqual(request_id["request_id"], "random_string")

    def test_response_verify_id(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        self.get_api_mock.return_value = ("random_string", mock_response)
        self.client.get_verify_gst_result("random_string")

        self.get_api_mock.assert_called_with(
            "api/v1/gst_verification/",
            headers={"X-Mercury-Request-Id": "random_string"},
            send_request_id=False,
            add_bearer_token=True,
        )

    def test_response_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.get_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.get_verify_gst_result("random_string")

    def test_response_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json = mock.MagicMock()
        mock_response.json.return_value = {"status": "SUCCESS"}
        self.get_api_mock.return_value = ("random_string", mock_response)

        request_id, result = self.client.get_verify_gst_result("random_string")
        self.assertEqual(request_id, "random_string")
        self.assertEqual(result["status"], "SUCCESS")
