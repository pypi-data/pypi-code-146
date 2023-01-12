"""Exec module for managing Kubernetes RoleBinding(s)."""
from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str,
    namespace: str = "default",
) -> Dict[str, Any]:
    """Retrieves a Kubernetes RbacV1 RoleBinding.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str):
            The metadata.name of the Kubernetes role_binding.

        namespace(str, Optional):
            The Kubernetes namespace in which role_bindingwas created.
            Defaults to 'default' namespace in case None.

    Returns:
        Dict[str, Any]:
            Return a role_binding in a given namespace.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec k8s.rbac.v1.role_binding.get name='role_binding-name' resource_id='role_binding' namespace='default'

        Using in a state:

        .. code-block:: yaml

            my-kubernetes-role-binding:
              exec.run:
                - path: k8s.rbac.v1.role_binding.get
                - kwargs:
                    name: 'role_binding-name'
                    resource_id: 'role_binding-name'
                    namespace: 'default'
    """
    result = dict(comment=[], ret=None, result=True)

    role_binding = (
        await hub.exec.k8s.client.RbacAuthorizationV1Api.read_namespaced_role_binding(
            ctx, name=resource_id, namespace=namespace
        )
    )

    if not role_binding["result"]:
        # Do not return success=false when it is not found.
        if "ApiException" in str(
            role_binding["comment"]
        ) and "Reason: Not Found" in str(role_binding["comment"]):
            result["comment"].append(
                hub.tool.k8s.comment_utils.get_empty_comment(
                    resource_type="k8s.rbac.v1.role_binding",
                    name=resource_id,
                )
            )
            result["comment"] += list(role_binding["comment"])
            return result

        result["comment"] += list(role_binding["comment"])
        result["result"] = False
        return result

    if not role_binding["ret"]:
        result["comment"].append(
            hub.tool.k8s.comment_utils.get_empty_comment(
                resource_type="k8s.rbac.v1.role_binding", name=resource_id
            )
        )
        return result

    result[
        "ret"
    ] = hub.tool.k8s.rbac.v1.role_binding_utils.convert_raw_role_binding_to_present(
        role_binding=role_binding["ret"]
    )
    return result


async def list_(
    hub,
    ctx,
    name: str = None,
    namespace: str = None,
) -> Dict:
    """Retrieves list of Kubernetes RoleBindings.

    Args:
        name(str, Optional):
            The name of the Idem state.
        namespace(str, Optional):
            The Kubernetes namespace in which role_bindingwas created.
            Defaults to all namespace in case None.

    Returns:
        Dict[str, Any]:
            Returns role bindings in present format


    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec k8s.rbac.v1.role_binding.list name="idem_name" namespace="default"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: k8s.rbac.v1.role_binding.list
                - kwargs:
                    name: my_resource
                    namespace: default


    """
    result = dict(comment=[], ret=[], result=True)
    if namespace is None:
        ret = await hub.exec.k8s.client.RbacAuthorizationV1Api.list_role_binding_for_all_namespaces(
            ctx
        )
    else:
        ret = await hub.exec.k8s.client.RbacAuthorizationV1Api.list_namespaced_role_binding(
            ctx, namespace=namespace
        )

    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]:
        result["comment"].append(
            hub.tool.k8s.comment_utils.list_empty_comment(
                resource_type="k8s.rbac.v1.role_binding", name=name
            )
        )
        return result
    for role_binding in ret["ret"].items:
        converted_resource = (
            hub.tool.k8s.rbac.v1.role_binding_utils.convert_raw_role_binding_to_present(
                role_binding=role_binding
            )
        )

        result["ret"].append(converted_resource)
    return result
