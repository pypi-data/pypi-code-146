"""State module for managing Kubernetes PersistentVolumeClaim(s)."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

from dict_tools import differ

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    metadata: make_dataclass(
        "metadata",
        [
            ("name", str),
            ("namespace", str, field(default=None)),
            ("labels", Dict, field(default=None)),
            ("annotations", str, field(default=None)),
        ],
    ),
    spec: make_dataclass(
        "spec",
        [
            ("access_modes", List[str], field(default=None)),
            ("volume_mode", str, field(default=None)),
            ("storage_class_name", str, field(default=None)),
            (
                "resources",
                make_dataclass(
                    "resources",
                    [
                        (
                            "request",
                            make_dataclass(
                                "request",
                                [("storage", str, field(default=None))],
                            ),
                            field(default=None),
                        )
                    ],
                ),
                field(default=None),
            ),
            (
                "selector",
                make_dataclass(
                    "selector",
                    [
                        ("match_labels", Dict, field(default=None)),
                        ("match_expressions", List[Dict], field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ),
    resource_id: str = None,
) -> Dict[str, Any]:
    """Creates a PersistentVolumeClaim.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        metadata(dict):
            Standard object's metadata.
            More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.

        spec(dict):
            Spec defines the desired characteristics of a volume requested by a pod author.
            More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims.

    Request Syntax:

        .. code-block:: sls

            [pvc-name]:
              k8s.core.v1.persistent_volume_claim.present:
                - name: 'string'
                - metadata: Dict
                - spec: Dict
                - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_present:
              k8s.core.v1.persistent_volume_claim.present:
                - name: "pvc-1"
                - metadata:
                    name: "pvc-1"
                    labels:
                      name: "pvc-1"
                    annotations:
                      volume.beta.kubernetes.io/storage-class: "sc-1"
                - spec:
                    access_modes:
                      - ReadWriteMany
                    resources:
                      requests:
                        storage: 1Mi

    """

    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    # Get namespace
    namespace = metadata.get("namespace") if "namespace" in metadata else "default"
    metadata["namespace"] = namespace

    # Check for existing persistent_volume_claim by name in namespace
    before = None
    if resource_id:
        persistent_volume_claim = (
            await hub.exec.k8s.core.v1.persistent_volume_claim.get(
                ctx, name=name, resource_id=resource_id, namespace=namespace
            )
        )
        if not persistent_volume_claim["result"] or not persistent_volume_claim["ret"]:
            result["result"] = False
            result["comment"] = tuple(persistent_volume_claim["comment"])
            return result
        before = persistent_volume_claim["ret"]

    # Update current state
    result["old_state"] = before

    # Handle no change behaviour
    desired_state = {
        "resource_id": resource_id,
        "metadata": metadata,
        "spec": spec,
    }

    desired_state = hub.tool.k8s.state_utils.merge_arguments(
        desire_state=desired_state, current_state=result["old_state"]
    )
    is_change_detected = before is None or bool(
        differ.deep_diff(old=result["old_state"] or {}, new=desired_state)
    )

    if not is_change_detected:
        result["comment"] = hub.tool.k8s.comment_utils.already_exists_comment(
            resource_type="k8s.core.v1.persistent_volume_claim", name=name
        )
        result["new_state"] = copy.deepcopy(result["old_state"])
        return result

    # Handle test behaviour
    if ctx.get("test", False):
        result["new_state"] = hub.tool.k8s.test_state_utils.generate_test_state(
            enforced_state=result["old_state"],
            desired_state=desired_state,
        )
        result["comment"] = (
            hub.tool.k8s.comment_utils.would_update_comment(
                resource_type="k8s.core.v1.persistent_volume_claim", name=name
            )
            if before
            else hub.tool.k8s.comment_utils.would_create_comment(
                resource_type="k8s.core.v1.persistent_volume_claim", name=name
            )
        )
        return result

    # Handle actual resource create or update
    body = hub.tool.k8s.marshaller.unmarshal(
        desired_state=desired_state, k8s_model_name="V1PersistentVolumeClaim"
    )
    if before:
        ret = await hub.exec.k8s.client.CoreV1Api.replace_namespaced_persistent_volume_claim(
            ctx, name=resource_id, namespace=namespace, body=body
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.update_comment(
            resource_type="k8s.core.v1.persistent_volume_claim", name=name
        )
    else:
        ret = await hub.exec.k8s.client.CoreV1Api.create_namespaced_persistent_volume_claim(
            ctx, namespace=namespace, body=body
        )
        resource_id = body.metadata.name
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.create_comment(
            resource_type="k8s.core.v1.persistent_volume_claim", name=name
        )

    # Fetch the updated resource and update new_state
    persistent_volume_claim = await hub.exec.k8s.core.v1.persistent_volume_claim.get(
        ctx, name=name, resource_id=resource_id, namespace=namespace
    )
    if not persistent_volume_claim["result"]:
        result["comment"] += persistent_volume_claim["comment"]
        result["result"] = persistent_volume_claim["result"]
        return result

    result["new_state"] = persistent_volume_claim["ret"]
    return result


async def absent(
    hub,
    ctx,
    name: str,
    metadata: Dict,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deletes a PersistentVolumeClaim.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        metadata(dict):
            Standard object's metadata.
            More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.

    Request Syntax:

        .. code-block:: sls

            [service-name]:
              k8s.core.v1.service.absent:
                - name: 'string'
                - metadata: Dict
                - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_absent:
              k8s.core.v1.persistent_volume_claim.absent:
                - name: "pvc-1"
                - resource_id: "pvc-1"
                - metadata:
                    namespace: "default"
    """

    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    namespace = metadata.get("namespace") if "namespace" in metadata else "default"

    before = None
    if resource_id:
        persistent_volume_claim = (
            await hub.exec.k8s.core.v1.persistent_volume_claim.get(
                ctx, name=name, resource_id=resource_id, namespace=namespace
            )
        )
        if persistent_volume_claim and persistent_volume_claim["result"]:
            before = persistent_volume_claim["ret"]
            result["old_state"] = before

    if not before:
        result["comment"] = hub.tool.k8s.comment_utils.already_absent_comment(
            resource_type="k8s.core.v1.persistent_volume_claim", name=name
        )
    elif ctx.get("test", False):
        result["comment"] = hub.tool.k8s.comment_utils.would_delete_comment(
            resource_type="k8s.core.v1.persistent_volume_claim", name=name
        )
    else:
        ret = await hub.exec.k8s.client.CoreV1Api.delete_namespaced_persistent_volume_claim(
            ctx, name=resource_id, namespace=namespace
        )
        if not ret["result"]:
            result["result"] = ret["result"]
            result["comment"] = ret["comment"]
            return result

        result["comment"] = hub.tool.k8s.comment_utils.delete_comment(
            resource_type="k8s.core.v1.persistent_volume_claim", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes the resource in a way that can be recreated/managed with the corresponding "present" function.

    list or watch objects of kind PersistentVolumeClaim.


    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe k8s.core.v1.persistent_volume_claim

    """
    result = {}
    ret = await hub.exec.k8s.core.v1.persistent_volume_claim.list(
        ctx, name="k8s.core.v1.persistent_volume_claim.describe"
    )
    if not ret["result"]:
        hub.log.debug(
            f"Could not describe k8s.core.v1.persistent_volume_claim {ret['comment']}"
        )
        return {}

    for resource in ret["ret"]:
        result[resource.get("resource_id")] = {
            "k8s.core.v1.persistent_volume_claim.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
