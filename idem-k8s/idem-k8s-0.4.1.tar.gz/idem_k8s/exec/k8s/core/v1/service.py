"""Exec module for managing Kubernetes CoreV1 Service(s)."""
from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    namespace: str = None,
) -> Dict[str, Any]:
    """Retrieves a Kubernetes CoreV1 Service.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            The service.metadata.name of the Kubernetes CoreV1 Service.

        namespace(str, Optional):
            The Kubernetes namespace in which CoreV1 Service was created. Defaults to 'default' namespace in case None.

    Returns:
        Dict[str, Any]:
            Return a CoreV1 Service in a given namespace.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec k8s.core.v1.service.get name='service-name' resource_id='v1service' namespace='default'

        Calling this exec module function from within a state:

        .. code-block:: yaml

            my-kubernetes-service:
              exec.run:
                - path: k8s.core.v1.service.get
                - kwargs:
                    name: 'service-name'
                    resource_id: 'v1service'
                    namespace: 'default'
    """
    result = dict(comment=[], ret=None, result=True)

    describe_ret = await hub.exec.k8s.client.CoreV1Api.read_namespaced_service(
        ctx, name=resource_id, namespace=namespace if namespace else "default"
    )
    if not describe_ret["result"]:
        # Do not return success=false when it is not found.
        if "ApiException" in str(describe_ret["comment"]) or "Reason: Not Found" in str(
            describe_ret["comment"]
        ):
            result["comment"].append(
                hub.tool.k8s.comment_utils.get_empty_comment(
                    resource_type="k8s.core.v1.service", name=resource_id
                )
            )
            result["comment"] += list(describe_ret["comment"])
            return result

        result["comment"] += list(describe_ret["comment"])
        result["result"] = False
        return result

    if not describe_ret["ret"]:
        result["comment"].append(
            hub.tool.k8s.comment_utils.get_empty_comment(
                resource_type="k8s.core.v1.service", name=resource_id
            )
        )
        return result

    result["ret"] = hub.tool.k8s.core.v1.service_utils.convert_raw_service_to_present(
        service=describe_ret.get("ret"),
    )
    return result
