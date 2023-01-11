import base64
import enum
import hashlib
import http.server
import secrets
import socketserver
import sys
import time
from typing import Optional
from typing import Tuple
from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlparse

import attrs
import click
import requests

from tecton import conf

AUTH_SERVER = "https://login.tecton.ai/oauth2/default/.well-known/oauth-authorization-server"
USER_INFO_ENDPOINT = "https://login.tecton.ai/oauth2/default/v1/userinfo"

# this must match the uri that the okta application was configured with
OKTA_EXPECTED_PORTS = [10003, 10013, 10023]

# our http server will populate this when it receives the callback from okta
_CALLBACK_PATH = None


class OktaCallbackReceivingServer(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        global _CALLBACK_PATH
        _CALLBACK_PATH = self.path
        self.send_response(301)
        self.send_header("Location", "https://www.tecton.ai/authentication-success")
        self.end_headers()


@attrs.frozen
class UserProfile:
    name: str
    email: str


def get_metadata():
    try:
        response = requests.get(AUTH_SERVER)
        response.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(e)
    return response.json()


# Okta docs: https://developer.okta.com/docs/guides/refresh-tokens/use-refresh-token/
class RefreshFlow:
    def __init__(self):
        self.metadata = get_metadata()

    def get_tokens(self, refresh_token):
        params = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "client_id": conf.get_or_none("CLI_CLIENT_ID"),
            "scope": "openid profile email",
        }
        try:
            return get_tokens_helper(self.metadata["token_endpoint"], params)
        except requests.RequestException as e:
            print("Authorization token expired. Please reauthenticate with `tecton login`", file=sys.stderr)
            sys.exit(1)


class AuthFlowType(enum.Enum):
    # Spin up local http server that can intercept the okta callback and avoid having to
    # copy & paste
    BROWSER_HANDS_FREE = 1

    # User manually opens link to login, and has to copy & paste the code.
    BROWSER_MANUAL = 2

    # Tecton-internal session token authorization.
    SESSION_TOKEN = 3


