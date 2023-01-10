from typing import Any, Dict, Tuple, Union

import pydantic
from pydantic import BaseModel

from classiq.interface.generator.functions import (
    CompositeFunctionData,
    ElementaryFunctionData,
)
from classiq.interface.generator.functions.function_data import (
    FunctionData,
    validate_name_end_not_newline,
)
from classiq.interface.generator.user_defined_function_params import CustomFunction
from classiq.interface.helpers.custom_pydantic_types import PydanticFunctionNameStr

DEFAULT_FUNCTION_LIBRARY_NAME = "default_function_library_name"


# We need to define ConcreteFunctionData so pydantic will know
# what class to use when deserializing from object (pydantic attempts to
# parse as each of the classes in the Union, in order).
ConcreteFunctionData = Union[ElementaryFunctionData, CompositeFunctionData]


class FunctionLibraryData(BaseModel):
    """Facility to store user-defined custom functions."""

    name: PydanticFunctionNameStr = pydantic.Field(
        default=DEFAULT_FUNCTION_LIBRARY_NAME,
        description="The name of the custom function library",
    )

    function_dict: Dict[str, ConcreteFunctionData] = pydantic.Field(
        default_factory=dict,
        description="A dictionary containing the custom functions in the library.",
    )

    functions: Tuple[ConcreteFunctionData, ...] = pydantic.Field(
        default=tuple(),
        description="A tuple for inputting custom functions to the library.",
    )

    @pydantic.validator("name")
    def validate_name(cls, name: str) -> str:
        validate_name_end_not_newline(name=name)
        return name

    @pydantic.validator("function_dict")
    def validate_function_dict(
        cls, function_dict: Dict[str, FunctionData]
    ) -> Dict[str, FunctionData]:
        if not all(
            function_data.name == name for name, function_data in function_dict.items()
        ):
            raise AssertionError("Bad function_dict encountered.")
        return function_dict

    @pydantic.validator("functions")
    def validate_functions(
        cls, functions: Tuple[FunctionData, ...], values
    ) -> Tuple[FunctionData, ...]:
        if not functions:
            return tuple()
        if values.get("function_dict"):
            raise ValueError("Expected only a single function data input field")
        values["function_dict"] = {
            function_data.name: function_data for function_data in functions
        }
        return tuple()

    def __contains__(self, obj: Any) -> bool:
        if isinstance(obj, str):
            return obj in self.function_dict
        elif isinstance(obj, CustomFunction):
            return obj.name in self.function_dict
        elif isinstance(obj, FunctionData):
            return obj in self.function_dict.values()
        else:
            return False
