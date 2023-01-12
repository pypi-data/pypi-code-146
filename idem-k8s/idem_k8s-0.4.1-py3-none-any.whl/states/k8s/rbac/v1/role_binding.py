"""State module for managening k8s RoleBinding."""
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
    role_ref: make_dataclass(
        "role_ref",
        [
            ("api_group", str),
            ("kind", str),
            ("name", str),
        ],
    ),
    subjects: List[
        make_dataclass(
            "subjects",
            [
                ("kind", str),
                ("name", str),
                ("namespace", str),
            ],
        )
    ],
    resource_id: str = None,
) -> Dict[str, Any]:
    """create a RoleBinding

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.
        metadata(dict):
            Standard object's metadata.
        role_ref(dict):
            RoleRef can reference a Role in the current namespace or a ClusterRole in the global namespace.
            If the RoleRef cannot be resolved, the Authorizer must return an error.
        subjects(list):
            Subjects holds references to the objects the role applies to.

    Request Syntax:

        .. code-block:: sls

            [unmanaged_resource]:
              k8s.rbac.v1.role_binding.present:
                - name: 'string'
                - metadata: 'dict'
                - role_ref: 'dict'
                - subjects: 'dict'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_present:
              k8s.rbac.v1.role_binding.present:
                  - resource_id: system:controller:token-cleaner
                  - metadata:
                      annotations:
                        rbac.authorization.kubernetes.io/autoupdate: 'true'
                      labels:
                        kubernetes.io/bootstrapping: rbac-defaults
                      name: system:controller:token-cleaner
                      namespace: kube-system
                  - role_ref:
                      api_group: rbac.authorization.k8s.io
                      kind: Role
                      name: system:controller:token-cleaner
                  - subjects:
                    - kind: ServiceAccount
                      name: token-cleaner
                      namespace: kube-system"""

    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    # Get namespace
    namespace = metadata.get("namespace", "default")

    # Check for existing role_binding by name in namespace
    before = None
    if resource_id:
        role_binding = await hub.exec.k8s.rbac.v1.role_binding.get(
            ctx, name=name, resource_id=resource_id, namespace=namespace
        )
        if not role_binding["result"]:
            result["comment"] = role_binding["comment"]
            result["result"] = role_binding["result"]
            return result
        before = role_binding["ret"]

    # Update current state
    result["old_state"] = before

    # Handle no change behaviour
    desired_state = {
        "resource_id": resource_id,
        "metadata": metadata,
        "role_ref": role_ref,
        "subjects": subjects,
    }

    desired_state = hub.tool.k8s.state_utils.merge_arguments(
        desire_state=desired_state, current_state=result["old_state"]
    )

    is_change_detected = before is None or bool(
        differ.deep_diff(old=result["old_state"] or {}, new=desired_state)
    )

    if not is_change_detected:
        result["comment"] = hub.tool.k8s.comment_utils.already_exists_comment(
            resource_type="k8s.rbac.v1.role_binding", name=name
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
                resource_type="k8s.rbac.v1.role_binding", name=name
            )
            if before
            else hub.tool.k8s.comment_utils.would_create_comment(
                resource_type="k8s.rbac.v1.role_binding", name=name
            )
        )
        return result

    # Handle actual resource create or update
    body = hub.tool.k8s.marshaller.unmarshal(
        desired_state=desired_state, k8s_model_name="V1RoleBinding"
    )
    if before:
        ret = await hub.exec.k8s.client.RbacAuthorizationV1Api.replace_namespaced_role_binding(
            ctx, name=resource_id, namespace=namespace, body=body
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.update_comment(
            resource_type="k8s.rbac.v1.role_binding", name=name
        )
    else:
        ret = await hub.exec.k8s.client.RbacAuthorizationV1Api.create_namespaced_role_binding(
            ctx, namespace=namespace, body=body
        )
        resource_id = body.metadata.name
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.create_comment(
            resource_type="k8s.rbac.v1.role_binding", name=name
        )
    # Fetch the updated resource and update new_state
    role_binding = await hub.exec.k8s.rbac.v1.role_binding.get(
        ctx, name=name, resource_id=resource_id, namespace=namespace
    )
    if not role_binding["result"]:
        result["comment"] = result["comment"] + role_binding["comment"]
        result["result"] = role_binding["result"]
        return result
    result["new_state"] = role_binding["ret"]

    return result


async def absent(
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
    ) = None,
    resource_id: str = None,
):
    """Delete a RoleBinding

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.
        metadata(dict, Optional):
            Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-
            architecture/api-conventions.md#metadata.

    Returns:
        Dict[str, Any]

    Request Syntax:

        .. code-block:: sls

            [k8s.rbac.v1.role_binding.name]:
              k8s.rbac.v1.role_binding.absent:
                - resource_id: 'string'
                - name: 'string'
                - metadata: 'dict'
    Examples:

        .. code-block:: sls

            resource_is_absent:
              k8s.rbac.v1.role_binding.absent:
                - resource_id: 'k8s.rbac.v1.role_binding.id'
                - name: 'role_binding_name'
    """

    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)
    namespace = "default"
    if metadata:
        namespace = metadata.get("namespace", "default")
    before = None
    if resource_id:
        role_binding = await hub.exec.k8s.rbac.v1.role_binding.get(
            ctx, name=name, resource_id=resource_id, namespace=namespace
        )
        if role_binding and role_binding["result"]:
            before = role_binding["ret"]
            result["old_state"] = before

    if not before:
        result["comment"] = hub.tool.k8s.comment_utils.already_absent_comment(
            resource_type="k8s.rbac.v1.role_binding", name=name
        )
    elif ctx.get("test", False):
        result["comment"] = hub.tool.k8s.comment_utils.would_delete_comment(
            resource_type="k8s.rbac.v1.role_binding", name=name
        )
    else:
        ret = await hub.exec.k8s.client.RbacAuthorizationV1Api.delete_namespaced_role_binding(
            ctx, name=resource_id, namespace=namespace
        )
        if not ret["result"]:
            result["result"] = ret["result"]
            result["comment"] = ret["comment"]
            return result

        result["comment"] = hub.tool.k8s.comment_utils.delete_comment(
            resource_type="k8s.rbac.v1.role_binding", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """list objects of kind RoleBinding

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe k8s.rbac.v1.role_binding
    """

    ret = await hub.exec.k8s.rbac.v1.role_binding.list(
        ctx, name="k8s.rbac.v1.role_binding.describe"
    )
    if not ret["result"]:
        hub.log.debug(f"Could not describe role_binding {ret['comment']}")
        return {}

    result = {}

    for resource in ret["ret"]:
        result[resource.get("resource_id")] = {
            "k8s.rbac.v1.role_binding.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result
