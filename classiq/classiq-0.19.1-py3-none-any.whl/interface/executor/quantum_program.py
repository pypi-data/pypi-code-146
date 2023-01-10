from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import pydantic
from pydantic import BaseModel

from classiq.interface.backend.ionq import ionq_quantum_program
from classiq.interface.backend.pydantic_backend import PydanticArgumentNameType
from classiq.interface.executor.quantum_instruction_set import QuantumInstructionSet
from classiq.interface.executor.register_initialization import RegisterInitialization

Arguments = Dict[PydanticArgumentNameType, Any]
MultipleArguments = Tuple[Arguments, ...]
CodeType = Union[str, ionq_quantum_program.IonqQuantumCircuit]
RegistersInitialization = Dict[str, RegisterInitialization]


class QuantumBaseProgram(BaseModel):
    syntax: QuantumInstructionSet = pydantic.Field(
        default=QuantumInstructionSet.QASM, description="The syntax of the program."
    )
    code: CodeType = pydantic.Field(
        ..., description="The textual representation of the program"
    )

    @pydantic.validator("code")
    def load_quantum_program(cls, code: CodeType, values: Dict[str, Any]) -> CodeType:
        if not isinstance(code, str):
            return code

        syntax = values.get("syntax")
        if syntax == QuantumInstructionSet.IONQ:
            return ionq_quantum_program.IonqQuantumCircuit.from_string(code)
        return code


class QuantumProgram(QuantumBaseProgram):
    arguments: MultipleArguments = pydantic.Field(
        default=(),
        description="The parameters dictionary for a parametrized quantum program.",
    )
    output_qubits_map: Dict[str, Tuple[int, ...]] = pydantic.Field(
        default_factory=dict,
        description="The map of outputs to their qubits in the circuit.",
    )
    registers_initialization: Optional[RegistersInitialization] = pydantic.Field(
        default_factory=None,
        description="Initial conditions for the different registers in the circuit.",
    )

    @pydantic.validator("arguments")
    def validate_arguments(cls, arguments: MultipleArguments, values: Dict[str, Any]):
        if arguments and values.get("syntax") not in (
            QuantumInstructionSet.QSHARP,
            QuantumInstructionSet.QASM,
        ):
            raise ValueError("Only QASM or Q# programs support arguments")

        if values.get("syntax") == QuantumInstructionSet.QSHARP and len(arguments) > 1:
            raise ValueError(
                f"Q# programs supports only one group of arguments. {len(arguments)} given"
            )

        return arguments

    @staticmethod
    def from_file(
        file_path: Union[str, Path],
        syntax: Optional[Union[str, QuantumInstructionSet]] = None,
        arguments: MultipleArguments = (),
    ) -> QuantumProgram:
        path = Path(file_path)
        code = path.read_text()
        if syntax is None:
            syntax = path.suffix.lstrip(".")
        return QuantumProgram(syntax=syntax, code=code, arguments=arguments)
