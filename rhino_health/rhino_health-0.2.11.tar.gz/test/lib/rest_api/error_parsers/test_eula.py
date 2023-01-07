from test.lib.rest_api.api_response_factory import ApiResponseFactory
from test.lib.rhino_session_factory import RhinoSessionFactory

import pytest

from rhino_health.lib.rest_api.error_parsers.eula import EULA_ERROR_MESSAGES, EULAErrorParser


class TestEula:
    def test_eula_error_format_works(self):
        parser = EULAErrorParser()
        for error_message in EULA_ERROR_MESSAGES:
            api_response = ApiResponseFactory.build(
                json_response={"detail": error_message},
                status_code=401,
                session=RhinoSessionFactory(),
            )
            error_message = parser.parse(api_response)
            assert "Please login to" in error_message

    def test_unrelated_error(self):
        parser = EULAErrorParser()
        api_response = ApiResponseFactory.build(
            json_response={"detail": "Password Expired"}, status_code=401
        )
        error_message = parser.parse(api_response)
        assert error_message is None
