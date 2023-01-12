import json
from collections import OrderedDict


def get_plugins(hub, k8s_openapi_spec_str: str, resource: str):
    plugins = {}

    # Parse open-api spec to retrieve state file template metadata
    k8s_openapi_spec = json.loads(k8s_openapi_spec_str)
    resource_metadata = hub.pop_create.k8s.openapi_spec_parser.parse(
        spec=k8s_openapi_spec, resource_name=resource
    )
    if not resource_metadata:
        raise NameError(resource)

    # Populate plugin with resource metadata
    api_class = resource_metadata["create"].get("api_class")
    resource_name = hub.tool.format.case.snake(resource.split("/").pop())
    plugin_key = ".".join(
        [hub.tool.format.case.snake(item) for item in resource.split("/") if item]
    )

    create_function = resource_metadata["create"].get("function_name")
    delete_function = resource_metadata["delete"].get("function_name")
    update_function = resource_metadata["update"].get("function_name")
    get_function = resource_metadata["get"].get("function_name")
    list_function = resource_metadata["list"].get("function_name")

    create_params = OrderedDict()
    if "name" not in create_params:
        create_params["name"] = hub.pop_create.k8s.template.NAME_PARAMETER
    create_params["resource_id"] = hub.pop_create.k8s.template.RESOURCE_ID_PARAMETER
    create_params.update(resource_metadata["create"].get("params"))
    create_params["timeout"] = hub.pop_create.k8s.template.CREATE_TIMEOUT_PARAMETER

    state_params = (
        "{ "
        + ",".join(
            [
                f' "{hub.tool.format.case.snake(key)}": {hub.tool.format.case.snake(key)}'
                for key in create_params
            ]
        )
        + " }"
    )

    delete_params = OrderedDict()
    if "name" not in delete_params:
        delete_params["name"] = hub.pop_create.k8s.template.NAME_PARAMETER
    delete_params["resource_id"] = hub.pop_create.k8s.template.RESOURCE_ID_PARAMETER
    delete_params.update(resource_metadata["delete"].get("params"))
    delete_params["timeout"] = hub.pop_create.k8s.template.DELETE_TIMEOUT_PARAMETER

    shared_function_data = {
        "hardcoded": {
            "resource": resource_name,
            "payload_type": resource_metadata["create"].get("payload_type"),
            "create_function": f"hub.exec.k8s.client.{api_class}.{create_function}",
            "delete_function": f"hub.exec.k8s.client.{api_class}.{delete_function}",
            "update_function": f"hub.exec.k8s.client.{api_class}.{update_function}",
            "get_function": f"hub.exec.k8s.client.{api_class}.{get_function}",
            "list_function": f"hub.exec.k8s.client.{api_class}.{list_function}",
            "api_class": api_class,
            "waiter_function": get_function,
            "state_parameters": state_params,
        },
    }

    plugins[plugin_key] = {
        "doc": resource,
        "imports": [
            "import copy",
            "from typing import Any",
            "from typing import Dict",
            "from typing import List",
            "from typing import Text",
            "from typing import Tuple",
            "from deepdiff import DeepDiff",
            "__contracts__ = ['resource']",
        ],
        "functions": {
            "present": dict(
                doc=resource_metadata["create"].get("doc"),
                params=dict(name=create_params.pop("name"), **create_params),
                **shared_function_data,
            ),
            "absent": dict(
                doc=resource_metadata["delete"].get("doc"),
                params=dict(name=delete_params.pop("name"), **delete_params),
                **shared_function_data,
            ),
            "describe": dict(
                doc=resource_metadata["list"].get("doc"),
                params={},
                **shared_function_data,
            ),
        },
    }
    return plugins
