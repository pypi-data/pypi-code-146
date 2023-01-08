import base64
import hashlib
import logging
import os
import re
from urllib import parse
from datetime import datetime, timedelta

import aiohttp
from aiohttp import ClientSession, BasicAuth
from lxml import html

from .abstract_auth import AbstractAuth

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
log = logging.getLogger(__name__)

# Constants
CLIENT_ID = "app.dashtt.pointt.android"
CLIENT_SECRET = "QuKV5lWbLIkZMX65IEzxowqTtp1oD7srDiMwrFuz"
BASE_URL = "https://accounts.ttsignon.com/"
AUTHORIZE_URL = "https://accounts.ttsignon.com/connect/authorize"
ACCESS_TOKEN_URL = "https://accounts.ttsignon.com/connect/token"


class HomecomAuth(AbstractAuth):
    def __init__(self, websession: ClientSession, host: str, auth: BasicAuth):
        """Initialize the auth."""
        super().__init__(websession, host)

        self.auth = auth
        self.expires_in = None
        self.refresh_token = None
        self.access_token = None
        self.issued_at = None

    def is_valid(self) -> bool:
        return (self.issued_at + timedelta(seconds=self.expires_in)) > datetime.utcnow()

    async def async_get_access_token(self) -> str:
        """Return a valid access token."""
        if not self.access_token:
            await self.authenticate()
        if not self.is_valid():
            await self.refresh_access_token()
        if self.access_token:
            return self.access_token
        raise NotAuthenticated()

    async def authenticate(self):
        code_challenge, code_verifier = generate_code_challenge()
        authorize_url = (
            AUTHORIZE_URL
            + "?client_id=app.dashtt.pointt.android&response_type=code&scope=openid%20offline_access"
              "%20user.identity%20user.write%20user.read%20company.identity%20company.read%20tos.write"
              "%20pointt.gateway.claiming%20pointt.gateway.removal%20pointt.gateway.list%20pointt"
              ".gateway.users%20pointt.gateway.resource.dashapp&redirect_uri=com.bosch.tt.dashtt"
              ".pointt%3A%2F&code_challenge_method=S256"
              f"&code_challenge={code_challenge}"
        )
        o_auth_session = aiohttp.ClientSession()
        async with o_auth_session as session:
            log.debug(authorize_url)
            response = await session.get(authorize_url, allow_redirects=True)
            print(response.headers)

            assert response.status == 200
            tree = html.fromstring(await response.text())
            return_url = tree.xpath("//*[@name='ReturnUrl']")[0].get("value")
            verification_token = tree.xpath("//*[@name='__RequestVerificationToken']")[
                0
            ].get("value")
            log.debug(verification_token)
            log.debug(return_url)
            response = await session.post(
                "https://identity-myprofile.bosch.com" + "/ids/login",
                data={
                    "uEmail": self.auth.login,
                    "uPassword": self.auth.password,
                    "ReturnUrl": return_url,
                    "__RequestVerificationToken": verification_token,
                },
                allow_redirects=False,
            )
            log.debug(await response.text())
            log.debug(response.status)
            log.debug(response.headers)
            assert response.status == 302
            location = response.headers["Location"]
            cookie = response.headers["Set-Cookie"]
            response = await session.get(
                "https://identity-myprofile.bosch.com" + location,
                headers={"Set-Cookie": cookie},
                allow_redirects=False,
            )
            location = response.headers["Location"]
            log.debug(location)
            log.debug(response.status)

            cookie = response.headers["Set-Cookie"]
            response = await session.get(
                location, headers={"Set-Cookie": cookie}, allow_redirects=False
            )

            location = response.headers["Location"]
            log.debug(location)
            log.debug(response.status)

            response = await session.get(
                "https://identity.bosch.com/" + location,
                headers={"Set-Cookie": cookie},
                allow_redirects=False,
            )

            location = response.headers["Location"]
            log.debug(location)
            log.debug(response.status)

            response = await session.get(
                location, headers={"Set-Cookie": cookie}, allow_redirects=False
            )
            log.debug(response.headers)
            log.debug(response.status)

            tree = html.fromstring(await response.text())
            code = tree.xpath("//*[@name='code']")[0].get("value")
            state = tree.xpath("//*[@name='state']")[0].get("value")
            session_state = tree.xpath("//*[@name='session_state']")[0].get("value")

            response = await session.post(
                BASE_URL + "signin-oidc",
                data={"code": code, "state": state, "session_state": session_state},
                allow_redirects=False,
            )
            location = response.headers["Location"]
            log.debug(location)
            log.debug(response.headers)
            log.debug(response.status)

            response = await session.get(
                BASE_URL + location,
                headers={"Set-Cookie": cookie},
                allow_redirects=False,
            )
            log.debug(response.headers)
            location = response.headers["Location"]
            log.debug(response.status)

            query = parse.urlparse(location).query
            redirect_params = parse.parse_qs(query)
            log.debug(redirect_params)
            code = redirect_params["code"][0]
            session_state = redirect_params["session_state"][0]
            scope = redirect_params["scope"][0]
            log.debug(code)

            data = {
                "grant_type": "authorization_code",
                "code": code,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": "com.bosch.tt.dashtt.pointt:/",
                "code_verifier": code_verifier,
                "session_state": session_state,
                "scope": scope,
            }

            response = await session.post(
                ACCESS_TOKEN_URL,
                data=data,
            )
            log.debug(response.headers)
            token = await response.json()
            assert response.status == 200
            self.refresh_token = token["refresh_token"]
            self.access_token = token["access_token"]
            self.expires_in = token["expires_in"]
            self.issued_at = datetime.utcnow()

    async def refresh_access_token(self):
        o_auth_session = aiohttp.ClientSession()
        async with o_auth_session as session:
            data = {
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            }
            response = await session.post(
                ACCESS_TOKEN_URL,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=data,
            )
            token = await response.json()
            assert response.status == 200
            self.access_token = token["access_token"]
            self.refresh_token = token["refresh_token"]
            self.expires_in = token["expires_in"]
            self.issued_at = datetime.utcnow()
            await session.close()


def generate_code_challenge():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8")
    code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    return code_challenge.replace("=", ""), code_verifier


class NotAuthenticated(Exception):
    """User not authenticated."""
