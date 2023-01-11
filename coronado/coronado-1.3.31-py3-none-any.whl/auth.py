# vim: set fileencoding=utf-8:


from datetime import datetime

from jose import jwt
from jose.exceptions import ExpiredSignatureError
from jose.exceptions import JWTClaimsError
from jose.exceptions import JWTError

from coronado.exceptions import AuthTokenAPIError

import json
import logging

import requests

from coronado import TripleEnum
from coronado import TripleObject
from coronado.tools import tripleKeysToCamelCase


# --- constants ----

EXPIRATION_OFFSET = -3900
TOKEN_URL = 'https://auth.partners.dev.tripleupdev.com/oauth2/token'


# --- globals ---

log = logging.getLogger(__name__)


# +++ classes +++

class Auth(TripleObject):

    def _getTokenPayload(self) -> str:
        payload = { 'grant_type': 'client_credentials' }

        credentials = (self._clientID, self._clientSecret)

        response = requests.request('POST', self._tokenURL, data = payload, auth = credentials)

        if response.status_code != 200:
            error = AuthTokenAPIError(': '.join([response.reason, json.loads(response.text)["error"]]))
            log.error(error)
            raise error

        return str(response.content, encoding = 'utf-8')


    def _setState(self, expirationOffset = None):
        d = json.loads(self._tokenPayload)

        deltaSeconds = expirationOffset if expirationOffset else d['expires_in']

        now = round(datetime.now().timestamp())
        self._expirationTime = round(now+deltaSeconds)
        self._token = d['access_token']
        self._tokenType = d['token_type']



    def __init__(self, tokenURL = TOKEN_URL, clientID = None, clientSecret = None, expirationOffset = None):
        """
        Instantiates a new Auth object.  It requires URLs and configuration
        parameters granted by triple for use with this API.

        Arguments
        ---------
            tokenURL : str
        The URL for the access token provider

            clientID : str
        A unique client ID, provider by triple

            clientSecret : str
        The unique client ID associated secret

        See:  <a href='https://aws.amazon.com/blogs/mobile/understanding-amazon-cognito-user-pool-oauth-2-0-grants/' target='_blank'>AWS Cognito user pool grants</a>
        for details.

            expirationOffset : int
        Expiration time buffer, seconds to subtract from expiration time to
        that the internal token representation is up-to-date; **used only for
        unit testing, users should ignore this argument**.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        self._tokenURL = tokenURL
        self._clientID = clientID
        self._clientSecret = clientSecret

        self._tokenPayload = self._getTokenPayload()

        self._setState(expirationOffset)


    @property
    def tokenPayload(self) -> str:
        """
        Returns the current access token associated with the receiver.  The
        property is guaranteed to never return an expired token.  The underlying
        implementation will request a new access token to the token provider
        API.

        Returns
        -------
        A JWT string
        """
        now = round(datetime.now().timestamp())
        delta = self._expirationTime-now
        if delta < 0:
            self._tokenPayload = self._getTokenPayload()
            self._setState()

        return self._tokenPayload


    @property
    def token(self) -> str:
        """
        Return the current access token by itself.  Auth objects have a JWT
        representation internally, which includes the actual access token in
        one of its attributes.  This property returns that access token
        sans all the rest of the JWT JSON structure.

        Returns
        -------
            A token string
        """
        self.tokenPayload  # This is for the refresh token side effect

        return self._token


    @property
    def tokenType(self) -> str:
        """
        Return the current token type by itself.  Auth objects have a JWT
        representation internally, which includes the actual access token in
        one of its attributes.  This property returns that token type
        attribute sans all the rest of the JWT JSON structure.

        Returns
        -------
            A token type string
        """
        self.tokenPayload  # This is for the refresh token side effect

        return self._tokenType


    @property
    def info(self) -> dict:
        """
        Return the receiver's reserved OAuth2 claims set.

        Reference:  https://www.oauth.com/oauth2-servers/openid-connect/id-tokens/

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        self.tokenPayload

        try:
            claimSet = jwt.decode(self.token, '', options = {'verify_signature': False})
        except JWTError as e:
            error = AuthTokenAPIError(str(e))
            log.error(error)
            raise error
        except ExpiredSignatureError as e:
            error = AuthTokenAPIError(str(e))
            log.error(error)
            raise error
        except JWTClaimsError as e:
            error = AuthTokenAPIError(str(e))
            log.error(error)
            raise error

        return tripleKeysToCamelCase(claimSet)


