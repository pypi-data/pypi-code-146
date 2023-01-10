from typing import Dict, List, Optional, Union

import pydantic
from pydantic import BaseModel

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.synthesis_metadata.solution_metadata import (
    SolutionMetadata,
)

from classiq.quantum_register import RegisterRole

ParameterName = str


class GeneratedRegister(BaseModel):
    name: str

    role: RegisterRole
    register_type: Optional[RegisterUserInput]

    qubit_indexes_relative: List[int]
    qubit_indexes_absolute: List[int] = list()

    def __len__(self) -> int:
        return self.qubit_indexes_relative.__len__()

    @property
    def width(self) -> int:
        return len(self)


class GeneratedFunction(BaseModel):
    name: str
    registers: List[GeneratedRegister] = list()
    depth: Optional[int]
    width: Optional[int]
    released_auxiliary_qubits: List[int] = list()
    dangling_inputs: List[str]

    def __getitem__(self, key: Union[int, str]) -> GeneratedRegister:
        if type(key) is int:
            return self.registers[key]
        if type(key) is str:
            for register in self.registers:
                if key == register.name:
                    return register
        raise KeyError(key)


class SynthesisMetrics(BaseModel):
    solution_metadata: SolutionMetadata
    generated_functions: List[GeneratedFunction] = pydantic.Field(default_factory=list)
    _function_mapping: Dict[Union[int, str], GeneratedFunction] = pydantic.PrivateAttr(
        default_factory=dict
    )
    circuit_parameters: List[ParameterName] = pydantic.Field(default_factory=list)
    width: Optional[int] = pydantic.Field(default=None)

    def _fill_function_mapping(self) -> None:
        if self._function_mapping:
            return
        for idx, fm in enumerate(self.generated_functions):
            self._function_mapping[idx] = fm
            self._function_mapping[fm.name] = fm

    def __getitem__(self, key: Union[int, str]) -> GeneratedFunction:
        self._fill_function_mapping()
        if key not in self._function_mapping:
            raise KeyError(f"No function named {key}")
        return self._function_mapping[key]

    def __len__(self) -> int:
        return self.generated_functions.__len__()

    def __iter__(self):
        topological_sort = self.solution_metadata.topological_sort
        if not topological_sort:
            return
        yield from (self[function_name] for function_name in topological_sort)

    def pprint(self) -> None:
        print("Circuit Synthesis Metrics")
        if self.solution_metadata.step_durations is not None:
            print(
                f"    Generation took {self.solution_metadata.step_durations.total_time()} seconds"
            )
        if self.solution_metadata.failure_reason:
            print("Generation failed :(")
            print(f"Failure reason: {self.solution_metadata.failure_reason}")
            return
        print(f"The circuit has {len(self.generated_functions)} functions:")
        for index, fm in enumerate(self.generated_functions):
            print(f"{index}) {fm.name}")
            print(
                f"  depth: {fm.depth} ; "
                f"width: {fm.width} ; "
                f"registers: {len(fm.registers)}"
            )
            for reg_index, register in enumerate(fm.registers):
                print(
                    f"  {reg_index}) {register.role.value} - {register.name} ; "
                    f"qubits: {register.qubit_indexes_absolute}"
                )
