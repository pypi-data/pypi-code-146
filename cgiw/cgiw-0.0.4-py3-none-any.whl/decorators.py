from typing import Any, Callable

from .schemas import PostHandlerType, BodyParserType, QueryType, HeadersType, ReturnType


def body_parser(parser: BodyParserType) -> Callable[[PostHandlerType], PostHandlerType]:
    def wrap(post_handler: PostHandlerType) -> PostHandlerType:
        def wrapper(query: QueryType, headers: HeadersType, body: Any) -> ReturnType:
            return post_handler(query, headers, parser(body))
        return wrapper
    return wrap
