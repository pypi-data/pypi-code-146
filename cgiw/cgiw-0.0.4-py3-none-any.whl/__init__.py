from os import getenv
from typing import Optional

from .schemas import GetHandlerType, PostHandlerType
from .parsers import parse_query, parse_headers, parse_body
from .handler import handle
from .composers import compose_response


def run(get: Optional[GetHandlerType] = None, post: Optional[PostHandlerType] = None, verbose=True):
    method = getenv('REQUEST_METHOD', '')
    query = parse_query()
    headers = parse_headers()
    body = parse_body(headers)
    response = handle(method, query, headers, body, get=get, post=post)
    result = compose_response(*response)
    if verbose:
        print(result)
    return result