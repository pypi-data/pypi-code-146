def parse(hub, spec: str, resource_name: str):
    k8s_resource_definitions = spec.get("definitions")
    k8s_resources = parse_paths(spec.get("paths"))

    if resource_name not in k8s_resources:
        hub.log.error(f"unsupported resource {resource_name} for kubernetes provider")
        raise NameError(resource_name)

    parsed_data = {}
    for action in ("create", "delete", "update", "get", "list"):
        resource_metadata = identify_resource_metadata(
            k8s_resources[resource_name], action
        )
        parsed_data[action] = parse_resource_metadata(
            hub, action, k8s_resource_definitions, resource_metadata
        )
    return parsed_data


def parse_paths(paths):
    resource_list = {}
    for uri, apis in paths.items():
        for http_method, details in apis.items():
            if "x-kubernetes-group-version-kind" not in details:
                continue

            # resource category : group/version/kind
            group_version_kind = [
                details["x-kubernetes-group-version-kind"].get("group")
                if details["x-kubernetes-group-version-kind"].get("group")
                else "core",
                details["x-kubernetes-group-version-kind"].get("version"),
                details["x-kubernetes-group-version-kind"].get("kind"),
            ]
            resource_category = "/".join([item for item in group_version_kind if item])
            api_class = (
                "".join(
                    item[0].upper() + item[1:]
                    for item in details["tags"].pop().split("_")
                )
                + "Api"
            )
            spec_data = {
                "description": details["description"],
                "http_method": http_method,
                "operation_id": details["operationId"],
                "method_params": details["parameters"]
                if "parameters" in details
                else None,
                "responses": details["responses"] if "responses" in details else None,
                "api_uri": uri,
                "api_params": apis["parameters"] if "parameters" in apis else None,
                "api_class": api_class,
            }
            if resource_category in resource_list:
                resource_list[resource_category].append(spec_data)
            else:
                resource_list[resource_category] = [
                    spec_data,
                ]
    return resource_list


def identify_resource_metadata(spec_data_list, action):
    spec_data_mapping = {
        "create": {
            "operation_prefix": "create",
            "http_method": "post",
            "exclusion_terms": [],
        },
        "update": {
            "operation_prefix": "replace",
            "http_method": "put",
            "exclusion_terms": [],
        },
        "delete": {
            "operation_prefix": "delete",
            "http_method": "delete",
            "exclusion_terms": ["Collection"],
        },
        "get": {
            "operation_prefix": "read",
            "http_method": "get",
            "exclusion_terms": [],
        },
        "list": {
            "operation_prefix": "list",
            "http_method": "get",
            "exclusion_terms": ["Namespaced"],
        },
    }

    if not spec_data_list:
        return {}

    filtered = [
        spec_data
        for spec_data in spec_data_list
        if (
            spec_data["http_method"] == spec_data_mapping[action]["http_method"]
            and spec_data["operation_id"].startswith(
                spec_data_mapping[action]["operation_prefix"]
            )
            and not any(
                map(
                    spec_data["operation_id"].__contains__,
                    spec_data_mapping[action]["exclusion_terms"],
                )
            )
        )
    ]
    return filtered[0]


def parse_resource_metadata(hub, action, resource_definitions, resource_metadata):
    payload_type, params = parse_spec_parameters(
        hub,
        action,
        resource_definitions,
        resource_metadata.get("method_params"),
    )
    return {
        "doc": resource_metadata.get("description"),
        "api_class": resource_metadata.get("api_class"),
        "function_name": hub.tool.format.case.snake(
            resource_metadata.get("operation_id")
        ),
        "params": params,
        "payload_type": None
        if not payload_type
        else "".join([item.capitalize() for item in payload_type.split(".") if item]),
    }


def parse_spec_parameters(hub, action, resource_definitions, method_params):
    payload_type = None
    parameters = {}
    if not method_params:
        return payload_type, parameters

    excluded_parameters = ["apiVersion", "kind"]
    if action == "create":
        props = {}
        for param in method_params:
            if "in" not in param or param["in"] != "body":
                continue
            schema = param.get("schema")
            definition_name = schema.get("$ref").split("/").pop()
            definition = resource_definitions.get(definition_name)
            payload_type = definition_name
            props = definition.get("properties")
            break
        for param_name, details in props.items():
            if param_name in excluded_parameters:
                continue
            parameters[param_name] = {
                "default": None,
                "doc": "\n            ".join(
                    hub.tool.format.wrap.wrap(details.get("description"), width=96)
                ),
                "param_type": hub.pop_create.k8s.type.translate_type(
                    details.get("type") if "$ref" not in details else "map"
                ),
                "required": True,
                "target": "kwargs",  # arg, kwargs, hardcoded
                "target_type": "mapping",
            }
    if action == "delete":
        parameters["metadata"] = {
            "default": None,
            "doc": "\n            ".join(
                hub.tool.format.wrap.wrap(
                    "Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.",
                    width=96,
                )
            ),
            "param_type": "Dict",
            "required": True,
            "target": "kwargs",
            "target_type": "mapping",
        }

    return payload_type, parameters
