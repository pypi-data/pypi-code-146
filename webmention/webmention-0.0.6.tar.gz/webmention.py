"""

"""

import requests


class EndpointNotFound(Exception):
    """Webmention endpoint could not be found."""


def send(source, target) -> dict:
    """
    Send a mention of `target` from `source`.

    """
    # TODO re-queue failures w/ a logarithmic backoff
    target = webcli.uri(target)
    endpoint = webcli.get(target).discover_link("webmention")
    if not endpoint:
        raise EndpointNotFound(target)
    return webcli.post(data={"source": source, "target": target}).json


def receive(source, target):
    """
    Receive a mention of `target` from source.

    """
