import json
import requests
import eloquasdk.utils as utils

from enum import Enum
from collections import OrderedDict

LOGIN_URL = 'https://login.eloqua.com'
ID_ENDPOINT = LOGIN_URL + '/id'
TOKEN_ENDPOINT = LOGIN_URL + '/auth/oauth2/token'


class AuthType(Enum):
    BASIC = 'Basic',
    OAUTH2 = 'Bearer'


def EloquaLogin(siteName=None, username=None,
                password=None, client_id=None,
                client_secret=None, auth_type=AuthType.BASIC):

    if auth_type == AuthType.BASIC:
        # use basic authentication
        token = utils.b64auth(siteName + '\\' + username, password)
        return token
    elif auth_type == 'oauth2':
        result = _get_token(siteName, username, password,
                            client_id, client_secret)

        return result.json(object_pairs_hook=OrderedDict)


def _get_token(siteName, username, password,
               client_id, client_secret):
    auth = utils.b64auth(client_id, client_secret)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic {auth}'.format(
            auth=auth.decode())
    }

    data = {
        'grant_type': 'password',
        'scope': 'full',
        'username': '{siteName}\\{username}'
                    .format(siteName=siteName,
                            username=username),
        'password': password
    }

    response = _send_request(
        'POST', TOKEN_ENDPOINT,
        headers=headers, data=json.dumps(data)
    )

    return response


def _refresh_token():
    print('resfresh token')


def _send_request(method, url, **kwargs):

    result = requests.request(
        method, url, **kwargs)

    # TODO: handle excpetions
    return result
