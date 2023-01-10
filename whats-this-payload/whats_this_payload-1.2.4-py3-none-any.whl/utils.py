"""Utility goodies."""

from typing import Union

from whats_this_payload.base import BaseHandler


def build_handler_chain(handlers: list[BaseHandler]) -> BaseHandler:
    """Build a chain of handlers from list."""
    root_handler = handlers[0]
    last_handler: Union[None, BaseHandler] = None
    for handler in handlers[1:]:
        last_handler = (
            root_handler.set_next_handler(handler=handler)
            if not last_handler
            else last_handler.set_next_handler(handler=handler)
        )

    return root_handler
