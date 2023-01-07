import logging
from enum import Enum
from typing import Optional

import arrow
import requests
from typing_extensions import TypedDict

from rhino_health.lib.rest_api.api_request import APIRequest
from rhino_health.lib.rest_api.api_response import APIResponse
from rhino_health.lib.rest_api.request_adapter import RequestAdapter
from rhino_health.lib.utils import url_for


class OauthProvider(Enum):
    GOOGLE = "google"
    OKTA = "okta"


class SSOAuthenticationDetails(TypedDict):
    """
    @autoapi True
    """

    sso_access_token: Optional[str]
    """The SSO Access Token, required for most SSO Flows"""
    sso_id_token: Optional[str]
    """The ID Token, optional for certain flows"""
    sso_provider: Optional[OauthProvider]
    """Which SSO Provider are you loggin in with"""
    sso_client: Optional[str]
    """Which SSO Client are you logging in with for client provided SSO Integrations"""


class AuthenticationDetails(SSOAuthenticationDetails):
    """
    @autoapi False Hide these options from the public facing documentation
    # TODO: Better solution for internal/external interface difference
    """

    email: Optional[str]
    """The email of the account you are logging in with"""
    password: Optional[str]
    """The password of the account you are logging in with, if using password"""


class RhinoAuthenticator(RequestAdapter):
    """
    Keeps track of authenticating with our backend API
    """

    AUTHORIZATION_KEY = "authorization"
    UNAUTHENTICATED_STATUS_CODE = 401
    DEFAULT_MAX_RETRY_COUNT = 2

    def __init__(
        self,
        base_url: str,
        authentication_details: AuthenticationDetails,
        otp_code: Optional[str] = None,
        max_retry_count: int = DEFAULT_MAX_RETRY_COUNT,
    ):
        # TODO: Include active_workgroup in the future
        self.base_url = base_url
        self.authentication_details = authentication_details
        self.otp_code = otp_code
        self.max_retry_count = max_retry_count
        self.login_token: Optional[str] = None
        self.login_timeout: Optional[arrow.Arrow] = None
        self.refresh_token: Optional[str] = None
        self.refresh_timeout: Optional[arrow.Arrow] = None

    @property
    def email(self):
        """@autoapi False"""
        return self.authentication_details.get("email", None)

    @property
    def password(self):
        """@autoapi False"""
        return self.authentication_details.get("password", None)

    @property
    def sso_access_token(self):
        """@autoapi False"""
        return self.authentication_details.get("sso_access_token", None)

    @property
    def sso_id_token(self):
        """@autoapi False"""
        return self.authentication_details.get("sso_id_token", None)

    @property
    def sso_provider(self):
        """@autoapi False"""
        return self.authentication_details.get("sso_provider", None)

    @property
    def sso_client(self):
        """@autoapi False"""
        return self.authentication_details.get("sso_client", None)

    @property
    def _is_using_username_and_password(self) -> bool:
        return bool(self.email and self.password)

    @property
    def _is_using_sso(self):
        return (self.sso_access_token or self.sso_id_token) and self.sso_provider

    def _login(self):
        if not self._is_using_username_and_password and not self._is_using_sso:
            raise RuntimeError("Must provide either username and password or SSO Credentials")
        if self._is_using_sso:
            self._login_via_sso()
        else:
            self._login_via_username_password()

    def _save_rhino_auth_token(self, raw_response):
        # TODO: Parse timeout hours from the token instead of hardcode
        self.login_token = raw_response["access"]
        self.login_timeout = arrow.utcnow().shift(minutes=5)
        self.refresh_token = raw_response["refresh"]
        self.refresh_timeout = arrow.utcnow().shift(hours=10)

    def _login_via_username_password(self):
        data = {"email": self.email, "password": self.password}
        if self.otp_code:
            data["otp_code"] = self.otp_code
        raw_response = requests.post(
            url_for(self.base_url, "auth/obtain_token"),
            data=data,
        ).json()
        if "access" in raw_response:
            self._save_rhino_auth_token(raw_response)
        else:
            raise Exception(raw_response.get("detail", "Error occurred trying to connect"))

    def _login_via_sso(self):
        data = {"response": {"token": self.sso_access_token}, "provider": self.sso_provider}
        if self.email:
            data["response"]["email"] = self.email
        if self.sso_id_token:
            data["response"]["id_token"] = self.sso_id_token
        if self.sso_client:
            data["client"] = self.sso_client
        try:
            raw_response = requests.post(
                url_for(self.base_url, "auth/oauth_token"),
                json=data,
            ).json()
            if "access" in raw_response:
                self._save_rhino_auth_token(raw_response)
            else:
                raise Exception(raw_response.get("detail", "Error occurred trying to connect"))
        except:
            raise Exception("Unable to authenticate, please check your credentials")

    def _refresh_token(self):
        raw_response = requests.post(
            url_for(self.base_url, "auth/refresh_token"),
            data={"refresh": self.refresh_token},
        ).json()
        self.login_token = raw_response.get("access")
        if not self.login_token:
            raise ValueError("Invalid email or password")

    def _should_reauthenticate(self):
        return (self.login_token is None) or (arrow.utcnow() > self.login_timeout)

    def _can_refresh(self):
        refresh_expired = (self.refresh_timeout is None) or (arrow.utcnow() > self.refresh_timeout)
        return self._refresh_token is not None and not refresh_expired

    def authenticate(self):
        if self._can_refresh():
            self._refresh_token()
        else:
            self._login()

    def before_request(self, api_request: APIRequest, adapter_kwargs: dict):
        if self._should_reauthenticate():
            self.authenticate()
        api_request.headers[self.AUTHORIZATION_KEY] = f"Bearer {self.login_token}"

    def after_request(
        self, api_request: APIRequest, api_response: APIResponse, adapter_kwargs: dict
    ):
        unauthenticated = api_response.status_code == self.UNAUTHENTICATED_STATUS_CODE
        retry_allowed = api_request.request_count <= self.max_retry_count
        if unauthenticated and retry_allowed:
            api_request.request_status = APIRequest.RequestStatus.RETRY
            logging.debug("Refreshing login token")
            self.authenticate()
            api_request.request_count += 1
        return
