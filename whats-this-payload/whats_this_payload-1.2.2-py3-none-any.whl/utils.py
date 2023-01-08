"""Utility goodies."""

from whats_this_payload.base import BaseHandler


def build_handler_chain(handlers: list[BaseHandler]) -> BaseHandler:
    """Build a chain of handlers from list."""
    root_handler = handlers[0]
    last_handler: None | BaseHandler = None
    for handler in handlers[1:]:
        if not last_handler:
            last_handler = root_handler.set_next_handler(handler=handler)
        else:
            last_handler = last_handler.set_next_handler(handler=handler)

    return root_handler
