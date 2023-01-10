import re
from enum import Enum
from typing import Any, Dict

import pydantic
import sympy

from classiq.interface.generator.arith.arithmetic import (
    FORBIDDEN_LITERALS,
    SUPPORTED_FUNC_NAMES,
    SUPPORTED_VAR_NAMES_REG,
)
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import FunctionParams
from classiq.interface.helpers.custom_pydantic_types import PydanticExpressionStr

AMPLITUDE_IO_NAME = "AMPLITUDE"
TARGET_OUTPUT_NAME = "TARGET"


class AmplitudeLoadingImplementation(str, Enum):
    EXPERIMENTAL = "EXPERIMENTAL"
    NAIVE = "NAIVE"
    GRAYCODE = "GRAYCODE"


class AmplitudeLoading(FunctionParams):
    size: pydantic.PositiveInt = pydantic.Field(
        description="The number of qubits of the amplitude input."
    )
    expression: PydanticExpressionStr = pydantic.Field(
        description="The mathematical expression of the amplitude loading function."
    )
    implementation: AmplitudeLoadingImplementation = pydantic.Field(
        default=AmplitudeLoadingImplementation.EXPERIMENTAL,
        description="Implementation options.",
    )

    @pydantic.validator("expression", pre=True)
    def validate_coefficient(cls, expression: str) -> str:
        if isinstance(expression, str):
            sympy.parse_expr(expression)

        if isinstance(expression, sympy.Expr):
            return str(expression)
        return expression

    @pydantic.root_validator()
    def check_all_variable_are_defined(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        expression = values.get("expression", "")
        literals = set(re.findall(SUPPORTED_VAR_NAMES_REG, expression))

        not_allowed = literals.intersection(FORBIDDEN_LITERALS)
        variables = literals.difference(SUPPORTED_FUNC_NAMES)
        if not_allowed:
            raise ValueError(f"The following names: {not_allowed} are not allowed")

        if len(variables) != 1:
            raise ValueError(f"{variables} must contain exactly single variable")
        return values

    def _create_ios(self) -> None:
        self._inputs = {
            AMPLITUDE_IO_NAME: RegisterUserInput(
                name=AMPLITUDE_IO_NAME, size=self.size
            ),
        }
        self._outputs = {
            TARGET_OUTPUT_NAME: RegisterUserInput(name=TARGET_OUTPUT_NAME, size=1),
            **self._inputs,
        }
        self._create_zero_input_registers({TARGET_OUTPUT_NAME: 1})

    @property
    def variable(self) -> str:
        literals = set(re.findall(SUPPORTED_VAR_NAMES_REG, self.expression))
        return list(literals.difference(SUPPORTED_FUNC_NAMES))[0]
