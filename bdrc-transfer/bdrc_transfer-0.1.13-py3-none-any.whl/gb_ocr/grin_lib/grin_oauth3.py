#!/usr/bin/env python3
# python3: Use env to locate python.

r"""GRIN/OAUTH2 python example.
Reduced from https://drive.google.com/file/d/1CJhAikrRdHB8eWrTd-NmEW900xPxg2rT/view?usp=sharing
"""

import urllib.request
import urllib.error

import httplib2
from oauth2client.file import Storage

# How much we read/write when streaming response data.
OUTPUT_BLOCKSIZE = 1024 * 1024


class CredsMissingError(IOError):
    """Raised by CredentialsFactory() when credentials are missing."""

    def __init__(self):
        super().__init__()


class GRINPermissionDeniedError(IOError):
    """GRIN says you're not allowed."""


class GoogleLoginError(IOError):
    """Something failed logging in to Google."""


def CredentialsFactory(credentials_file):
    """Use the oauth2 libraries to load our credentials."""
    storage = Storage(credentials_file)
    creds = storage.get()
    if creds is None:
        raise CredsMissingError()

    # If our credentials are expired, use the 'refresh_token' to generate a new
    # one.
    if creds.access_token_expired:
        creds.refresh(httplib2.Http())
    return creds


def MakeGrinRequest(creds, url):
    """Makes an HTTP request to grin using urllib2, and returns the response."""
    # python 3
    # request = urllib2.request.Request(url)
    request = urllib.request.Request(url)
    request.add_header('Authorization', 'Bearer %s' % creds.access_token)

    try:
        # python 3
        # response = urllib2.urlopen(request)
        response = urllib.request.urlopen(request)

    # python3: exception syntax
    # Try to give better diagnostics on a 403, which means we are logged in OK but
    # GRIN denied the request.
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            raise GRINPermissionDeniedError((
                'GRIN denied this request (403). You may not have permission to '
                'access this directory, or we may not have applied your ACL to '
                'production, yet. This can take up to 12 hours.'))
        raise exc

    # See if we were redirected to the account login page. This means something
    # about our token was not accepted. Our project may not be setup correctly.
    if 'accounts.google.com/ServiceLogin' in response.geturl():
        raise GoogleLoginError((
            'Something went wrong logging in to Google. Your credentials file '
            'may be invalid.'))
    return response
