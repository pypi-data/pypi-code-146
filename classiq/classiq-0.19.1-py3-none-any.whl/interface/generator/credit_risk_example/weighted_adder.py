from typing import List

import numpy as np
import pydantic

from classiq.interface.generator import function_params
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import DEFAULT_ZERO_NAME

LENGTH_ERROR_MESSAGE = "Input length error: Length of weights vector has to be identical to the number of input qubits"
STATE = "state"
SUM = "sum"


class PydanticStrictNonNegativeInteger(pydantic.ConstrainedInt):
    strict = True
    ge = 0


class WeightedAdder(function_params.FunctionParams):
    """
    Creates a circuit implementing a scalar product between an n-qubit state |q1,q2,...,qn> and an n-length non-negative
    integer vector (w1,w2,...wn), such that the result of the output register is |q1*w1+q2*w2+...qn*wn>.
    If no weights are provided, they are default to 1 for every qubit.
    """

    num_state_qubits: pydantic.PositiveInt = pydantic.Field(
        description="The number of input qubits"
    )
    weights: List[PydanticStrictNonNegativeInteger] = pydantic.Field(
        default=None,
        description="List of non-negative integers corresponding to the weight of each qubit",
    )

    @pydantic.validator("weights", always=True, pre=True)
    def validate_weights(cls, weights, values):
        num_state_qubits = values.get("num_state_qubits")
        if weights is None:
            return [1] * num_state_qubits
        if len(weights) != num_state_qubits:
            raise ValueError(LENGTH_ERROR_MESSAGE)
        return weights

    def num_sum_qubits(self) -> int:
        sum_weights = np.sum(self.weights)
        if sum_weights > 0:
            return 1 + int(np.floor(np.log2(sum_weights)))
        return 1

    def _create_ios(self) -> None:
        self._inputs = {
            STATE: RegisterUserInput(name=STATE, size=self.num_state_qubits)
        }
        zero_input_name = f"{DEFAULT_ZERO_NAME}_{SUM}"
        self._create_zero_input_registers({zero_input_name: self.num_sum_qubits()})
        self._outputs = {
            **self._inputs,
            SUM: RegisterUserInput(name=SUM, size=self.num_sum_qubits()),
        }
