import base64
import hmac
import hashlib
import time
from urllib.parse import quote_plus


def get_query_sign(params: dict):
    keys = list(params.keys())
    keys.sort()

    sign = ''
    for k in keys:
        val = params[k]
        if val is not None:
            if isinstance(val, bytes):
                val = val.decode('utf-8')
            else:
                val = str(val)
            sign += f'{k}={quote_plus(val)}&'
    return sign[:-1]


def get_signature(method, params, body, key, secret, timestamp):
    query_sign = get_query_sign(params)
    body_sign = get_query_sign(body)
    sign_str = f'{method.upper()}\n{key}\n{query_sign}\n{body_sign}\n{timestamp}'
    h = hmac.new(
        secret.encode('utf-8'),
        sign_str.encode('utf-8'),
        hashlib.sha1
    )
    return base64.b64encode(h.digest()).decode('utf-8')


def sign_headers(method, params, body, key, secret, timestamp=None):
    timestamp = timestamp or int(time.time() * 1000)
    signature = get_signature(method, params, body, key, secret, timestamp)
    return {
        'accesskeyid': key,
        'signature': signature,
        'timestamp': str(timestamp)
    }
