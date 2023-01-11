from jose import jwt
from typing import Optional, List, Dict, Union
from lazyops.types import BaseModel

__all__ = [
    "TokenResponse",
    "Jwks",
]


class TokenResponse(BaseModel):
    sub: Optional[str]
    iat: Optional[int]
    exp: Optional[int]
    iss: Optional[str]
    aud: Optional[str]
    jti: Optional[str]
    client_id: Optional[str]
    scope: Optional[str]
    role_names: Optional[List]

    @property
    def user_id(self):
        return self.sub


class Jwks(BaseModel):
    key: Optional[Union[Dict, str]]
    algorithms: Optional[str]
    audience: Optional[str]
    issuer: Optional[str]
    options: Optional[Dict]

    def decode_token(
        self,
        token: str,
    ) -> TokenResponse:
        payload = jwt.decode(
            token,
            key=self.key,
            algorithms=self.algorithms,
            audience=self.audience,
            issuer=self.issuer,
            options=self.options,
        )
        return TokenResponse.parse_obj(payload)
