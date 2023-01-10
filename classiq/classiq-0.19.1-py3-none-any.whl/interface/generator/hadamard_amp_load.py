from typing import List

import pydantic

from classiq.interface.generator import function_params
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.complex_type import Complex
from classiq.interface.generator.validations.validator_functions import (
    validate_amplitudes,
)

OUTPUT_STATE = "OUTPUT_STATE"
EXTRA_QUBITS = "EXTRA_QUBITS"


class HadamardAmpLoad(function_params.FunctionParams):
    """
    loads a amplitudes vector using hadamard decomposition
    """

    num_qubits: pydantic.PositiveInt = pydantic.Field(
        description="The number of qubits in the circuit."
    )
    amplitudes: List[Complex] = pydantic.Field(description="amplitudes vector to load")

    cutoff: pydantic.PositiveInt = pydantic.Field(
        description="The number of hadamard coefficients to keep. "
        "The largest cutoff_num coefficients are used to load the amplitudes"
    )

    _validate_amplitudes = pydantic.validator("amplitudes", allow_reuse=True)(
        validate_amplitudes
    )

    @pydantic.root_validator()
    def cutoff_validator(cls, values):
        amp = values.get("amplitudes")
        cutoff = values.get("cutoff")
        if cutoff > len(amp):
            raise ValueError(
                "cutoff number should be smaller or equal to the length of the amplitudes vector "
            )
        return values

    @property
    def state_qubits_num(self) -> int:
        return len(self.amplitudes).bit_length() - 1

    @property
    def has_extra_qubits(self) -> bool:
        return self.num_qubits > self.state_qubits_num

    def _create_ios(self) -> None:
        self._inputs = dict()
        self._outputs = {
            OUTPUT_STATE: RegisterUserInput(
                name=OUTPUT_STATE, size=self.state_qubits_num
            )
        }
        if self.has_extra_qubits:
            num_extra_qubits = self.num_qubits - self.state_qubits_num
            self._outputs[EXTRA_QUBITS] = RegisterUserInput(
                name=EXTRA_QUBITS, size=num_extra_qubits
            )
