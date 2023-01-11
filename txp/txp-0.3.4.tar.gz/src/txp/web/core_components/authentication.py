"""
This module implements the Authentication view for the application.
"""
# ============================ imports =========================================
import oauthlib
import txp.common.utils.authentication_utils as auth
from txp.web.core_components.app_component import AppComponent
import logging
import streamlit as st

# TODO: This might be a problem. The logging configuration is being taken from `txp` package
from txp.common.config import settings

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class AuthenticationComponent(AppComponent):
    def __init__(self):
        super(AuthenticationComponent, self).__init__(
            component_key="authentication_view"
        )
        #  The redirection flow must be set manually. Streamlit doesn't provide a way to obtain the
        #  url host.
        self._CLIENT_OAUTH_SECRET = st.secrets["oauth_secrets"]
        self._FIREBASE_API_KEY = st.secrets["firebase_api_key"]
        self._GOOGLE_OAUTH_REDIRECT = st.secrets["oauth_redirect_url"]
        self._FIREBASE_DEFAULT_SERVICE_ACCOUNT = st.secrets[
            "firebase_default_service_account"
        ]

    def _render(self) -> None:
        if not self._is_google_auth_redirection():
            st.title("Ingresar a Tranxpert")
            google_oauth2_flow = auth.get_google_oauth_flow(
                self._CLIENT_OAUTH_SECRET, self._GOOGLE_OAUTH_REDIRECT
            )

            auth_url, _ = google_oauth2_flow.authorization_url()

            st.write(
                f"""
                    <h4>
                        <a target="_blank" href="{auth_url}" onclick="close();return false;">
                        Ingresar con Google
                        </a>
                    </h4>
                """,
                unsafe_allow_html=True,
            )
        else:
            log.info("User no authenticated. Starting authentication flow")
            self._authenticate_user_and_get_roles()

    @staticmethod
    def _is_google_auth_redirection() -> bool:
        """Returns true if there are query parameters in the URL that matches
        the redirected parameters by Google Auth flow after consent.

        More info:
            https://developers.google.com/identity/protocols/oauth2/web-server#handlingresponse
        """
        params = st.experimental_get_query_params()
        return "code" in params

    @staticmethod
    def _get_auth_code() -> str:
        """Returns the OAuthentication code from the URL Query params"""
        code = st.experimental_get_query_params()["code"][0]
        return code

    def _authenticate_user_and_get_roles(self):
        try:
            identity_platform_credentials = auth.sing_in_user_in_identity_platform(
                self._get_auth_code(),
                self._FIREBASE_API_KEY,
                self._CLIENT_OAUTH_SECRET,
                self._GOOGLE_OAUTH_REDIRECT,
            )
            # st.experimental_set_query_params(**{})
        except oauthlib.oauth2.rfc6749.errors.InvalidGrantError:
            st.experimental_set_query_params(**{})
            st.experimental_rerun()

        if not identity_platform_credentials:
            st.error(
                "Hubo un error al realizar la autenticación."
                "Intente nuevamente o contacte a soporte."
            )
            log.error("Could not sign-in user in Identity Platform")
            return

        self.app_state.authentication_info.identity_platform_credentials = (
            identity_platform_credentials
        )

        role_credentials, role_enum = auth.get_principal_credentials(
            self.app_state.authentication_info.user_email,
            self._CLIENT_OAUTH_SECRET,
            self.app_state.authentication_info.id_token,
            self._FIREBASE_DEFAULT_SERVICE_ACCOUNT,
        )

        if not role_credentials:
            st.error(
                "Hubo un error al realizar la autenticación."
                "Intente nuevamente o contacte a soporte."
            )
            log.error(
                "Could not obtain Role Service Account credentials from Firestore"
            )
            return

        self.app_state.authentication_info.role_service_account_credentials = (
            role_credentials
        )

        self.app_state.authentication_info.user_role = role_enum

        log.info(
            f"Successfully authenticated user with email: "
            f"{self.app_state.authentication_info.user_email}"
        )
        st.experimental_rerun()  # Rerun app now authenticated
