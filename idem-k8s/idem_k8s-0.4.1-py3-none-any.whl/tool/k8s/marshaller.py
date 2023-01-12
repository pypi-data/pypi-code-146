import re
from typing import Any
from typing import Dict
from typing import List

from kubernetes import client as k8s_client


def marshal(
    hub,
    k8s_object: Any,
    skip_attributes: List,
    skip_empty_values: bool,
    include_empty_string_keys: List = [],
):
    result = {}
    representation = k8s_object.to_dict()
    for key, value in representation.items():
        processed_value = process(
            key, value, skip_attributes, skip_empty_values, include_empty_string_keys
        )
        if skip_empty_values and not processed_value:
            continue
        result[key] = processed_value
    return result


def process(
    key: str,
    value: Any,
    skip_attributes: List,
    skip_empty_values: bool,
    include_empty_string_keys: List = [],
):
    # Handle skipping attributes
    if key in skip_attributes:
        return None

    # Handle skipping empty values
    if (not (key in include_empty_string_keys and value is not None)) and (
        (skip_empty_values and not value) or (skip_empty_values and value == "null")
    ):
        return None

    new_skip_attr = [
        item[len(key + ".") :] for item in skip_attributes if item.startswith(key + ".")
    ]
    if isinstance(value, list):
        result = []
        for item in value:
            processed_item = process(
                key, item, new_skip_attr, skip_empty_values, include_empty_string_keys
            )
            if processed_item or (
                key in include_empty_string_keys and processed_item is not None
            ):
                result.append(processed_item)
        return result
    if isinstance(value, dict):
        result = {}
        for k, v in value.items():
            processed_item = process(
                k, v, new_skip_attr, skip_empty_values, include_empty_string_keys
            )
            if processed_item or (
                key in include_empty_string_keys and processed_item is not None
            ):
                result[k] = processed_item
        return result
    return value


def unmarshal(hub, desired_state: Dict, k8s_model_name: str):
    k8s_class = getattr(k8s_client, k8s_model_name)
    arguments = {}
    for key, val in desired_state.items():
        if not k8s_class.openapi_types.get(key):
            continue
        result = val
        if isinstance(val, list):
            item_type = get_item_type(k8s_class, key)
            if item_type:
                result = [unmarshal(hub, item, item_type) for item in val]
        elif isinstance(val, dict):
            item_type = get_item_type(k8s_class, key)
            if item_type:
                result = unmarshal(hub, val, item_type)
        arguments[key] = result
    k8s_object = getattr(k8s_client, k8s_model_name)(**arguments)
    return k8s_object


def get_item_type(k8s_class, key: str):
    item_type = k8s_class.openapi_types.get(key).strip()
    if item_type.startswith("list") and re.search("list\\[(.+?)\\]", item_type):
        item_type = re.search("list\\[(.+?)\\]", item_type).group(1)
    if hasattr(k8s_client, item_type):
        return item_type
    return None
