from os import getenv

from .schemas import GetHandlerType, PostHandlerType
from .parsers import parse_query, parse_headers, parse_body
from .handler import handle
from .composers import compose_response


def run(get: GetHandlerType, post: PostHandlerType):
    method = getenv('REQUEST_METHOD', '')
    query = parse_query()
    headers = parse_headers()
    body = parse_body(headers)
    response = handle(method, query, headers, body)
    return compose_response(*response)