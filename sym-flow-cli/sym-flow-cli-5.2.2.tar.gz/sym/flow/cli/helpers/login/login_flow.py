import uuid
import webbrowser
from abc import ABC, abstractmethod
from http.server import HTTPServer
from typing import Optional, Tuple

import pkce
import requests
from sym.shared.cli.errors import CliError

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.errors import LoginError
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.login.handler import make_handler
from sym.flow.cli.models import AuthToken, Organization, parse_auth_token


class LoginFlow(ABC):
    @abstractmethod
    def login(self, options: GlobalOptions, org: Organization) -> AuthToken:
        pass


class BrowserRedirectFlow(LoginFlow):
    """
    Issue an authorization code request by opening the browser to a particular
    URL. Start a server and wait for the user to successfully login. The browser will
    redirect a successful login back to the locally running server, with a request
    body containing an auth code. With the auth code, obtain an access and refresh token.

    Implements the auth code flow described here:
    https://www.altostra.com/blog/cli-authentication-with-auth0
    """

    port: int

    def __init__(self, port: int):
        self.port = port
        self.browser_login_params = None

    def login(self, options: GlobalOptions, org: Organization) -> Optional[AuthToken]:
        auth_code, code_verifier = self.get_auth_code(options, org)
        if not auth_code:
            return
        return self.get_token_from_code(options, org, auth_code, code_verifier)

    @property
    def redirect_url(self) -> str:
        return f"http://localhost:{self.port}/callback"

    def _new_server(self, options: GlobalOptions, handler):
        for port in range(self.port, self.port + 10):  # try a few
            try:
                return HTTPServer(("localhost", port), handler)
            except OSError as e:
                if e.errno not in (48, 98):  # Address already in use
                    raise
                options.dprint(f"Port {port} in use, trying to increment...")

    def wait_for_code(self, state: str, options: GlobalOptions) -> Optional[str]:
        """
        Starts a server and waits for a request that contains an auth code.
        """
        handler = make_handler(options, state)
        with self._new_server(options, handler) as httpd:
            options.dprint(f"Waiting for an auth code at {self.redirect_url}")
            httpd.handle_request()

            # Bubble up any error message received during handling of the request from the HTTPServer.
            if error_message := getattr(handler, "error_message", None):
                # If we know the problem is that the user just signed up (and therefore their email is not validated),
                # give them a non-error message.
                if "complete sign up" in error_message:
                    cli_output.info(error_message)
                    return
                else:
                    # Otherwise, raise the error message that we got from the HTTP response.
                    raise CliError(error_message)

            # We didn't get an auth_code, but the HTTPServer didn't register any errors.
            if not (auth_code := getattr(handler, "auth_code", None)):
                raise CliError("Unable to get access token from Auth0. Please try again.")

            return auth_code

    def gen_state(self) -> str:
        return str(uuid.uuid4())

    def gen_browser_login_params(self, options: GlobalOptions, org: Organization, force: bool = False) -> str:
        if force or self.browser_login_params is None:
            state = self.gen_state()
            code_verifier = pkce.generate_code_verifier(length=128)
            code_challenge = pkce.get_code_challenge(code_verifier)
            query_params = "&".join(
                [
                    "response_type=code",
                    f"client_id={org.client_id}",
                    "code_challenge_method=S256",
                    f"code_challenge={code_challenge}",
                    f"redirect_uri={self.redirect_url}",
                    f"audience=https://api.symops.com",
                    f"state={state}",
                    "prompt=login",
                ]
            )
            url = f"{options.auth_url}/authorize?{query_params}"
            self.browser_login_params = (url, state, code_verifier)

        return self.browser_login_params

    def get_auth_code(self, options: GlobalOptions, org: Organization) -> Tuple[str, str]:
        """
        Perform the Auth0 code flow by opening the browser with a URL containing query parameters
        that orchestrate the flow. When the user logs in successfully, the browser will follow the
        redirect and issue a request back to the CLI with an auth code.

        Returns an auth code and a PKCE code verifier that both need to be provided to the
        token endpoint when obtaining an auth token.
        """
        (url, state, code_verifier) = self.gen_browser_login_params(options, org)

        webbrowser.open(url)

        auth_code = self.wait_for_code(state, options)
        options.dprint(f"Auth code received: {auth_code}")
        return auth_code, code_verifier

    def get_token_from_code(
        self,
        options: GlobalOptions,
        org: Organization,
        auth_code: str,
        code_verifier: str,
    ) -> AuthToken:
        """
        With the provided auth code and verifier, obtains an auth token.
        """
        data = {
            "grant_type": "authorization_code",
            "client_id": org.client_id,
            "code_verifier": code_verifier,
            "code": auth_code,
            "redirect_uri": self.redirect_url,
        }
        headers = {"content-type": "application/x-www-form-urlencoded"}
        url = f"{options.auth_url}/oauth/token"
        r = requests.post(url, headers=headers, data=data)
        if not r.ok:
            raise LoginError(r.text)

        return parse_auth_token(r.json())
