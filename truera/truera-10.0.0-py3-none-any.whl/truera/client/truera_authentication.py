import time
from typing import Callable

import jwt
import requests

from truera.client.public.auth_details import AuthDetails
from truera.client.public.auth_details import AuthDetailsMode


class TrueraAuthentication:

    def get_auth_details(self) -> AuthDetails:
        pass

    def set_connection_string(self, connection_string: str):
        pass


class AnonAuthentication(TrueraAuthentication):

    def __init__(self) -> None:
        self.auth_details = AuthDetails(mode=AuthDetailsMode.ANON_AUTH)

    def get_auth_details(self) -> AuthDetails:
        return self.auth_details


class BasicAuthentication(TrueraAuthentication):
    """Basic authentication for BaseTrueraWorkspace.
    """

    def __init__(self, username: str, password: str) -> None:
        """Construct `BasicAuth` for BaseTrueraWorkspace.

        Args:
            username: Username for the basic auth credentials.
            password: Password for the basic auth credentials.
        """
        self.auth_details = AuthDetails(
            mode=AuthDetailsMode.BASIC_AUTH,
            username=username,
            password=password
        )

    def get_auth_details(self) -> AuthDetails:
        return self.auth_details


class TokenAuthentication(TrueraAuthentication):
    """Token authentication for BaseTrueraWorkspace.
    """

    def __init__(self, token: str) -> None:
        """Construct `TokenAuth` for BaseTrueraWorkspace.

        Args:
            token: Token containing credentials to authenticate with the services.
        """
        self.token = Token(value=token)
        self.auth_details = AuthDetails(
            mode=AuthDetailsMode.TOKEN_AUTH, token=self.token
        )

    def get_auth_details(self) -> AuthDetails:
        return self.auth_details


class ServiceAccountAuthentication(TrueraAuthentication):
    """Service Account Authentication for BaseTrueraWorkspace.
    """

    def __init__(self, client_id: str, client_secret: str):
        """Construct `ServiceAccountAuth` for BaseTrueraWorkspace.

        Args:
            client_id (str): Client ID from service account credentials.
            client_secret (str): Client secret from service account credentials.
        """

        self.client_id = client_id
        self.client_secret = client_secret
        self.token_endpoint = None

        self.token = Token(refresh_func=self._get_token_refresh_func())
        self.auth_details = AuthDetails(
            mode=AuthDetailsMode.TOKEN_AUTH, token=self.token
        )

    def get_auth_details(self) -> AuthDetails:
        if not self.token_endpoint:
            raise RuntimeError(
                "token_endpoint is not set, call set_connection_string(). Please contact TruEra support."
            )
        return self.auth_details

    def set_connection_string(self, connection_string: str):
        if connection_string:
            self.token_endpoint = f"{connection_string}/oauth/token"
        else:
            raise ValueError("connection_string is empty")

    def _get_token_refresh_func(self) -> Callable[[], str]:

        # Expects self.token_endpoint to be set before refresh_func is called
        # Python scope handles class variables changing on the fly

        def refresh_func() -> str:
            payload = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            }
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            resp = requests.post(
                self.token_endpoint, data=payload, headers=headers
            )
            try:
                resp.raise_for_status()
                return resp.json()['access_token']
            except requests.HTTPError as e:
                raise RuntimeError(
                    f"Could not get service account token, response status code: {e.response.status_code}"
                )

        return refresh_func


class Token:

    def __init__(
        self, value: str = None, refresh_func: Callable[[], str] = None
    ):
        if not (value or refresh_func):
            raise ValueError(
                "Either a value or a refresh_func must be provided to Token class."
            )

        self._token = value
        self.refresh_func = refresh_func

    def __str__(self):
        """Support implicit usage of this class in `str(Token)` or `f"{Token}"`.
        """
        return self.value()

    def value(self) -> str:
        if not self._token or self.is_expired():
            if self.refresh_func:
                self._token = self.refresh_func()
            else:
                raise RuntimeError("The provided token has expired.")
        return self._token

    def is_expired(self) -> bool:
        decoded_jwt = jwt.decode(
            self._token, options={'verify_signature': False}
        )
        return time.time() > decoded_jwt['exp']
