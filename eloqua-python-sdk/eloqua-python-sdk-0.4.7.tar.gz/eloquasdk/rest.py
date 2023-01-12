import requests
import logging

from requests.auth import HTTPBasicAuth
from enum import Enum

from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
from requests.exceptions import RequestException

from .error import EloquaException

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

LOGIN_ENDPOINT = 'https://login.eloqua.com'
ID_ENDPOINT = LOGIN_ENDPOINT + '/id'
DEFAULT_API_VERSION = '2.0'

LOGIN_URL = 'https://login.eloqua.com'
API_VERSION = '2.0'
TOKEN_URL = LOGIN_URL + '/auth/oauth2/token'

logger = logging.getLogger('eloqua.client')


class AuthType(Enum):
    BASIC = 1,
    OAUTH2 = 2


class EloquaRestClient(object):

    def __init__(
        self,
        username,
        password,
        rest_url,
        client_id=None,
        client_secret=None,
        debug=False
    ):
        self.rest_url = rest_url
        self.debug = debug

        basic_auth_args = (username, password)
        oauth_args = (username, password, client_id, client_secret)
        # Determine if the user wants to use OAuth 2.0 for added security
        # Eloqua supports Resource Owner Password Credentials Grant
        if all(arg is not None for arg in oauth_args):
            self.oauth = OAuth2Session(
                client=LegacyApplicationClient(client_id=client_id),
                auto_refresh_url=TOKEN_URL,
                token_updater=self.token_updater)

            self.token = self.oauth.fetch_token(
                token_url=TOKEN_URL,
                username=username,
                password=password,
                client_id=client_id,
                client_secret=client_secret)

            self.auth_type = AuthType.OAUTH2

        elif all(arg is not None for arg in basic_auth_args):
            self.auth = HTTPBasicAuth(*basic_auth_args)
            self.auth_type = AuthType.BASIC

        else:
            raise TypeError(
                'You must provide login information.'
            )

        self.valid_until = None
        self.base_url = None

    def make_request(self, **kwargs):
        if self.debug:
            logger.info(u'{method} Request: {url}'.format(**kwargs))
            if kwargs.get('json'):
                logger.info('payload: {json}'.format(**kwargs))

        if self.auth_type == AuthType.OAUTH2:
            resp = self.oauth.request(**kwargs)
        else:
            resp = requests.request(auth=self.auth, **kwargs)

        if self.debug:
            logger.info(u'{method} response: {status}'.format(
                method=kwargs['method'],
                status=resp.status_code))

        return resp

    def get_assets(
        self,
        asset_type,
        depth='minimal',
        count=1000,
        page=0,
        order_by='',
        search=''
    ):
        assets_url = (
            'email/groups' if asset_type == 'EmailGroups'
            else asset_type
        )

        url = self.rest_url + '/assets/' + assets_url
        return self.get(
            url,
            depth=depth,
            count=count,
            page=page,
            orderBy=order_by,
            search=search)

    def get(self, url, headers=None, **queryparams):
        if not headers:
            headers = {
                'Accept': 'application/json'
            }
        elif 'Accept' not in headers.keys():
            headers['Accept'] = 'application/json'

        if len(queryparams):
            url += '?' + urlencode(queryparams)

        try:
            r = self.make_request(**dict(
                method='GET',
                url=url,
                headers=headers
            ))
        except RequestException as e:
            raise e
        else:
            if r.status_code >= 400:
                raise EloquaException(r.reason, r.text)
            return r.json()
