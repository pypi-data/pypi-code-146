"""
    This module provides functions and classes that helps with programmatic interaction with
    Identity Platform and related authentication services.
"""
# ============================ imports =========================================
from google_auth_oauthlib import flow
import firebase_admin
from firebase_admin import auth as firebase_auth
from google.oauth2 import service_account
import requests
import json
from typing import Optional, List, Dict, Tuple
import enum
import logging
import dataclasses

# ============================ constants and data ============================
# Info about Google Auth Scopes can be found at:
#   https://developers.google.com/identity/protocols/oauth2/scopes
_DEFAULT_AUTH_SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]


@dataclasses.dataclass
class AuthenticationInfo:
    """This class holds information of the authentication process supported by the
    provided functions in this module.

    Args:
        identity_platform_credentials: The IdentityPlatform response for the method
            accounts.signInWithIdp. More info at:
                https://cloud.google.com/identity-platform/docs/reference/rest/v1/accounts/signInWithIdp#response-body
        role_service_account_credentials: The Service Account credentials created for the
            user appropriate Role.
    """

    class UserRole(enum.Enum):
        Admin = 'Admin'
        Client = 'Client'

    identity_platform_credentials: Dict = dataclasses.field(default_factory=dict)
    role_service_account_credentials: service_account.Credentials = None
    user_role: UserRole = None

    @property
    def user_email(self) -> Optional[str]:
        """Returns the user email found in the Identity Platform authenticated
        credentials.
        """
        if "email" in self.identity_platform_credentials:
            return self.identity_platform_credentials["email"]
        else:
            logging.warning("No email field found in identity platform credentials.")
            return None

    @property
    def id_token(self) -> Optional[str]:
        """Returns the Identity Platform Token found in the Identity Platform authenticated"""
        if "idToken" in self.identity_platform_credentials:
            return self.identity_platform_credentials["idToken"]
        else:
            logging.warning("No idToken field found in identity platform credentials.")
            return None

    def is_user_logged_in(self) -> bool:
        # Todo: add a more detailed verification
        return bool(self.identity_platform_credentials) and bool(
            self.role_service_account_credentials
        )


# ========================== Functions =======================================
def get_google_oauth_flow(
    client_oauth_secret: str,
    redirect_url: str = "localhost:8501",
    scopes: List[str] = _DEFAULT_AUTH_SCOPES,
) -> flow.Flow:
    """Returns a Google Authentication Flow.

    More info can be found in the API docs:
        https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html

    Args:
        client_oauth_secret(str): The OAuth 2.0 client ID for web application.
        redirect_url(str): The redirect URL to be used with authentication flow
        scopes(List[str]): The list of scopes to use in with OAuth2.0 flow.


    """
    try:
        _app_flow = flow.Flow.from_client_config(
            json.loads(client_oauth_secret),
            scopes=scopes,
            redirect_uri=redirect_url,
        )
    except ValueError:
        raise RuntimeError(
            "Client configuration is not in the correct format. Impossible"
            "to create OAuth flow."
        )
    else:
        return _app_flow


def sing_in_user_in_identity_platform(
    auth_code: str,
    firebase_api_key,
    client_oauth_secret: str,
    redirect_url: str = "localhost:8501",
    scopes: List[str] = _DEFAULT_AUTH_SCOPES,
) -> Optional[Dict]:
    """Sign in an user in Identity Platform using the received OAuth2.0 code
    for the user after successful OAuth2.0 authentication.

    More info at:
        https://cloud.google.com/identity-platform/docs/reference/rest/v1/accounts/signInWithIdp

    Args:
        auth_code: The authorization code response returned by Google afer the user
            successfully authenticated himself using the OAuth2.0 Flow
        client_oauth_secret(str): The OAuth 2.0 client ID for web application.
        redirect_url(str): The redirect URL to be used with authentication flow
        scopes(List[str]): The list of scopes to use in with OAuth2.0 flow.
    """
    google_auth_flow = get_google_oauth_flow(client_oauth_secret, redirect_url, scopes)
    google_auth_flow.fetch_token(code=auth_code)
    oauth_credentials = google_auth_flow.credentials

    logging.debug("Access token obtained from Google Auth flow consent")
    logging.debug("Trying to sing in into Identity Platform")

    # Sign in into identity platform
    query_params = {"key": firebase_api_key}
    headers = {"Content-Type": "application/json"}
    data = {
        "postBody": f"access_token={oauth_credentials.token}&providerId=google.com",
        "requestUri": "http://localhost",  # This can be localhost because manual credentials were provided
        "returnIdpCredential": True,
        "returnSecureToken": True,
    }

    r = requests.post(
        "https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp",
        params=query_params,
        headers=headers,
        data=json.dumps(data),
    )

    if r.status_code == 200:
        identity_platform_credentials = json.loads(r.content.decode())
        logging.info(
            f"User successfully authenticated with Google "
            f'Identity Platform {identity_platform_credentials["fullName"]}'
        )
        return identity_platform_credentials

    else:
        logging.error(
            f"Unexpected Error when authenticating the user "
            f"with Identity Platform: {r.content.decode()}"
        )
        return None


