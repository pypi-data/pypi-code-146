from typing import Optional

from auth0.v3.authentication.token_verifier import (
    AsymmetricSignatureVerifier,
    TokenVerifier,
)
from pydantic import BaseModel, Field


class JWT(BaseModel):
    class Config:
        allow_population_by_field_name = True

    # Used to map to an Organization
    client_id: str = Field(alias="azp")

    # The type of the connection in Auth0
    connection_strategy: str = Field(alias="https://api.symops.com/connection_strategy")

    # The name of the connection in Auth0
    connection_name: str = Field(alias="https://api.symops.com/connection_name")

    # Email & Name of the user associated with the JWT
    email: str = Field(alias="https://api.symops.com/email")
    name: str = Field(alias="https://api.symops.com/name")

    # The ID of the user in the underlying IDP
    idp_id: Optional[str] = Field(alias="https://api.symops.com/idp_id", default=None)

    @classmethod
    def from_access_token(cls, access_token: str, auth_url: str) -> "JWT":
        """Decode the provided access token and return a JWT object."""
        verifier = TokenVerifier(
            signature_verifier=AsymmetricSignatureVerifier(
                jwks_url=f"{auth_url}/.well-known/jwks.json",
                algorithm="RS256",
            ),
            issuer=f"{auth_url}/",
            audience="https://api.symops.com",
        )

        decoded_token = verifier.verify(access_token)
        return cls.parse_obj(decoded_token)
