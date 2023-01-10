from itertools import chain
from typing import Optional, Tuple, Union

import pydantic
from pydantic import BaseModel

from classiq.interface.generator.functions.register import Register
from classiq.interface.generator.functions.register_mapping_data import (
    RegisterMappingData,
)
from classiq.interface.helpers.custom_pydantic_types import PydanticNonEmptyString

RegistersStrictType = Tuple[Register, ...]
RegistersType = Union[Register, RegistersStrictType]


def to_tuple(reg_type: RegistersType) -> RegistersStrictType:
    if isinstance(reg_type, Register):
        return (reg_type,)
    else:
        return reg_type


class FunctionImplementation(BaseModel):
    """
    Facilitates the creation of a user-defined custom function implementation
    """

    class Config:
        validate_all = True
        extra = "forbid"

    name: Optional[PydanticNonEmptyString] = pydantic.Field(
        default=None,
        description="The name of the custom implementation",
    )

    serialized_circuit: PydanticNonEmptyString = pydantic.Field(
        description="The QASM code of the custom function implementation",
    )

    auxiliary_registers: RegistersStrictType = pydantic.Field(
        default_factory=tuple,
        description="A tuple of auxiliary registers to the custom implementation",
    )

    def num_qubits_in_all_registers(self, register_mapping: RegisterMappingData) -> int:
        all_input_registers = (
            register_mapping.input_registers
            + register_mapping.zero_input_registers
            + list(self.auxiliary_registers)
        )
        input_qubits = set(
            chain.from_iterable(register.qubits for register in all_input_registers)
        )
        return len(input_qubits)

    @pydantic.validator(
        "auxiliary_registers",
        pre=True,
        always=True,
    )
    def validate_all_registers_are_tuples(
        cls,
        registers: RegistersType,
    ) -> RegistersStrictType:
        if isinstance(registers, Register):
            return (registers,)
        return registers

    def validate_ranges_of_all_registers(
        self, register_mapping: RegisterMappingData
    ) -> None:
        input_registers = register_mapping.input_registers
        output_registers = register_mapping.output_registers
        zero_input_registers = register_mapping.zero_input_registers
        auxiliary_registers = list(self.auxiliary_registers)

        all_input_registers = (
            input_registers + zero_input_registers + auxiliary_registers
        )
        input_qubits = set(
            chain.from_iterable(register.qubits for register in all_input_registers)
        )
        num_qubits = len(input_qubits)
        all_qubits = set(range(num_qubits))
        if num_qubits != sum(register.width for register in all_input_registers):
            raise ValueError("The input registers must not overlap.")
        if input_qubits != all_qubits:
            raise ValueError(
                "The set of qubits contained in all registers must be consecutive."
            )

        all_output_registers = output_registers + auxiliary_registers
        output_qubits = set(
            chain.from_iterable(register.qubits for register in all_output_registers)
        )
        if len(output_qubits) != sum(
            register.width for register in all_output_registers
        ):
            raise ValueError("The output registers must not overlap.")
        if not output_qubits == all_qubits:
            raise ValueError("The input and output qubits must be mutually consistent.")
