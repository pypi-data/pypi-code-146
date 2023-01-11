from typing import Dict
from typing import List

from cloudspec import CloudSpecFunction


def return_type(hub, func_data: CloudSpecFunction):
    ret = ""
    if func_data.return_type:
        ret += "\n\n    Returns:\n"
        ret += f"        {func_data.return_type}"
        ret += "\n"
    return ret


def doc(hub, func_data: CloudSpecFunction):
    if func_data.doc:
        doc = func_data.doc.replace('"""', "'''")
        doc = "\n" + hub.tool.format.wrap.indent(doc, 1) + "\n"
    else:
        doc = ""
    return doc


def parse(hub, functions: Dict[str, CloudSpecFunction], targets: List[str]):
    funcs = {}
    if not functions:
        # It might be an init file
        return funcs
    for function_name in targets:
        function_data = functions[function_name]

        doc = hub.cloudspec.parse.function.doc(function_data)
        doc += hub.cloudspec.parse.param.sphinx_docs(function_data.params)
        doc += "\n\n    Returns:\n        Dict[str, Any]\n"

        param_mapping = hub.cloudspec.parse.param.mappings(function_data.params)
        funcs[function_name] = dict(
            function=dict(
                name=function_name,
                hardcoded=function_data.hardcoded,
                doc=doc,
                header_params=hub.cloudspec.parse.param.headers(function_data.params),
                required_call_params=hub.cloudspec.parse.param.callers(
                    function_data.params
                ),
            ),
            parameter=dict(
                mapping=param_mapping,
            ),
        )
    return funcs
