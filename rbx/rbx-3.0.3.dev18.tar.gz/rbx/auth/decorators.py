from functools import wraps
from typing import NamedTuple

from flask import abort, current_app, request

from . import fake_key, Keystore


class Grants(NamedTuple):
    key: str
    campaigns: list = []
    is_restricted: bool = False


def protect(with_grants=False):
    """Protect an endpoint via API Keys.

    If with_grants is True, the Grants object is added to the caller as a 'grants' keyword
    argument.

    When DEV_MODE is enabled, all restrictions are lifted.

    Keys are retrieved from the Keystore, and cached using the LRU local caching.
    They are provided via the "X-RBX-TOKEN" header, and can also be provided via the 'key'
    query string parameter.

    If the request originates from App Engine's Cron Service, or from Cloud Tasks, it is always
    granted access.

    From the documentation:

        The X-Appengine-Cron header is set internally by Google App Engine.
        If your request handler finds this header it can trust that the request is a cron request.
        The X- headers are stripped by App Engine when they originate from external sources so that
        you can trust this header.

    """

    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if any(
                [
                    "X-Appengine-Cron" in request.headers,
                    "X-AppEngine-TaskName" in request.headers,
                ]
            ):
                return func(*args, **kwargs)

            key_id = request.headers.get("X-RBX-TOKEN") or request.args.get("key")
            if key_id is None:
                abort(401)

            if current_app.config.get("DEV_MODE", False):
                key = fake_key(
                    key_id=key_id,
                    name="DEV Mode",
                    email="dev-mode@localhost.com",
                    is_restricted=False,
                )
            else:
                key = get_key(key_id=key_id)

            if not key or not key.has_access(
                service=current_app.name.replace("_", "-"),
                operation=func.__name__.replace("_", "-"),
            ):
                abort(401)

            if with_grants:
                kwargs["grants"] = Grants(
                    key=key_id, campaigns=key.campaigns, is_restricted=key.is_restricted
                )

            return func(*args, **kwargs)

        return wrapped

    return decorator


def get_key(key_id):
    return Keystore().get_key(key_id=key_id)
