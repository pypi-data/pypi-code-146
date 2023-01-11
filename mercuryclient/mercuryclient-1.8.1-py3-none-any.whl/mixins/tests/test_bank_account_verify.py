from unittest import mock
from unittest import TestCase

from mercuryclient.api import MercuryApi
from mercuryclient.types.bank_account_verify.request import AccountVerifyRequest


class AccountVerifyMixinTest(TestCase):
    def setUp(self):

        self.client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )

        self.request_obj = AccountVerifyRequest(
            name="test",
            phone="9874563210",
            bank_account_number="874512369854",
            bank_ifsc_code="ES001",
        )

        self.expected_dict = {
            "name": "test",
            "phone": "9874563210",
            "bank_account_number": "874512369854",
            "bank_ifsc_code": "ES001",
            "profile": "some_profile",
            "provider": "some_provider",
        }

        self.post_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._post_json_http_request"
        ).start()
        self.addCleanup(self.post_api_mock.stop)

    def test_request_account_verify(self):

        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        self.client.verify_bank_account(
            self.request_obj, "some_provider", "some_profile"
        )
        self.post_api_mock.assert_called_with(
            path="api/v1/account_verify/",
            data=self.expected_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.verify_bank_account(
                self.request_obj, "some_provider", "some_profile"
            )

    def test_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_id = self.client.verify_bank_account(
            self.request_obj, "some_provider", "some_profile"
        )
        self.assertEqual(request_id["request_id"], "random_string")
