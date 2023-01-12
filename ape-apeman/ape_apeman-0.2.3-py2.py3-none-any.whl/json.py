# hex or humanized json dumps

import json
from decimal import Decimal

from eth_utils import humanize_bytes, to_hex
from hexbytes import HexBytes


class JSONEncoder_hex_bytes(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        elif isinstance(o, HexBytes):
            return to_hex(bytes(o))
        elif isinstance(o, bytes):
            return to_hex(o)
        else:
            return super().default(o)


class JSONEncoder_humanize(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        elif isinstance(o, HexBytes):
            return humanize_bytes(bytes(o))
        elif isinstance(o, bytes):
            return humanize_bytes(o)
        else:
            return super().default(o)


def dumps(*args, **kwargs):
    humanize = kwargs.pop("humanize", False)
    hex_bytes = kwargs.pop("hex_bytes", False)
    if humanize:
        kwargs["cls"] = JSONEncoder_humanize
    elif hex_bytes:
        kwargs["cls"] = JSONEncoder_hex_bytes

    return json.dumps(*args, **kwargs)
