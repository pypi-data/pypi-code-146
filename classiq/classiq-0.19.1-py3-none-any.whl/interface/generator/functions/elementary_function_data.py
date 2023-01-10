from typing import Any, Dict, List, Optional, Set, Tuple, Union

import pydantic

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import ArithmeticIODict, IOName
from classiq.interface.generator.functions.function_data import FunctionData
from classiq.interface.generator.functions.function_implementation import (
    FunctionImplementation,
)
from classiq.interface.generator.functions.register import Register
from classiq.interface.generator.functions.register_mapping_data import (
    RegisterMappingData,
)

ImplementationsType = Union[Tuple[FunctionImplementation, ...], FunctionImplementation]


class ElementaryFunctionData(FunctionData, extra=pydantic.Extra.forbid):
    """
    Facilitates the creation of a user-defined elementary function

    This class sets extra to forbid so that it can be used in a Union and not "steal"
    objects from other classes.
    """

    register_mapping: RegisterMappingData = pydantic.Field(
        default_factory=RegisterMappingData,
        description="The IO data that is common to all implementations of the function",
    )
    implementations: Optional[ImplementationsType] = pydantic.Field(
        description="The implementations of the custom function",
    )

    @pydantic.validator("register_mapping")
    def validate_register_mapping(
        cls, register_mapping: RegisterMappingData
    ) -> RegisterMappingData:
        if not register_mapping.output_registers:
            raise ValueError("The outputs of a custom function must be non-empty")
        return register_mapping

    @pydantic.validator("implementations")
    def validate_implementations(
        cls, implementations: Optional[ImplementationsType], values: Dict[str, Any]
    ) -> Optional[ImplementationsType]:
        if not implementations:
            raise ValueError(
                "The implementations of a custom function must be non-empty."
            )

        if isinstance(implementations, FunctionImplementation):
            implementations = (implementations,)

        register_mapping = values.get("register_mapping")
        assert isinstance(register_mapping, RegisterMappingData)
        for impl in implementations:
            impl.validate_ranges_of_all_registers(register_mapping=register_mapping)

        return implementations

    @property
    def input_set(self) -> Set[IOName]:
        return set(self.register_mapping.input_names)

    @property
    def output_set(self) -> Set[IOName]:
        return set(self.register_mapping.output_names)

    @property
    def inputs(self) -> ArithmeticIODict:
        return _map_reg_user_input(self.register_mapping.input_registers)

    @property
    def outputs(self) -> ArithmeticIODict:
        return _map_reg_user_input(self.register_mapping.output_registers)


def _map_reg_user_input(registers: List[Register]) -> ArithmeticIODict:
    return {
        reg.name: RegisterUserInput(size=len(reg.qubits), name=reg.name)
        for reg in registers
    }
