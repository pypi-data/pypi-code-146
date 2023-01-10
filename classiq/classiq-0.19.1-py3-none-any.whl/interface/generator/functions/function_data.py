import abc
from typing import Set

import pydantic

from classiq.interface.generator.function_params import ArithmeticIODict, IOName
from classiq.interface.helpers.custom_pydantic_types import PydanticFunctionNameStr


class FunctionData(pydantic.BaseModel, abc.ABC):
    """
    Facilitates the creation of a user-defined custom function
    """

    name: PydanticFunctionNameStr = pydantic.Field(
        description="The name of a custom function"
    )

    @property
    @abc.abstractmethod
    def input_set(self) -> Set[IOName]:
        pass

    @property
    @abc.abstractmethod
    def output_set(self) -> Set[IOName]:
        pass

    @property
    @abc.abstractmethod
    def inputs(self) -> ArithmeticIODict:
        pass

    @property
    @abc.abstractmethod
    def outputs(self) -> ArithmeticIODict:
        pass

    @pydantic.validator("name")
    def validate_name(cls, name: str):
        validate_name_end_not_newline(name=name)
        return name


def validate_name_end_not_newline(name: str):
    _new_line = "\n"
    if name.endswith(_new_line):
        raise ValueError("Function name cannot end in a newline character")
