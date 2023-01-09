from dataclasses import dataclass

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fractal_roles.models import Role, TokenPayloadRolesMixin  # type: ignore
from fractal_roles.services import RolesService as BaseRolesService  # type: ignore

from fractal_tokens.services.generic import TokenPayload, TokenService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@dataclass
class TokenPayloadRoles(TokenPayloadRolesMixin, TokenPayload):
    ...


class User(Role):
    ...


class RolesService(BaseRolesService):
    def __init__(self):
        self.roles = [User()]


def rsa_key_pair():
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    key = rsa.generate_private_key(
        backend=default_backend(),
        public_exponent=65537,
        key_size=512,  # use at least 4096 in production
    )

    private_key = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode("utf-8")

    return private_key, key.public_key()


def get_token_payload_roles(
    *,
    token_service: TokenService,
    roles_service: BaseRolesService,
    endpoint: str = "",
    method: str = "get",
    typ: str = "access",
):
    def _get_payload(token: str = Depends(oauth2_scheme)) -> TokenPayloadRoles:
        payload = token_service.verify(token, typ=typ)
        payload = roles_service.verify(payload, endpoint, method)
        return payload

    return _get_payload