def _get_firebase_default_app(
    firebase_default_service_account: str,
) -> Optional[firebase_admin.App]:
    """Returns the default firebase APP given the Firebase default service account

    If there's some problem with the creation of the App instance, then the streamlit
    app will set the unexpected error flag for the session.

    Args:
        firebase_default_service_account: The default service account from
            Firebase as a string
    """
    try:
        json_acc_info = json.loads(firebase_default_service_account, strict=False)

    except:
        logging.error(
            "There was an error parsing the Firebase default "
            "service account information"
        )
        return None

    try:
        credentials = firebase_admin.credentials.Certificate(json_acc_info)
        firebase_app = firebase_admin.initialize_app(credentials)
    except:
        logging.error(
            "There was an error creating the Firebase Default " "Application instance"
        )
        return None
    else:
        return firebase_app


def _get_user_role(user_email: str) -> Optional[str]:
    """Returns the User Role for the logged user in the state.

    If the user doesn't have a role (claim) assigned in Identity Platform, then
    the app will set the unexpected error flag.

    TODO: Validate the role against a list of expected roles. Add this when the roles functionalities
        and the application use cases for each type of role are being implemented.

    Args:
        user_email(str): The user email address to request the claims for in Identity Platform.
    """
    user = firebase_auth.get_user_by_email(user_email)
    claims = user.custom_claims
    if "role" not in claims:
        logging.error("No role/custom claim found for the authenticated user")

        return None

    return claims["role"]


def get_principal_credentials(
    user_email: str,
    client_oauth_secret: str,
    id_token: str,
    firebase_default_service_account: str,
) -> Tuple[Optional[service_account.Credentials], AuthenticationInfo.UserRole]:
    """Request the Service Account Credentials to Firestore using the current
    user logged Role.

    Args:
        user_email(str): The user email to request the claims for.
        client_oauth_secret(str): The OAuth 2.0 client ID for web application.
        id_token(str): The Identity Platform ID Token for the user.

    Returns:
        The service_account.Credentials for the user. None if there's an error.
    """
    firebase_app: firebase_admin.App = _get_firebase_default_app(
        firebase_default_service_account
    )
    if firebase_app is None:
        logging.error(
            "Could not create the default Firebase App. "
            "Principal Credentials could not be obtained"
        )
        return None, None

    user_role = _get_user_role(user_email)
    if not user_role:
        logging.error("No user role found for the user.")
        return None, None

    project_id = json.loads(client_oauth_secret)["web"]["project_id"]

    # Perform Request to Firestore.
    # TODO: This request should be more reliable.
    firestore_url = "https://firestore.googleapis.com/v1"
    default_db_path = f"projects/{project_id}/databases/(default)/documents"
    collection = f"user_roles/{user_role}"

    logging.info(f"Requesting service account for user role: {user_role}")

    headers = {
        "Authorization": "Bearer " + id_token,
        "Content-Type": "application/json",
    }
    response = requests.get(
        f"{firestore_url}/{default_db_path}/{collection}", headers=headers
    )

    if response.status_code == 200:
        try:
            content = json.loads(response.content.decode())
            service_account_info = json.loads(content["fields"]["key"]["stringValue"])
            role_credentials = service_account.Credentials.from_service_account_info(
                service_account_info
            )
            logging.info(
                f"SUCCESS obtaining service account credentials for "
                f"the user role: {user_role}"
            )
            return role_credentials, AuthenticationInfo.UserRole(user_role)

        except ValueError:
            logging.error(
                "Could not create service principal credentials for the "
                "service account found"
            )
            return None, None
        finally:
            firebase_admin.delete_app(firebase_admin.get_app())

    else:
        logging.error(
            f"Unexpected response code when requesting "
            f"service account for user role: {response.status_code}"
        )
        firebase_admin.delete_app(firebase_admin.get_app())
        return None, None
