"""Exec module for managing Kubernetes APIService."""
from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Retrieves a Kubernetes APIService.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str):
            The metadata.name of the Kubernetes APIService.

    Returns:
        Dict[str, Any]:
            Return a Kubernetes APIService.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec k8s.apiregistration_k8s_io.v1.api_service.get name='api-service-name' resource_id='api-service-1'

        Using in a state:

        .. code-block:: yaml

            my-kubernetes-api_service:
              exec.run:
                - path: k8s.apiregistration_k8s_io.v1.api_service.get
                - kwargs:
                    name: 'api-service-name'
                    resource_id: 'api-service-1'

    """
    result = dict(comment=[], ret=None, result=True)

    api_service = await hub.exec.k8s.client.ApiregistrationV1Api.read_api_service(
        ctx, name=resource_id
    )

    if not api_service["result"]:
        # Do not return success=false when it is not found.
        if "ApiException" in str(api_service["comment"]) or "Reason: Not Found" in str(
            api_service["comment"]
        ):
            result["comment"].append(
                hub.tool.k8s.comment_utils.get_empty_comment(
                    resource_type="k8s.apiregistration_k8s_io.v1.api_service",
                    name=resource_id,
                )
            )
            result["comment"] += list(api_service["comment"])
            return result

        result["comment"] += list(api_service["comment"])
        result["result"] = False
        return result

    if not api_service["ret"]:
        result["comment"].append(
            hub.tool.k8s.comment_utils.get_empty_comment(
                resource_type="k8s.apiregistration_k8s_io.v1.api_service",
                name=resource_id,
            )
        )
        return result

    result[
        "ret"
    ] = hub.tool.k8s.apiregistration_k8s_io.v1.api_service_utils.convert_raw_api_service_to_present(
        api_service=api_service.get("ret"),
    )
    return result


async def list_(hub, ctx, name) -> Dict:
    """Retrieves list of Kubernetes ApiServices.

    Args:
        name(str, Optional): The name of the Idem state.

    Returns:
        Dict[bool, list, dict or None]:

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec k8s.apiregistration_k8s_io.v1.api_service.list name="idem_name"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: k8s.apiregistration_k8s_io.v1.api_service.list
                - kwargs:
                    name: my_resource

    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.exec.k8s.client.ApiregistrationV1Api.list_api_service(ctx)

    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]:
        result["comment"].append(
            hub.tool.k8s.comment_utils.list_empty_comment(
                resource_type="k8s.apiregistration_k8s_io.v1.api_service", name=name
            )
        )
        return result
    for api_service in ret["ret"].items:
        converted_resource = hub.tool.k8s.apiregistration_k8s_io.v1.api_service_utils.convert_raw_api_service_to_present(
            api_service=api_service
        )
        result["ret"].append(converted_resource)
    return result
