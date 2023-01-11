from typing import Dict

from cloudspec import CloudSpecParam


def sphinx_docs(hub, parameters: CloudSpecParam) -> str:
    """
    Get the sphinx docs for the parameters
    """
    if not parameters:
        return ""

    ret = "\n    Args:\n"
    for param in parameters.values():
        ret += f"        {param.snaked}"
        # Doc strings standard is lower case list[]
        if param.param_type is None:
            param_type = None
        else:
            param_type = param.param_type.replace("List[", "list[")
        if param.member:
            # Complex params are represented as Dict[str, Any] in the sphinx docs
            param_type = param_type.format("Dict[str, Any]")

        if param_type:
            ret += f"({param_type}{', optional' if not param.required else ''})"

        ret += f": {param.doc}"
        if not ret.endswith("."):
            ret += "."
        if not param.required:
            ret += f" Defaults to {param.default}."

        ret += nested_params_docs(param, "            ")
        ret += "\n"

    return ret.rstrip()


def nested_params_docs(param: CloudSpecParam, offset: str):
    """
    Get the sphinx docs for the nested parameters
    """
    ret = ""
    if param.member:
        for nested_param_name, nested_param_data in param.member.params.items():
            # Doc strings standard is lower case list[]
            param_type = nested_param_data.param_type.replace("List[", "list[")
            if nested_param_data.member:
                # This is the next level of nested complex argument.
                param_type = param_type.format("Dict[str, Any]")
            ret += f"\n{offset}* "
            ret += f"{nested_param_name} ({param_type}{', optional' if not nested_param_data.required else ''}): {nested_param_data.doc}"

            # Recursively add doc for all nested complex arguments
            ret += nested_params_docs(nested_param_data, offset + "    ")
    return ret


def headers(hub, parameters: CloudSpecParam) -> str:
    """
    The arguments that will be put in the function definition
    """
    ret = ""

    required_params = {
        name: data for name, data in parameters.items() if data["required"]
    }
    for param_name, param_data in required_params.items():
        ret += add_param_to_header(param_data)

    unrequired_params = {
        name: data for name, data in parameters.items() if not data["required"]
    }

    for param_name, param_data in unrequired_params.items():
        ret += add_param_to_header(param_data)

        # TODO handle this case properly
        if param_data.default == "{}" or param_data.default == "[]":
            ret += f" = None"
        else:
            ret += f" = {param_data.default}"

    return ret


def add_param_to_header(param_data: Dict) -> str:
    ret = f",\n    {param_data.snaked}: "
    if param_data.member:
        # Insert nested complex format for as the argument type.
        # param_type should be "{}|List[{}]|Dict[str, {}]"
        ret += f"{param_data.param_type}".format(
            add_nested_param_to_header(param_data.member, "        ")
        )
    else:
        ret += f"{param_data.param_type}"

    return ret


def add_nested_param_to_header(member: Dict, offset: str) -> str:
    """
    Create a dataclass for a complex nested argument
    """
    ret = f'make_dataclass(\n{offset}"{member.name}",\n{offset}['
    for param_name, param_data in member.get("params").items():
        ret += f"\n{offset}    "
        # TODO: Nested param name should be snaked
        ret += f'("{param_name}", '
        if param_data.member:
            # Recursively add all nested complex arguments
            ret += param_data.param_type.format(
                add_nested_param_to_header(param_data.member, offset + "    ")
            )
        else:
            ret += f"{param_data.param_type}"
        if param_data["required"]:
            ret += f"), "
        else:
            ret += f", field(default={param_data.default})), "
    # Remove last ', '
    ret = ret[0:-2]
    ret += f"\n{offset}]\n{offset})"

    return ret


def callers(hub, parameters: CloudSpecParam) -> str:
    """
    Get a mapping of the function args to the values that will be used in the final caller
    """
    ret = []

    required_params = {
        name: data for name, data in parameters.items() if data["required"]
    }
    for param_data in required_params.values():
        ret.append(f"{param_data.snaked}={param_data.default or 'value'}")

    return ", ".join(ret)


def mappings(hub, parameters: CloudSpecParam) -> Dict[str, str]:
    ret = {}
    map_params = {
        name: data
        for name, data in parameters.items()
        if data["target_type"] == "mapping"
    }
    for name, data in map_params.items():
        target = data["target"]
        if target not in ret:
            ret[target] = {}
        ret[target][name] = data.snaked

    fmt = lambda item: ", ".join(f'"{k}": {v}' for k, v in item.items())
    return {k: f"{{{fmt(v)}}}" for k, v in ret.items()}


def simple_map(hub, parameters: Dict[str, CloudSpecParam]):
    result = {}
    for k, param_data in parameters.items():
        if k == "name" and param_data.target_type == "arg":
            continue
        result[param_data.snaked] = k
    return result
