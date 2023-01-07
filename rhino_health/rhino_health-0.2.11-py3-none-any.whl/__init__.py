"""Entry point to using the Rhino Health Python SDK."""

__version__ = "0.2.11"

from typing import Optional

import rhino_health.lib.endpoints
import rhino_health.lib.metrics
from rhino_health.lib.constants import ApiEnvironment
from rhino_health.lib.rest_api.rhino_authenticator import SSOAuthenticationDetails
from rhino_health.lib.rhino_client import SDKVersion
from rhino_health.lib.rhino_session import RhinoSession

# Which modules to autogenerate documentation for
__api__ = [
    "rhino_health.lib.metrics",
    "rhino_health.lib.endpoints",
    "rhino_health.lib.constants",
    "rhino_health.lib.rhino_session",
    "rhino_health.lib.rest_api",
]


def login(
    username=None,
    password=None,
    otp_code=None,
    rhino_api_url=ApiEnvironment.PROD_API_URL,
    sdk_version=SDKVersion.PREVIEW,
    show_traceback=False,
    authentication_details: Optional[SSOAuthenticationDetails] = None,
):
    """
    Login to the Rhino platform and get a RhinoSession to interact with the rest of the system.

    Parameters
    ----------
    username: Optional[str]
        The email you are logging in with if logging in with username/password
    password: Optional[str]
        The password you are logging in with if logging in with username/password
    authentication_details: Optional[AuthenticationDetails]
        Dictionary of authentication information you are logging in with. Refer to Examples and See Also section
    otp_code: Optional[str]
        If 2FA is enabled for the account, the One Time Password code from your 2FA device
    rhino_api_url: Optional[ApiEnvironment]
        Which rhino environent you are working in.
    sdk_version: Optional[SDKVersion]
        Used internally for future backwards compatibility. Use the default
    show_traceback: Optional[bool]
        Should traceback information be included if an error occurs

    Returns
    -------
    session: RhinoSession
        A session object to interact with the cloud API

    Examples
    --------
    >>> import rhino_health
    >>> my_username = "rhino_user@rhinohealth.com" # Replace me
    >>> my_password = "ASecurePasswordYouSet321" # Replace me
    >>> session = rhino_health.login(username=my_username, password=my_password, otp_code=otp_code)
    RhinoSession()

    >>> import rhino_health
    >>> session = rhino_health.login(authentication_details={"sso_access_token": "MyAccessToken", "sso_provider": "google", "sso_client": "my_hospital"})
    RhinoSession()

    See Also
    --------
    rhino_health.lib.constants.ApiEnvironment : List of supported environments
    rhino_health.lib.rhino_session.RhinoSession : Session object with accessible endpoints
    rhino_health.lib.rest_api.rhino_authenticator.SSOAuthenticationDetails: Authentication detail dictionary for login with SSO
    """
    if username and password and not authentication_details:
        authentication_details = {"email": username, "password": password}
    return RhinoSession(
        authentication_details, otp_code, rhino_api_url, sdk_version, show_traceback
    )
