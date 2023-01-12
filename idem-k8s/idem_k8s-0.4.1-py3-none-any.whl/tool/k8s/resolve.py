from typing import Any
from typing import Dict

import pop.contract


def client(hub, path: str, context):
    """
    Get an AWS service client based on the path and call an operation on it
    idem will automatically populate credentials from acct in the client.

    The calls mirror the namespacing of boto3.client and have the same parameters

    If a response can be paginated, the full result will be asynchronously collected and returned.

    path::

        boto3.client.[service_name].[operation] [kwargs="values"]

    Examples:
        In these examples will use the service_name of "ec2" and operation of "create_vpc"

        Call from the CLI
        .. code-block: bash

            $ idem exec boto3.client.ec2.create_vpc CidrBlock="10.0.0.0/24"

        Call from code
        .. code-block: python

            await hub.exec.boto3.client.ec2.create_vpc(ctx, CidrBlock="10.0.0.0/24")

    :param hub:
    :param path: client.[service_name].[function_name]
    :param context: None
    :return: The result of the call
    """
    c, api_class, operation = path.split(".", maxsplit=2)
    assert c == "client"

    async def _client_caller(ctx, *args, **kwargs) -> Dict[str, Any]:
        result = {"comment": (), "ret": None, "result": True}
        try:
            ret: Dict[str, Any] = await hub.tool.k8s.client.exec(
                ctx, api_class, operation, *args, **kwargs
            )
            if hasattr(ret, "keys"):
                keys = sorted(ret.keys())
            else:
                keys = []
            result["comment"] = tuple(keys)
            result["ret"] = ret
            result["result"] = bool(ret)
        except Exception as e:
            result["result"] = False
            result["comment"] = (f"{e.__class__.__name__}: {e}",)
        return result

    return pop.contract.ContractedAsync(
        hub,
        contracts=[],
        func=_client_caller,
        ref=path,
        name=operation,
        implicit_hub=False,
    )
