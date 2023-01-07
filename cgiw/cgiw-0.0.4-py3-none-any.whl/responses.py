from json import dumps
from typing import Optional, Union, Tuple, Dict

from .schemas import JsonType, ReturnType


def json(obj: JsonType) -> ReturnType:
    return ('200 OK', {'Content-Type': 'application/json'}, dumps(obj))

def redirect(url: str) -> ReturnType:
    headers = {
        'Content-Type': 'text/plain',
        'Location': url
    }
    return ('301 Moved Permanently', headers, f'Redirecting to {url}...')