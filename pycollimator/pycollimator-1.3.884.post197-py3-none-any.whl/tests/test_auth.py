import sys

from pycollimator import Api, utils
import pytest
from tests import setup_auth_token, ENV


def test_auth_token():
    if ENV == "local":
        return

    token = setup_auth_token()

    print("toekn is", token)
    assert utils.is_uuid(token)


def test_is_uuid():
    assert utils.is_uuid("0f8c8d8f-a0b2-4b1c-b8d9-d5f5c9d5f5c9")
    assert utils.is_uuid("0f8c8d8f-a0b2-4b1c-b8d9-d5f5c9d5f5c9-123") is False
    assert utils.is_uuid("0f8c8d8f-a0b2-4b1c-b8d9-d5f5c9d5f5cZ") is False
    assert utils.is_uuid("1234") is False
    assert utils.is_uuid(None) is False


def test_api_status():
    response = Api.get(f"{Api.BASE_PATH}/status")
    assert response["status"] == "OK"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
