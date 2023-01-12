import os
from typing import Any
from typing import Dict

from kubernetes import client as k8s_client
from kubernetes.config import kube_config

ITERATION_FINISHED = object()

__func_alias__ = {"exec_": "exec"}


class K8sConfigurationError(Exception):
    def __init__(self, message="kube_config_path need to be set"):
        self.message = message
        super().__init__(self.message)


def load_kube_config(hub, ctx):
    config_file_path = os.environ.get("KUBE_CONFIG_PATH")
    context = os.environ.get("KUBE_CTX")

    k8s_profile = (hub.OPT.get("idem") or {}).get("acct_profile")

    if not config_file_path:
        config_file_path = (
            (((hub.OPT.get("acct") or {}).get("extras") or {}).get("k8s") or {}).get(
                k8s_profile
            )
            or {}
        ).get("kube_config_path")

    if not context:
        context = (
            (((hub.OPT.get("acct") or {}).get("extras") or {}).get("k8s") or {}).get(
                k8s_profile
            )
            or {}
        ).get("context")

    if not config_file_path:
        config_file_path = ctx.acct.get("kube_config_path")

    if not context:
        context = ctx.acct.get("context")

    if not config_file_path:
        raise K8sConfigurationError

    # If context is None, current_context from config file will be used.
    kube_config.load_kube_config(config_file=config_file_path, context=context)


async def exec_(
    hub,
    ctx,
    api_class: str,
    operation: str,
    *op_args,
    **op_kwargs: Dict[str, Any],
) -> Any:
    """
    :param hub:
    :param ctx:
    :param api_class: kubernetes API class name
    :param operation: The operation to run from the service client
    :param op_args: arguments to pass to the operation call
    :param op_kwargs: keyword arguments to pass to the operation call

    :return: The result of the operation call
    """
    hub.tool.k8s.client.load_kube_config(ctx)
    # Don't pass kwargs that have a "None" value to the function call
    kwargs = {k: v for k, v in op_kwargs.items() if v is not None}
    api_instance = getattr(k8s_client, api_class)()
    hub.log.debug(f"Getting raw results for {api_instance}.{operation}")
    op = getattr(api_instance, operation)
    return await hub.pop.loop.wrap(op, *op_args, **kwargs)
