from typing import Any

from pydantic import ValidationError, parse_obj_as
from pytest import mark, raises

from saxo_apy.models import (
    APIEnvironment,
    AuthorizationCode,
    AuthorizationType,
    ClientId,
    ClientSecret,
    GrantType,
    HttpsUrl,
    RefreshToken,
)


@mark.parametrize(
    "scalar, value",
    [
        (ClientId, "0123456789abcdef0123456789abcdef"),
        (ClientSecret, "0123456789abcdef0123456789abcdef"),
        (HttpsUrl, "https://gateway.saxobank.com/openapi/"),
        (GrantType, "Code"),
        (APIEnvironment, "SIM"),
        (APIEnvironment, "LIVE"),
        (AuthorizationCode, "3ed4c58c-936a-41c8-8c37-1bea188206bd"),
        (RefreshToken, "3ed4c58c-936a-41c8-8c37-1bea188206bd"),
        (AuthorizationType, "authorization_code"),
        (AuthorizationType, "refresh_token"),
    ],
)
def test_scalars(scalar: Any, value: str) -> None:
    """Test all scalars defined in models.py."""
    parse_obj_as(scalar, value)


@mark.parametrize(
    "scalar, value",
    [
        (ClientId, "123"),
        (ClientSecret, "456"),
        (HttpsUrl, "http://gateway.saxobank.com/openapi/"),
        (GrantType, "Codes"),
        (APIEnvironment, "ssim"),
        (APIEnvironment, "liv"),
        (AuthorizationCode, "3ed4c58c936a41c88c371bea188206bd"),
        (RefreshToken, "3ed4c58c936a41c88c371bea188206bd"),
        (AuthorizationType, "auth_code"),
        (AuthorizationType, "refr_token"),
    ],
)
def test_scalars_bad_input(scalar: Any, value: str) -> None:
    with raises(ValidationError):
        parse_obj_as(scalar, value)
