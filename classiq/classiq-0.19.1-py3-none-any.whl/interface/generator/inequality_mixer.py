from typing import Iterable, Union

import pydantic
import sympy

from classiq.interface.generator import function_params
from classiq.interface.generator.arith.fix_point_number import FixPointNumber
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.parameters import ParameterFloatType

DATA_REG_INPUT_NAME = "data_reg_input"
BOUND_REG_INPUT_NAME = "bound_reg_input"

DATA_REG_OUTPUT_NAME = "data_reg_output"
BOUND_REG_OUTPUT_NAME = "bound_reg_output"


class InequalityMixer(function_params.FunctionParams):
    """
    Mixing a  fixed point number variable below a given upper bound or above a given
    lower bound. i.e. after applying this function the variable will hold a
    superposition position of all the valid values.
    """

    data_reg_input: RegisterUserInput = pydantic.Field(
        description="The input variable to mix."
    )

    bound_reg_input: Union[RegisterUserInput, FixPointNumber] = pydantic.Field(
        description="Fixed number or variable that defined the upper or lower bound for"
        " the mixing operation. In case of a fixed number bound, the value"
        " must be positive."
    )

    mixer_parameter: ParameterFloatType = pydantic.Field(
        description="The parameter used for rotation gates in the mixer."
    )

    is_less_inequality: bool = pydantic.Field(
        default=True,
        description="Whether to mix below or above a certain bound."
        "Less inequality mixes between 0 and the given bound."
        "Greater inequality mixes between the bound and the maximal number allowed by"
        " the number of qubits (i.e 2^n - 1).",
    )

    @pydantic.validator("mixer_parameter", pre=True)
    def validate_parameter(cls, parameter):
        if isinstance(parameter, str):
            # We only check that this method does not raise any exception to see that it can be converted to sympy
            sympy.parse_expr(parameter)

        if isinstance(parameter, sympy.Expr):
            return str(parameter)
        return parameter

    @staticmethod
    def _create_bit_names(base_name: str, num_bits: int) -> Iterable[str]:
        return (f"{base_name}_{i}" for i in range(num_bits))

    def _create_ios(self) -> None:

        input_names = self._create_bit_names(
            DATA_REG_INPUT_NAME, self.data_reg_input.size
        )
        output_names = self._create_bit_names(
            DATA_REG_OUTPUT_NAME, self.data_reg_input.size
        )
        self._inputs = {
            name: RegisterUserInput(name=name, size=1) for name in input_names
        }
        self._outputs = {
            name: RegisterUserInput(name=name, size=1) for name in output_names
        }

        if isinstance(self.bound_reg_input, RegisterUserInput):
            input_names = self._create_bit_names(
                BOUND_REG_INPUT_NAME, self.bound_reg_input.size
            )
            output_names = self._create_bit_names(
                BOUND_REG_OUTPUT_NAME, self.bound_reg_input.size
            )
            self._inputs.update(
                {name: RegisterUserInput(name=name, size=1) for name in input_names}
            )
            self._outputs.update(
                {name: RegisterUserInput(name=name, size=1) for name in output_names}
            )
