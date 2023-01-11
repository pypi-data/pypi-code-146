from datetime import date
from unittest import TestCase, mock

from mercuryclient.api import MercuryApi


class OkycVerificationMixinTest(TestCase):
    def setUp(self):
        self.client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )

        self.post_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._post_json_http_request"
        ).start()
        self.addCleanup(self.post_api_mock.stop)
        self.get_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._get_json_http_request"
        ).start()
        self.addCleanup(self.get_api_mock.stop)
        self.request_data = {
            "request_type": "OTP_REQUEST",
            "provider": "zoop",
            "profile": "some_profile",
            "id_number": "ABCDE1234",
        }

    def test_wrong_request_type_raises_exception(self):
        with self.assertRaises(Exception) as exc:
            self.request_data["request_type"] = "Something"
            self.client.initiate_okyc_request(self.request_data)

        self.assertEqual(str(exc.exception), "Something is not a valid request_type")
        self.post_api_mock.assert_not_called()

    def test_request_okyc_verification(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        self.client.initiate_okyc_request(self.request_data)

        self.post_api_mock.assert_called_with(
            "api/v1/okyc_verification/",
            data={
                "provider": "zoop",
                "profile": "some_profile",
                "request_type": "OTP_REQUEST",
                "id_number": "ABCDE1234",
            },
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)

        with self.assertRaises(Exception):
            self.client.initiate_okyc_request(self.request_data)

    def test_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)

        request_id = self.client.initiate_okyc_request(self.request_data)
        self.assertEqual(request_id, "random_string")

    def test_response_verify_okyc(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        self.get_api_mock.return_value = ("random_string", mock_response)
        self.client.get_okyc_response("random_string")

        self.get_api_mock.assert_called_with(
            "api/v1/okyc_verification/",
            headers={"X-Mercury-Request-Id": "random_string"},
            send_request_id=False,
            add_bearer_token=True,
        )

    def test_response_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.get_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.get_okyc_response("random_string")

    def test_response_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json = mock.MagicMock()
        mock_response.json.return_value = {"status": "SUCCESS"}
        self.get_api_mock.return_value = ("random_string", mock_response)

        request_id, result = self.client.get_okyc_response("random_string")
        self.assertEqual(request_id, "random_string")
        self.assertEqual(result["status"], "SUCCESS")
