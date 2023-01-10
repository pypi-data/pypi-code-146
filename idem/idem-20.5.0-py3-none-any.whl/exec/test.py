from typing import Any
from typing import Dict

__func_alias__ = {"ctx_": "ctx"}
__contracts__ = ["returns", "soft_fail"]


def __init__(hub):
    hub.exec.test.ITEMS = {}


def ping(hub):
    """
    Immediately return success
    """
    return {"result": True, "ret": True}


async def aping(hub):
    return {"result": True, "ret": True}


def fail(hub):
    raise Exception("Expected failure")


async def afail(hub):
    raise Exception("Expected failure")


def echo(hub, value):
    """
    Return the parameter passed in without changing it at all
    """
    return value


async def aecho(hub, value):
    """
    Return the parameter passed in without changing it at all
    """
    return value


async def event(
    hub,
    body: str,
    ingress_profile: str = "default",
    tags: Dict[str, Any] = None,
):
    """
    :param body: The event body
    :param ingress_profile: The ingress profile to allowlist for this event

    .. code-block:: bash

        $ idem exec test.event body ingress_profile="default" --serialize-plugin="json"
        $ idem exec test.event body="my_event" ingress_profile="default" --serialize-plugin="json"
    """
    event_kwargs = dict(body=body, profile=ingress_profile, tags=tags)
    await hub.idem.event.put(**event_kwargs)
    return {"result": True, "ret": event_kwargs}


async def reconcile_with_rerun_data(hub, ctx):
    """
    In order to trigger reconciliation for exec.run the result should be False.
    Also 'rerun_data' passed through the context will be concatenated.
    """
    return {
        "result": False,
        "rerun_data": ctx.get("rerun_data") + "1-" if ctx.get("rerun_data") else "-1-",
        "comment": "test",
        "ret": {"hello": "world"},
    }
