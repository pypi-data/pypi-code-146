import pytest

from calibration_client import CalibrationClient
from .common.secrets import CLIENT_OAUTH2_INFO, BASE_API_URL


@pytest.fixture(scope='session')
def client():
    return CalibrationClient(
        client_id=CLIENT_OAUTH2_INFO['CLIENT_ID'],
        client_secret=CLIENT_OAUTH2_INFO['CLIENT_SECRET'],
        token_url=CLIENT_OAUTH2_INFO['TOKEN_URL'],
        refresh_url=CLIENT_OAUTH2_INFO['REFRESH_URL'],
        auth_url=CLIENT_OAUTH2_INFO['AUTH_URL'],
        scope=CLIENT_OAUTH2_INFO['SCOPE'],
        user_email=CLIENT_OAUTH2_INFO['EMAIL'],
        base_api_url=BASE_API_URL
    )


# Fixture for use with unittest class-style tests
@pytest.fixture(scope="class")
def client_cls(request, client):
    request.cls.cal_client = client
