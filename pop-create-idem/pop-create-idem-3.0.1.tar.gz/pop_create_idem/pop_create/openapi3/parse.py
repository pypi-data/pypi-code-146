from typing import Any
from typing import Dict
from typing import Tuple

import openapi3.object_base

__func_alias__ = {"type_": "type"}


def plugins(hub, ctx, paths: openapi3.object_base.Map) -> Dict[str, Any]:
    ret = {}
    for name, path in paths.items():
        assert isinstance(path, openapi3.paths.Path)
        # Get the request type that works for this request
        for request_type in path.raw_element.keys():
            func: openapi3.paths.Operation = getattr(path, request_type)
            if not func:
                continue
            subs = [hub.tool.format.case.snake(sub) for sub in func.tags]
            if not subs:
                plugin = "init"
            else:
                plugin = subs.pop()

            refs = [ctx.service_name] + subs + [plugin]
            ref = ".".join(refs)
            if ref not in ret:
                # This is the first time we have looked at this plugin
                ret[ref] = {"functions": {}, "doc": ""}
            func_name, func_data = hub.pop_create.openapi3.parse.function(name, func)
            func_data["hardcoded"] = {
                "method": request_type,
                "path": name.split(" ")[0],
            }
            ret[ref]["functions"][func_name] = func_data
    return ret


def function(
    hub,
    name: str,
    func: openapi3.paths.Operation,
) -> Tuple[str, Dict[str, Any]]:
    # This is the preferred way to get a function name
    func_name = func.operationId
    # Fallback function name based on the pets example
    if not func_name and " " in name:
        func_name = "_".join(name.split(" ")[1:]).lower()
    if not func_name and func.extensions:
        func_name = func.extensions[sorted(func.extensions.keys())[0]]
    else:
        func_name = func.summary

    # Maybe we need more fallbacks, you tell me
    if not func_name:
        # Maybe a fallback based on the path and method?
        raise AttributeError(f"Not sure how to find func name for {name}, help me out")

    func_name = hub.tool.format.case.snake(func_name)

    func_spec = {
        "doc": (func.description or "").strip(),
        "params": {
            p.name: hub.pop_create.openapi3.parse.parameter(p) for p in func.parameters
        },
    }
    return func_name, func_spec


def parameter(hub, parameter: openapi3.paths.Parameter):
    if parameter.in_ == "query":
        target_type = "mapping"
    elif parameter.in_ == "path":
        target_type = "mapping"
    elif parameter.in_ == "header":
        target_type = "mapping"
    elif parameter.in_ == "cookie":
        target_type = "mapping"
    else:
        raise ValueError(f"Unknown parameter type: {parameter.in_}")

    return {
        "required": parameter.required,
        "target_type": target_type,
        "target": parameter.in_,
        "param_type": hub.pop_create.openapi3.parse.type(parameter.schema.type),
        "doc": parameter.description or parameter.name,
    }


def type_(hub, param_type: str) -> str:
    if "integer" == param_type:
        return "int"
    elif "boolean" == param_type:
        return "bool"
    elif "number" == param_type:
        return "float"
    elif "string" == param_type:
        return "str"
    else:
        return ""
