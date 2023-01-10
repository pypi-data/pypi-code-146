from __future__ import annotations

import itertools
from typing import Any, Dict, Iterable, List, Tuple

import pydantic

from classiq.interface.generator.functions.register import Register, get_register_names

from classiq.quantum_register import RegisterRole as Role

REGISTER_NOT_FOUND_ERROR = "Register name not found"


class RegisterMappingData(pydantic.BaseModel):
    input_registers: List[Register] = pydantic.Field(default_factory=list)
    output_registers: List[Register] = pydantic.Field(default_factory=list)
    zero_input_registers: List[Register] = pydantic.Field(default_factory=list)

    @pydantic.root_validator()
    def validate_mapping(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        input_registers = values.get("input_registers", list())
        output_registers = values.get("output_registers", list())
        zero_input_registers = values.get("zero_input_registers", list())

        input_qubits = cls._get_qubit_range(input_registers)
        output_qubits = cls._get_qubit_range(output_registers)
        zero_input_qubits = cls._get_qubit_range(zero_input_registers)

        all_input_qubits = sorted(input_qubits + zero_input_qubits)
        if not cls._validate_no_overlap(all_input_qubits):
            raise ValueError("overlapping input qubits are not allowed")
        if not cls._validate_no_overlap(output_qubits):
            raise ValueError("overlapping output qubits are not allowed")

        if not output_qubits == all_input_qubits:
            raise ValueError(
                "output registers should be included within the input / zero input registers"
            )

        return values

    @pydantic.validator("input_registers", "output_registers")
    def validate_input_registers_are_distinct(cls, field_value: List[Register]):
        if len(field_value) != len({io_register.name for io_register in field_value}):
            raise ValueError("The names of IO registers must be distinct.")
        return field_value

    @staticmethod
    def _validate_no_overlap(reg_list: List[int]) -> bool:
        return len(reg_list) == len(set(reg_list))

    @staticmethod
    def _get_qubit_range(registers: Iterable[Register]) -> List[int]:
        return sorted(
            list(itertools.chain.from_iterable(reg.qubits for reg in registers))
        )

    @property
    def input_names(self) -> Iterable[str]:
        return get_register_names(self.input_registers)

    @property
    def output_names(self) -> Iterable[str]:
        return get_register_names(self.output_registers)

    def validate_equal_mappings(self, other: RegisterMappingData):
        if any(
            [
                self.input_registers != other.input_registers,
                self.output_registers != other.output_registers,
                self.zero_input_registers != other.zero_input_registers,
            ]
        ):
            raise ValueError("Interface should be identical in all implementations")

    def get_input_register(self, name) -> Register:
        for reg in self.input_registers:
            if reg.name == name:
                return reg
        raise ValueError(REGISTER_NOT_FOUND_ERROR)

    def get_output_register(self, name) -> Register:
        for reg in self.output_registers:
            if reg.name == name:
                return reg
        raise ValueError(REGISTER_NOT_FOUND_ERROR)

    @staticmethod
    def from_registers_dict(
        regs_dict: Dict[Role, Tuple[Register, ...]]
    ) -> RegisterMappingData:
        return RegisterMappingData(
            input_registers=list(regs_dict[Role.INPUT]),
            output_registers=list(regs_dict[Role.OUTPUT]),
            zero_input_registers=list(regs_dict[Role.ZERO]),
        )

    class Config:
        extra = "forbid"
