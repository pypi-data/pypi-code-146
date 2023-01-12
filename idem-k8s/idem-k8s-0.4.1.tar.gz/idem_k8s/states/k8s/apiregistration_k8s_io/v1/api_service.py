"""State module for managing Kubernetes APIService."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict

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
            ("group_priority_minimum", int),
            ("group", str, field(default=None)),
            ("ca_bundle", str, field(default=None)),
            ("insecure_skip_tls_verify", bool, field(default=None)),
            ("version", str, field(default=None)),
            ("version_priority", int, field(default=None)),
            (
                "service",
                make_dataclass(
                    "service",
                    [
                        ("name", str, field(default=None)),
                        ("namespace", str, field(default=None)),
                        ("port", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ),
    resource_id: str = None,
) -> Dict[str, Any]:
    """Creates an APIService.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        metadata(dict):
            Standard object's metadata.
            More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.

        spec(dict):
            Spec contains information for locating and communicating with a server.

    Request Syntax:

        .. code-block:: sls

            [api_service-name]:
              k8s.apiregistration_k8s_io.v1.api_service.present:
                - name: 'string'
                - metadata: Dict
                - spec: Dict
                - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_present:
              k8s.apiregistration_k8s_io.v1.api_service.present:
                - name: 'test-api-service'
                - metadata:
                    labels:
                      k8s-app: metrics-server
                    name: v1beta1.metrics.k8s.io
                - spec:
                    group: metrics.k8s.io
                    group_priority_minimum: 100
                    insecure_skip_tls_verify: true
                    service:
                      name: metrics-server
                      namespace: kube-system
                    version: v1beta1
                    version_priority: 100

    """

    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    # Check for existing api_service by name
    before = None
    if resource_id:
        api_service = await hub.exec.k8s.apiregistration_k8s_io.v1.api_service.get(
            ctx, name=name, resource_id=resource_id
        )
        if not api_service["result"] or not api_service["ret"]:
            result["result"] = False
            result["comment"] = tuple(api_service["comment"])
            return result
        before = api_service["ret"]

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
            resource_type="k8s.apiregistration_k8s_io.v1.api_service", name=name
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
                resource_type="k8s.apiregistration_k8s_io.v1.api_service", name=name
            )
            if before
            else hub.tool.k8s.comment_utils.would_create_comment(
                resource_type="k8s.apiregistration_k8s_io.v1.api_service", name=name
            )
        )
        return result

    # Handle actual resource create or update
    body = hub.tool.k8s.marshaller.unmarshal(
        desired_state=desired_state, k8s_model_name="V1APIService"
    )
    if before:
        ret = await hub.exec.k8s.client.ApiregistrationV1Api.replace_api_service(
            ctx, name=resource_id, body=body
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.update_comment(
            resource_type="k8s.apiregistration_k8s_io.v1.api_service", name=name
        )
    else:
        ret = await hub.exec.k8s.client.ApiregistrationV1Api.create_api_service(
            ctx, body=body
        )
        resource_id = body.metadata.name
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.k8s.comment_utils.create_comment(
            resource_type="k8s.apiregistration_k8s_io.v1.api_service", name=name
        )

    # Fetch the updated resource and update new_state
    api_service = await hub.exec.k8s.client.ApiregistrationV1Api.read_api_service(
        ctx, name=resource_id
    )
    if not api_service["result"]:
        result["comment"] = result["comment"] + api_service["comment"]
        result["result"] = api_service["result"]
        return result
    after = api_service["ret"]
    result[
        "new_state"
    ] = hub.tool.k8s.apiregistration_k8s_io.v1.api_service_utils.convert_raw_api_service_to_present(
        api_service=after
    )
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deletes an APIService.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

    Request Syntax:

        .. code-block:: sls

            [api-service-name]:
              k8s.apiregistration_k8s_io.v1.api_service.absent:
                - name: 'string'
                - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_absent:
              k8s.apiregistration_k8s_io.v1.api_service.absent:
                - name: "test-api-service"
                - resource_id: "test-api-service"
    """

    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)

    before = None
    if resource_id:
        api_service = await hub.exec.k8s.apiregistration_k8s_io.v1.api_service.get(
            ctx, name=name, resource_id=resource_id
        )
        if api_service and api_service["result"]:
            before = api_service["ret"]
            result["old_state"] = before

    if not before:
        result["comment"] = hub.tool.k8s.comment_utils.already_absent_comment(
            resource_type="k8s.apiregistration_k8s_io.v1.api_service", name=name
        )
    elif ctx.get("test", False):
        result["comment"] = hub.tool.k8s.comment_utils.would_delete_comment(
            resource_type="k8s.apiregistration_k8s_io.v1.api_service", name=name
        )
    else:
        ret = await hub.exec.k8s.client.ApiregistrationV1Api.delete_api_service(
            ctx, name=resource_id
        )
        if not ret["result"]:
            result["result"] = ret["result"]
            result["comment"] = ret["comment"]
            return result

        result["comment"] = hub.tool.k8s.comment_utils.delete_comment(
            resource_type="k8s.apiregistration_k8s_io.v1.api_service", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes the resource in a way that can be recreated/managed with the corresponding "present" function.

    list or watch objects of kind APIService.


    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe k8s.apiregistration_k8s_io.v1.api_service
    """

    result = {}
    ret = await hub.exec.k8s.apiregistration_k8s_io.v1.api_service.list(
        ctx, name="k8s.apiregistration_k8s_io.v1.api_service.describe"
    )
    if not ret["result"]:
        hub.log.debug(
            f"Could not describe k8s.apiregistration_k8s_io.v1.api_service {ret['comment']}"
        )
        return {}

    for resource in ret["ret"]:
        result[resource.get("resource_id")] = {
            "k8s.apiregistration_k8s_io.v1.api_service.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
