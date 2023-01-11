import dataclasses
from typing import Any
from typing import Dict
from typing import List

import pop.hub
from dict_tools.data import NamespaceDict

HTTP_REQUEST_FORMAT = """
return await hub.tool.{{cookiecutter.service_name}}.session.request(
    method="{{func.hardcoded.method}}",
    path=f"{{param.value.path}}",
    query_params={{param.mapping.query}},
    data={{param.mapping.data}},
)
"""


def create_hub() -> pop.hub.Hub:
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="tool")
    hub.pop.sub.load_subdirs(hub.tool, recurse=True)
    return hub


class CloudSpec(NamespaceDict):
    """
    Validate a cloud spec

    .. code-block:: json

        {
            "project_name": "",
            "service_name": "",
            "api_version": "latest",
            "request_format": "",
            "plugins": {}
        }
    """

    def __init__(
        self,
        project_name: str,
        service_name: str,
        api_version: str = "latest",
        request_format: Dict[str, str] = None,
        plugins: Dict[str, Dict[str, Any]] = None,
    ):
        """
        :param project_name: The name of the project
        :param service_name: The simple clean_name of the cloud
        :param request_format: Map of function call types to the underlying request methods
        :param plugins: A mapping of plugin references on the hub to CloudSpecPlugin jsons
        """
        if request_format is None:
            request_format = {"http": HTTP_REQUEST_FORMAT}
        if plugins:
            validate_plugins = {
                name: CloudSpecPlugin(**plugin_spec)
                for name, plugin_spec in plugins.items()
            }
        else:
            validate_plugins = {}

        super().__init__(
            api_version=api_version,
            project_name=project_name,
            service_name=service_name,
            request_format=request_format,
            plugins=validate_plugins,
        )


class CloudSpecPlugin(NamespaceDict):
    """

    .. code-block:: json

        {
            "{{cookiecutter.service_name}}.sub.sub.plugin_name": {
                "imports": ["import pathlib", "from sys import executable"],
                "virtual_imports": [],
                "func_alias": {"list_":  "list"},
                "virtualname": "",
                "doc": "a module level docstring",
                "functions": {}
            }
        }
    """

    def __init__(
        self,
        doc: str,
        imports: List[str] = None,
        virtual_imports: List[str] = None,
        contracts: List[str] = None,
        func_alias: Dict[str, str] = None,
        virtualname: str = "",
        sub_virtual: bool = None,
        sub_alias: List[str] = None,
        functions: Dict[str, Dict[str, Dict[str, str]]] = None,
    ):
        """
        Args:
            doc: A docstring for this function
            imports: python imports that will for sure be available, program crashes if not available
            virtual_imports: python imports that prevent the module from loading, plugin does not load if not available
            contracts: A list of contracts to implement for this plugin
            func_alias: A mapping of functions that mirror builtin names, to the names they should have
            virtualname: The name this plugin should be called by on the hub
            sub_virtual: Used to prevent a sub and all it's children from loading
            sub_alias: Only used in init plugins when the parent sub has a name clash
            functions: A mapping of function names to CloudSpecFunction jsons
        """

        if functions:
            validated_functions = {
                name: CloudSpecFunction(**function_spec)
                for name, function_spec in functions.items()
            }
        else:
            validated_functions = {}
        super().__init__(
            doc=doc,
            imports=imports or [],
            virtual_imports=virtual_imports or [],
            contracts=contracts or [],
            func_alias=func_alias or {},
            virtualname=virtualname,
            sub_virtual=sub_virtual,
            sub_alias=sub_alias,
            functions=validated_functions,
        )


class CloudSpecFunction(NamespaceDict):
    """
    .. code-block:: json

        {
            "function_name": {
                "doc": "",
                "return_type": "",
                "hardcoded": {},
                "params": {}
            }
        }
    """

    def __init__(
        self,
        doc: str,
        return_type: str = "None",
        hardcoded: Dict[str, str] = None,
        params: Dict[str, Dict[str, Dict[str, str]]] = None,
    ):
        """
        Args:
            doc: A function docstring
            return_type: return value Type as string
            hardcoded: A mapping of string parameters to string values
            params: A mapping of parameter names to CloudSpecParam jsons
        """
        if params:
            validated_params = {
                name: CloudSpecParam(name=name, **param_spec)
                for name, param_spec in params.items()
            }
        else:
            validated_params = {}
        super().__init__(
            doc=doc,
            return_type=return_type,
            hardcoded=hardcoded or {},
            params=validated_params,
        )


class CloudSpecParam(NamespaceDict):
    """
    .. code-block json::

        {
            "param_name": {
                "doc": "Docstring for this parameter",
                "param_type": "Type",
                "required": True|False,
                "default": "",
                "target": "",
                "target_type": "mapping|value|arg|kwargs"
                "member": {
                    "name": "param_type_name",
                    "params": {
                        "nested_param1_name": CloudSpecParam,
                        "nested_param2_name": CloudSpecParam,
                        ...
                    }
                },
            }
        }
    """

    def __init__(
        self,
        name: str,
        required: bool,
        target: str,
        target_type: str,
        member: dataclasses.make_dataclass(
            cls_name="CloudSpecMember",
            fields=[("name", str), ("params", Dict[str, "CloudSpecParam"])],
        ) = None,
        param_type: str = None,
        doc: str = "",
        default: Any = None,
        snaked: str = None,
    ):
        """
        Args:
            name: Name of the parameter
            doc: Docstring for the parameter
            required: "True|False"
            target: "query|data|path|sdk-class|sdk-subclass|function-call"
            target_type: "mapping|format_str|arg|kwargs"
            param_type: A type hint for this parameter
            member: Nested member params
            default: The default value for this parameter if it is not required
            snaked: Snake case representation of the parameter name to be used, would override generated one
        """
        # If the target_type is "mapping" the target is the name of a dictionary variable
        # If the target_type is "arg" or "kwargs" the target is the name of callable this param should forwarded to
        # If the target_type is "value" then it is directly dropped in and it is included in the function parameters
        if target_type not in ("mapping", "value", "arg", "kwargs"):
            raise TypeError(f"Invalid target type: {target_type}")

        hub = create_hub()

        if member and member.get("params", None):
            validated_member_params = {
                name: CloudSpecParam(name=name, **param_spec)
                for name, param_spec in member.get("params").items()
            }
            member = {"name": member.get("name"), "params": validated_member_params}
        else:
            member = None

        if not snaked:
            # Snake case the parameter every time
            snaked = hub.tool.format.case.snake(name)
            # Add an underscore to the parameter name if it shadows a builtin
            unclashed_name = hub.tool.format.keyword.unclash(snaked) or snaked
            snaked = unclashed_name.replace(" ", "_").replace("-", "_").strip(". ")

        super().__init__(
            doc=doc,
            snaked=snaked,
            param_type=param_type,
            required=required,
            default=default,
            target_type=target_type,
            member=member,
            target=target,
        )
