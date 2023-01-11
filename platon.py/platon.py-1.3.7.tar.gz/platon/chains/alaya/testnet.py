from platon import Web3
from platon.providers.auto import (
    load_provider_from_uri,
)

from .endpoints import (
    ALAYA_TESTNET_DOMAIN,
    build_http_headers,
    build_chain_url,
)

_headers = build_http_headers()
_chain_url = build_chain_url(ALAYA_TESTNET_DOMAIN)

w3 = Web3(load_provider_from_uri(_chain_url, _headers))
