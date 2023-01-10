from typing import Collection, Dict, Iterator, List

from classiq.interface.executor.register_initialization import Number
from classiq.interface.generator.synthesis_metrics import (
    GeneratedFunction,
    GeneratedRegister,
)

from classiq.exceptions import ClassiqStateInitializationError

RegisterName = str
InitialConditions = Dict[RegisterName, Number]


def get_registers_from_generated_functions(
    generated_functions: List[GeneratedFunction],
    register_names: Collection[RegisterName],
) -> List[GeneratedRegister]:
    registers: List[GeneratedRegister] = list()
    remain_register = list(register_names)

    for register in _relevant_registers(
        generated_functions=generated_functions, remain_register=remain_register
    ):
        registers.append(register)
        remain_register.remove(register.name)
        if not remain_register:
            return registers

    raise ClassiqStateInitializationError(
        f"The circuit doesn't contain registers that match: {', '.join(remain_register)}."
    )


def _relevant_registers(
    generated_functions: List[GeneratedFunction], remain_register: List[RegisterName]
) -> Iterator[GeneratedRegister]:
    return iter(
        register
        for function in generated_functions
        for register in function.registers
        if register.name in remain_register
    )
