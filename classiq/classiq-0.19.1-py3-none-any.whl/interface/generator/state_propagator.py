from typing import List

import numpy as np
import pydantic

from classiq.interface.generator import function_params
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.complex_type import Complex
from classiq.interface.generator.function_params import (
    DEFAULT_INPUT_NAME,
    DEFAULT_OUTPUT_NAME,
)


class StatePropagator(function_params.FunctionParams):
    """
    Creates a quantum circuit that propagates the start state vector to the end state vector,
    both are assumed to be pure states.
    The default start state vector is |000...0>.
    """

    end_state_vector: List[Complex] = pydantic.Field(
        description="The desired state vector at the end of the operator."
        " Must be of size 2**num_qubits. Does not have to be "
        "normalized"
    )

    start_state_vector: List[Complex] = pydantic.Field(
        default_factory=list,
        description="The  state vector at the input of the operator."
        " Must be of size 2**num_qubits. Does not have to be"
        " normalized",
    )

    @pydantic.validator("start_state_vector", always=True)
    def validate_start_state(cls, start_state_vector, values):
        end_state_vector = values.get("end_state_vector")
        num_qubits = cls._num_qubits(end_state_vector)
        if len(start_state_vector) == 0:
            default_start_state_vector = [0.0 for _ in range(2**num_qubits)]
            default_start_state_vector[0] = 1.0
            start_state_vector = default_start_state_vector

        if len(start_state_vector) != len(end_state_vector):
            raise ValueError("Start and end state vectors are of non-equal length")

        return start_state_vector

    @staticmethod
    def _num_qubits(vector: List[Complex]) -> int:
        return int(np.log2(len(vector)))

    def _create_ios(self) -> None:
        self._inputs = {
            DEFAULT_INPUT_NAME: RegisterUserInput(
                name=DEFAULT_INPUT_NAME, size=self._num_qubits(self.start_state_vector)
            )
        }
        self._outputs = {
            DEFAULT_OUTPUT_NAME: RegisterUserInput(
                name=DEFAULT_OUTPUT_NAME, size=self._num_qubits(self.end_state_vector)
            )
        }
