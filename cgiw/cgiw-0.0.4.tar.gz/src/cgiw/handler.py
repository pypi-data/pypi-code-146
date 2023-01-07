from typing import Optional, Any

from .schemas import QueryType, HeadersType, GetHandlerType, PostHandlerType, ReturnType


def handle(method: str, query: QueryType, headers: HeadersType, body: Optional[Any] = None, get: Optional[GetHandlerType] = None, post: Optional[PostHandlerType] = None) -> ReturnType:
    if method == 'POST' and post:
        return post(query, headers, body)
    elif method == 'GET' and get:
        return get(query, headers)
    return ('405 Method Not Allowed', {}, '')