# Okta docs: https://developer.okta.com/docs/guides/implement-auth-code-pkce/use-flow/
class OktaAuthorizationFlow:
    def __init__(
        self, auth_flow_type: AuthFlowType = AuthFlowType.BROWSER_HANDS_FREE, okta_session_token: Optional[str] = None
    ):
        self.metadata = get_metadata()
        self.auth_flow_type = auth_flow_type

        self.okta_session_token = okta_session_token

    def build_authorization_url(self, code_verifier: str, redirect_uri: str) -> Tuple[str, str, str]:
        # base64's `urlsafe_b64encode` uses '=' as padding. These are not URL safe when used in URL paramaters.
        code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest()).rstrip(b"=")

        state = str(secrets.randbits(64))

        params = {
            "response_type": "code",
            "client_id": conf.get_or_none("CLI_CLIENT_ID"),
            "redirect_uri": redirect_uri,
            "state": state,
            "scope": "openid offline_access profile email",
            "code_challenge_method": "S256",
            "code_challenge": code_challenge,
        }
        if self.auth_flow_type == AuthFlowType.SESSION_TOKEN:
            params["sessionToken"] = self.okta_session_token
            params["response_mode"] = "query"
        authorize_url = f"{self.metadata['authorization_endpoint']}?{urlencode(params)}"
        return authorize_url, state

    def _browser_auth(self, code_verifier: str) -> Tuple[str, str]:
        for port in OKTA_EXPECTED_PORTS:
            try:
                httpd = socketserver.TCPServer(("", int(port)), OktaCallbackReceivingServer)
                break
            except OSError as e:
                # socket in use, try other port
                if e.errno == 48:
                    continue
                else:
                    print(
                        "Encountered error with authorization callback. Your environment may not support automatic login; try running `tecton login --manual` instead.",
                        file=sys.stderr,
                    )
                    sys.exit(1)
        else:
            raise e

        redirect_uri = f"http://localhost:{port}/authorization/callback"
        authorize_url, state = self.build_authorization_url(code_verifier, redirect_uri)
        print(f"Requesting authorization for Tecton CLI via browser. ")
        time.sleep(2)
        try:
            print("If browser doesn't open automatically, visit the following link:")
            print(f"{authorize_url}")
            click.launch(authorize_url)
            httpd.handle_request()
        finally:
            httpd.server_close()

        return self._extract_code_from_url(_CALLBACK_PATH, state), redirect_uri

    def _extract_code_from_url(self, url: str, state: str) -> str:
        parsed = parse_qs(urlparse(url).query)
        if "error" in parsed:
            print(f"Encountered error: {parsed['error']}", file=sys.stderr)
            if "access_denied" in parsed["error"]:
                print(
                    "Please contact your Tecton administrator to verify you have been granted cluster access.",
                    file=sys.stderr,
                )
            sys.exit(1)
        code = parsed["code"][0]
        assert state == parsed["state"][0]
        from tecton.cli import printer

        printer.safe_print("✅ Authentication successful!")
        return code

    def _manual_auth(self, authorize_url):
        print("Please visit the following link to login and access the authentication code:")
        print(f"{authorize_url}")
        code = input("Paste the authentication code here:").strip()
        return code

    # NOTE: this is for internal use only. Requires an Okta session token.
    # This works by leveraging the Okta session token to skip browser-based
    # Okta authentication. The parameters are stored in the redirect uri from
    # Okta. https://developer.okta.com/docs/reference/api/oidc/#authorize
    def _session_token_auth(self, authorize_url: str, state: str) -> str:
        # We disallow redirects so that we can extract the code from the
        # redirect location.
        r = requests.get(authorize_url, allow_redirects=False)
        r.raise_for_status()
        if r.status_code != 302:
            print("Unsuccessful headless Okta auth.", file=sys.stderr)
            sys.exit(1)
        url = r.headers.get("location")
        return self._extract_code_from_url(url, state)

    # To receive the auth code, we send the user to their browser to login to okta.
    # Once they've logged in, Okta will redirect them to a locally served webpage with the auth code.
    # Then, this function will return that auth code.
    def get_authorization_code(self) -> Tuple[str, str, str]:

        code_verifier = secrets.token_urlsafe(43)

        if self.auth_flow_type == AuthFlowType.BROWSER_HANDS_FREE:
            code, redirect_uri = self._browser_auth(code_verifier)
            return code, code_verifier, redirect_uri

        redirect_uri = "https://www.tecton.ai/authorization-callback"
        authorize_url, state = self.build_authorization_url(code_verifier, redirect_uri)

        if self.auth_flow_type == AuthFlowType.SESSION_TOKEN:
            code = self._session_token_auth(authorize_url, state)
        else:
            code = self._manual_auth(authorize_url)
        return code, code_verifier, redirect_uri

    def get_tokens(self, auth_code, code_verifier, redirect_uri):
        params = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "code_verifier": code_verifier,
            "redirect_uri": redirect_uri,
            "client_id": conf.get_or_none("CLI_CLIENT_ID"),
        }
        try:
            return get_tokens_helper(self.metadata["token_endpoint"], params)
        except Exception as e:
            raise SystemExit(e)


def get_tokens_helper(endpoint, params):
    response = requests.post(endpoint, data=params)
    response.raise_for_status()

    response_json = response.json()
    access_token = response_json.get("access_token", None)
    id_token = response_json.get("id_token", None)
    refresh_token = response_json.get("refresh_token", None)
    expiration = time.time() + int(response_json.get("expires_in"))
    return access_token, id_token, refresh_token, expiration


# returns None if neither access nor refresh token are found in config
def get_token_refresh_if_needed():
    token = conf.get_or_none("OAUTH_ACCESS_TOKEN")
    if not token:
        return None
    expiration = conf.get_or_none("OAUTH_ACCESS_TOKEN_EXPIRATION")
    if expiration and time.time() < int(expiration):
        return token
    else:
        f = RefreshFlow()
        refresh_token = conf.get_or_none("OAUTH_REFRESH_TOKEN")
        if not refresh_token:
            return None
        access_token, _, _, expiration = f.get_tokens(refresh_token)
        conf.set("OAUTH_ACCESS_TOKEN", access_token)
        conf.set("OAUTH_ACCESS_TOKEN_EXPIRATION", expiration)
        conf.save_okta_tokens(access_token, expiration)
        return access_token


def get_user_profile():
    token = get_token_refresh_if_needed()

    if not token:
        return None

    try:
        header = {"Authorization": f"Bearer {token}"}
        response = requests.get(USER_INFO_ENDPOINT, headers=header)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Unable to get use info. Please try logging in again using `tecton login`")
        raise SystemExit(e)

    response = response.json()
    return UserProfile(name=response["name"], email=response["email"])


if __name__ == "__main__":
    f = OktaAuthorizationFlow()
    code, verifier, redirect_uri = f.get_authorization_code()
    access_token, id_token, refresh_token, expiration = f.get_tokens(code, verifier, redirect_uri)

    rf = RefreshFlow()
    print(rf.get_tokens(refresh_token))
