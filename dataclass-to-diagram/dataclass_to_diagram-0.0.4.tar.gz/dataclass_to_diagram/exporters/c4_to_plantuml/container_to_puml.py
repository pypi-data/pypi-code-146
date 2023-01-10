from typing import Final
from dataclass_to_diagram.models.c4.container.containter import (
    BaseContainer,
)

from .args_dict_to_str import args_dict_to_str
from .base_element_to_puml import base_element_to_puml
from .component_to_puml import component_to_puml

TEMPLATE: Final[str] = "{class_name}({args}){components}"


def container_to_puml(
    context: BaseContainer,
) -> str:
    args = base_element_to_puml(context)
    args_str = args_dict_to_str(args)
    if context.components:
        components_list: list[str] = []
        for component in context.components:
            components_list.append(component_to_puml(component))
        components_list_joined: str = "\n".join(components_list)
        components = "\n{0}".format(components_list_joined)
        components = components.replace("\n", "\n    ")
        components = " {{{0}\n}}".format(components)
    else:
        components = ""

    return TEMPLATE.format(
        class_name=context.class_name_str,
        args=args_str,
        components=components,
    )
