from typing import List

import pydantic

from classiq.interface.generator import function_params
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.complex_type import Complex
from classiq.interface.generator.validations.validator_functions import (
    validate_amplitudes,
)

OUTPUT_STATE = "OUTPUT_STATE"


class SparseAmpLoad(function_params.FunctionParams):
    """
    loads a sparse amplitudes vector
    """

    num_qubits: pydantic.PositiveInt = pydantic.Field(
        description="The number of qubits in the circuit."
    )
    amplitudes: List[Complex] = pydantic.Field(description="amplitudes vector to load")

    _validate_amplitudes = pydantic.validator("amplitudes", allow_reuse=True)(
        validate_amplitudes
    )

    @property
    def state_qubits_num(self) -> int:
        return len(self.amplitudes).bit_length() - 1

    def _create_ios(self) -> None:
        self._inputs = {}
        self._outputs = {
            OUTPUT_STATE: RegisterUserInput(
                name=OUTPUT_STATE, size=self.state_qubits_num
            )
        }
