"""Obtain an OCP OAuth token for an SSO IdP with Kerberos support."""

import functools
import html
import re
import typing
from urllib import parse

import requests
import requests_gssapi


class OcpOAuthLogin:
    """Obtain an OCP OAuth token for an SSO IdP with Kerberos support."""

    def __init__(self, api_url: str):
        """Create an instance for a certain cluster represented by its API URL."""
        self.session = requests.Session()
        self.auth = requests_gssapi.HTTPSPNEGOAuth(mutual_authentication=requests_gssapi.OPTIONAL)
        self.meta_url = parse.urljoin(api_url, '/.well-known/oauth-authorization-server')

    @functools.cached_property
    def _token_endpoint(self) -> str:
        """Return the URL of the OAuth token endpoint."""
        response = self.session.get(self.meta_url)
        response.raise_for_status()
        return str(response.json()['token_endpoint'])

    @functools.cached_property
    def identity_providers(self) -> typing.Dict[str, str]:
        """Return a dictionary of all identity providers and their URLs."""
        # https://github.com/openshift/library-go/blob/master/pkg/oauth/oauthdiscovery/urls.go
        response = self.session.get(self._token_endpoint + '/request')
        response.raise_for_status()
        # https://github.com/openshift/oauth-server/blob/master/pkg/server/selectprovider/templates.go
        return {
            parse.unquote(name): parse.urljoin(self._token_endpoint, url)
            for url, name
            in re.findall(r'href="([^"]*\bidp=([^="&]+\b)[^"]*)"', html.unescape(response.text))
        }

    def token(self, identity_provider: str) -> str:
        """Authenticate with the given identity provider and return an access token."""
        response = self.session.get(self.identity_providers[identity_provider], auth=self.auth)
        response.raise_for_status()
        # https://github.com/openshift/oauth-server/blob/master/pkg/server/tokenrequest/tokenrequest.go
        data = dict(re.findall('name="([^"]*)" value="([^"]*)"', html.unescape(response.text)))
        response = self.session.post(response.url, data=data)
        response.raise_for_status()
        # https://github.com/openshift/oauth-server/blob/master/pkg/server/tokenrequest/tokenrequest.go
        if not (match := re.search('<code>(.*)</code>', html.unescape(response.text))):
            raise Exception(f'Unable to find access token in response: {response.text}')
        return match[1]
