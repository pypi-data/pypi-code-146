from dataclass_to_diagram.models.c4.base import BaseComponent

from .args_dict_to_str import args_dict_to_str
from .base_element_to_puml import base_element_to_puml


def component_to_puml(
    context: BaseComponent,
) -> str:
    args = base_element_to_puml(context)
    args_str = args_dict_to_str(args)
    return "{class_name}({args})".format(
        class_name=context.class_name_str,
        args=args_str,
    )
