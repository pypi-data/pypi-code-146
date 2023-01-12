"""Exec module for managing Kubernetes PersistentVolumeClaim(s)."""
from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    namespace: str = "default",
) -> Dict[str, Any]:
    """Retrieves a Kubernetes CoreV1 PersistentVolumeClaim.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str):
            The metadata.name of the Kubernetes CoreV1 PersistentVolumeClaim.

        namespace(str, Optional):
            The Kubernetes namespace in which CoreV1 PersistentVolumeClaim was created.
            Defaults to 'default' namespace in case None.

    Returns:
        Dict[str, Any]:
            Return a CoreV1 PersistentVolumeClaim in a given namespace.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec k8s.core.v1.persistent_volume_claim.get name='pvc-name' resource_id='pvc-12' namespace='default'

        Using in a state:

        .. code-block:: yaml

            my-kubernetes-pvc:
              exec.run:
                - path: k8s.core.v1.persistent_volume_claim.get
                - kwargs:
                    name: 'pvc-name'
                    resource_id: 'pvc-12'
                    namespace: 'default'
    """
    result = dict(comment=[], ret=None, result=True)

    persistent_volume_claim = (
        await hub.exec.k8s.client.CoreV1Api.read_namespaced_persistent_volume_claim(
            ctx, name=resource_id, namespace=namespace
        )
    )

    if not persistent_volume_claim["result"]:
        # Do not return success=false when it is not found.
        if "ApiException" in str(
            persistent_volume_claim["comment"]
        ) or "Reason: Not Found" in str(persistent_volume_claim["comment"]):
            result["comment"].append(
                hub.tool.k8s.comment_utils.get_empty_comment(
                    resource_type="k8s.core.v1.persistent_volume_claim",
                    name=resource_id,
                )
            )
            result["comment"] += list(persistent_volume_claim["comment"])
            return result

        result["comment"] += list(persistent_volume_claim["comment"])
        result["result"] = False
        return result

    if not persistent_volume_claim["ret"]:
        result["comment"].append(
            hub.tool.k8s.comment_utils.get_empty_comment(
                resource_type="k8s.core.v1.persistent_volume_claim", name=resource_id
            )
        )
        return result

    result[
        "ret"
    ] = hub.tool.k8s.core.v1.persistent_volume_claim_utils.convert_raw_persistent_volume_claim_to_present(
        persistent_volume_claim=persistent_volume_claim.get("ret"),
    )
    return result


async def list_(hub, ctx, name) -> Dict:
    """Retrieves list of Kubernetes CoreV1 PersistentVolumeClaims.

    Args:
        name(str, Optional): The name of the Idem state.

    Returns:
        Dict[bool, list, dict or None]:

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec k8s.core.v1.persistent_volume_claim.list name="idem_name"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: k8s.core.v1.persistent_volume_claim.list
                - kwargs:
                    name: my_resource

    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.exec.k8s.client.CoreV1Api.list_persistent_volume_claim_for_all_namespaces(
        ctx
    )

    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]:
        result["comment"].append(
            hub.tool.k8s.comment_utils.list_empty_comment(
                resource_type="k8s.core.v1.persistent_volume_claim", name=name
            )
        )
        return result
    for persistent_volume_claim in ret["ret"].items:
        converted_resource = hub.tool.k8s.core.v1.persistent_volume_claim_utils.convert_raw_persistent_volume_claim_to_present(
            persistent_volume_claim=persistent_volume_claim
        )
        result["ret"].append(converted_resource)
    return result
