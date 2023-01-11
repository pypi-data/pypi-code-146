from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Optional,
    Sequence,
    Union,
)

from platon.exceptions import (
    ValidationError,
)

if TYPE_CHECKING:
    from platon import Web3
    from platon.module import Module


def attach_modules(
    parent_module: Union["Web3", "Module"],
    module_definitions: Dict[str, Sequence[Any]],
    w3: Optional[Union["Web3", "Module"]] = None
) -> None:
    for module_name, module_info in module_definitions.items():
        module_class = module_info[0]

        if hasattr(parent_module, module_name):
            raise AttributeError(
                f"Cannot set {parent_module} module named '{module_name}'.  The platon object "
                "already has an attribute with that name"
            )

        if w3 is None:
            setattr(parent_module, module_name, module_class(parent_module))
            w3 = parent_module
        else:
            setattr(parent_module, module_name, module_class(w3))

        if len(module_info) == 2:
            submodule_definitions = module_info[1]
            module = getattr(parent_module, module_name)
            attach_modules(module, submodule_definitions, w3)
        elif len(module_info) != 1:
            raise ValidationError("Module definitions can only have 1 or 2 elements.")
