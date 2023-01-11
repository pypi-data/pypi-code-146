import os
from typing import (
    Dict,
    Optional,
    Tuple,
)

from platon_typing import (
    URI,
)
from platon_utils import (
    ValidationError,
)

from platon.exceptions import (
    AlayaKeyNotFound,
)

ALAYA_MAINNET_DOMAIN = 'openapi.alaya.network'
ALAYA_TESTNET_DOMAIN = 'devnetopenapi.alaya.network'

WEBSOCKET_SCHEME = 'wss'
HTTP_SCHEME = 'https'


# def load_api_key() -> str:
#     # in web3py v6 remove outdated WEB3_ALAYA_API_KEY
#     key = os.environ.get('WEB3_ALAYA_PROJECT_ID',
#                          os.environ.get('WEB3_ALAYA_API_KEY', ''))
#     if key == '':
#         raise AlayaKeyNotFound(
#             "No Alaya Project ID found. Please ensure "
#             "that the environment variable WEB3_ALAYA_PROJECT_ID is set."
#         )
#     return key


def load_secret() -> str:
    # return os.environ.get('WEB3_ALAYA_API_SECRET', '')
    return ''


def build_http_headers() -> Optional[Dict[str, Tuple[str, str]]]:
    # secret = load_secret()
    # if secret:
    #     headers = {'auth': ('', secret)}
    #     return headers
    return None


def build_chain_url(domain: str) -> URI:
    scheme = os.environ.get('WEB3_ALAYA_SCHEME', WEBSOCKET_SCHEME)
    # key = load_api_key()
    secret = load_secret()
    if scheme == WEBSOCKET_SCHEME and secret == '':
        return URI("%s://%s/ws" % (scheme, domain))
    # elif scheme == WEBSOCKET_SCHEME and secret != '':
    #     return URI("%s://:%s@%s/ws/v3/%s" % (scheme, secret, domain, key))
    elif scheme == HTTP_SCHEME:
        return URI("%s://%s" % (scheme, domain))
    else:
        raise ValidationError("Cannot connect to Alaya with scheme %r" % scheme)
