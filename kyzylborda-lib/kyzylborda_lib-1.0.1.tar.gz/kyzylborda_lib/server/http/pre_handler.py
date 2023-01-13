from __future__ import annotations

from .request import Request, SUPPORTED_METHODS
from .response import Response, respond
from ...sandbox import stop_box


__all__ = ("pre_handler",)


async def pre_handler(request: Request) -> Response | None:
    if not any(request.raw_header.startswith(f"{method} /__internal__/".encode()) for method in SUPPORTED_METHODS):
        return None

    prefix = "/__internal__/reboot_container/"
    if request.path.startswith(prefix):
        if request.method != "POST":
            return respond(405)
        suffix = request.path[len(prefix):]
        token, _, redirect_to = suffix.partition("?")
        await stop_box(token)
        return respond(303, b"Restarted", headers={
            "Location": redirect_to
        })

    return respond(404)
