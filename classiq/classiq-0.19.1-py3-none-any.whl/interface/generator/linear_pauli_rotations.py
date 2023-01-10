from typing import TYPE_CHECKING, Any, Dict, List

import pydantic

from classiq.interface.generator import function_params
from classiq.interface.generator.arith.register_user_input import RegisterUserInput

STATE = "state"
TARGET = "target"

LENGTH_ERROR_MESSAGE = "Slopes, offsets and basis values must have the same length"

if TYPE_CHECKING:
    PydanticPauliBasisStr = str
else:
    PydanticPauliBasisStr = pydantic.constr(
        to_lower=True,
        regex=r"[xyz]",
    )


class LinearPauliRotations(function_params.FunctionParams):
    """
    Perform independent linear rotations on target qubits, each controlled by an identical
    n-qubit state register |x>.

    Each target qubit, indexed with k and denoted by q_k, undergoes the following transformation:
    |x>|q_k> -> |x> * [cos(theta(x,k)/2) + i*sin(theta(x,k)/2)*sigma]|q_k>
    with sigma being 'X', 'Y' or 'Z' Pauli matrix, and the angle is a linear function of the state,
    theta(x,k)/2 = (slope(k)*x + offset(k))/2.

    For example, a 'Y' rotation on one target qubit will result in a circuit implementing the following logic:
    |x>|0> -> cos((slope*x + offset)/2)|x>|0> + sin((slope*x + offset)/2)|x>|1>

            q_0: ─────────────────────────■───────── ... ──────────────────────
                                          │
                                          .
                                          │
        q_(n-1): ─────────────────────────┼───────── ... ───────────■──────────
                  ┌────────────┐  ┌───────┴───────┐       ┌─────────┴─────────┐
         target: ─┤ RY(offset) ├──┤ RY(2^0 slope) ├  ...  ┤ RY(2^(n-1) slope) ├
                  └────────────┘  └───────────────┘       └───────────────────┘
    """

    num_state_qubits: pydantic.PositiveInt = pydantic.Field(
        description="The number of input qubits"
    )
    bases: List[PydanticPauliBasisStr] = pydantic.Field(
        description="The types of Pauli rotations ('X', 'Y', 'Z')."
    )
    slopes: List[float] = pydantic.Field(
        description="The slopes of the controlled rotations."
    )
    offsets: List[float] = pydantic.Field(
        description="The offsets of the controlled rotations."
    )

    @pydantic.validator("bases", "slopes", "offsets", pre=True, always=True)
    def as_list(cls, v):
        if not isinstance(v, list):
            v = [v]
        return v

    @pydantic.root_validator()
    def validate_lists(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        offsets = values.get("offsets", list())
        bases = values.get("bases", list())
        slopes = values.get("slopes", list())
        if len(slopes) == len(offsets) and len(offsets) == len(bases):
            return values
        raise ValueError(LENGTH_ERROR_MESSAGE)

    def _create_ios(self) -> None:
        self._inputs = {
            STATE: RegisterUserInput(name=STATE, size=self.num_state_qubits),
            TARGET: RegisterUserInput(name=TARGET, size=len(self.bases)),
        }
        self._outputs = {**self.inputs}
