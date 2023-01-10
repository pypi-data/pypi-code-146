from typing import Dict

from bittrade_kraken_rest.connection import send_private


def raw(*, url: str = "", options: Dict = None):
    return send_private(url=url, data=options or {})
