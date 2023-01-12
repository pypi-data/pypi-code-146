import asyncio
import logging
from typing import Dict

import jmespath

logger = logging.getLogger(__name__)


async def wait(
    hub,
    ctx,
    waiter,
    waiter_config,
    initial_delay: int = None,
    err_graceful: bool = False,
):

    if not waiter or not waiter_config:
        raise NameError("Waiter or waiter config undefined")

    if initial_delay:
        await asyncio.sleep(initial_delay)

    method_handle = getattr(
        hub.exec.k8s.client, ".".join([waiter.api_class_name, waiter.operation])
    )
    delay = waiter_config.get("delay")
    max_attempts = waiter_config.get("max_attempts")
    retry = True
    while retry and max_attempts:
        ret = await method_handle(ctx, **waiter.arguments)
        if not ret["result"] and not err_graceful:
            raise RuntimeError(ret["comment"])

        status = ret["result"]
        comment = ret["comment"]
        data = ret["ret"].to_dict() if ret["result"] else {}

        if waiter.result_arguments:
            result = {
                key: extract(data, path)
                for key, path in waiter.result_arguments.items()
            }
        else:
            result = data

        retry = not bool(
            waiter.acceptor_function(status=status, data=result, comment=comment)
        )

        if retry:
            max_attempts -= 1
            await asyncio.sleep(delay)

    if not max_attempts:
        raise TimeoutError("Wait timed out.")


def extract(data: Dict, expr: str):
    return jmespath.search(expr, data)
