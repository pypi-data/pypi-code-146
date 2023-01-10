from typing import Any, Dict, Optional, Tuple

import pydantic

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.exponentiation import Exponentiation
from classiq.interface.generator.function_param_list_without_self_reference import (
    function_param_library_without_self_reference,
)
from classiq.interface.generator.function_params import (
    DEFAULT_ZERO_NAME,
    FunctionParams,
    IOName,
    parse_function_params_values,
)

PHASE_ESTIMATION_DEFAULT_OUTPUT_NAME = "PHASE_ESTIMATION"


class ExponentiationScaling(pydantic.BaseModel):
    """
    Details of exponentiation scaling for phase estimation.
    """

    max_depth: pydantic.PositiveInt = pydantic.Field(
        description="The max_depth of the smallest exponentiation",
    )
    max_depth_scaling_factor: pydantic.NonNegativeFloat = pydantic.Field(
        default=2.0,
        description="The scaling factor of the exponentiation max_depth; defaults to 2.",
    )


class ExponentiationSpecification(pydantic.BaseModel):
    """
    Specifications of individual Exponentiation details for each qubit; only valid if Exponentiation is given as unitary_params for PhaseEstimation.
    This sets the optimization to ExponentiationOptimization.MINIMIZE_ERROR and overrides the max_depth constraints.
    """

    scaling: Optional[ExponentiationScaling] = pydantic.Field(
        default=None,
        description="The scaling of the exponentiation functions.",
    )
    max_depths: Optional[Tuple[pydantic.NonNegativeInt, ...]] = pydantic.Field(
        default=None,
        description="The max_depth of each exponentiation function; overrides scaling.",
    )

    @pydantic.root_validator
    def validate_exponentiation_specification(
        cls, values: Dict[str, Any]
    ) -> Dict[str, Any]:
        if values.get("scaling") is None and values.get("max_depths") is None:
            raise ValueError("At least one specification must be provided.")
        return values


class PhaseEstimation(FunctionParams):
    """
    Quantum phase estimation of a given unitary function.
    """

    size: pydantic.PositiveInt = pydantic.Field(
        description="The number of qubits storing the estimated phase."
    )
    unitary: str = pydantic.Field(
        default="",
        description="The unitary function for phase estimation.",
    )
    unitary_params: FunctionParams = pydantic.Field(
        description="The unitary function parameters."
    )
    exponentiation_specification: Optional[
        ExponentiationSpecification
    ] = pydantic.Field(
        default=None,
        description="The specifications for phase estimation of exponentiation functions.",
    )

    _output_name: IOName = pydantic.PrivateAttr(
        default=PHASE_ESTIMATION_DEFAULT_OUTPUT_NAME
    )

    @property
    def output_name(self) -> str:
        return self._output_name

    def _create_ios(self) -> None:
        self._inputs = {**self.unitary_params.inputs}
        self._outputs = {**self.unitary_params.outputs}
        self._outputs[self._output_name] = RegisterUserInput(
            name=self._output_name, size=self.size
        )
        self._create_zero_input_registers({DEFAULT_ZERO_NAME: self.size})

    @pydantic.root_validator(pre=True)
    def parse_function_params(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        parse_function_params_values(
            values=values,
            params_key="unitary_params",
            discriminator_key="unitary",
            param_classes=function_param_library_without_self_reference.param_list,
        )
        return values

    @pydantic.validator("unitary_params")
    def validate_unitary_params(cls, unitary_params: FunctionParams) -> FunctionParams:
        if not unitary_params.is_powerable():
            raise ValueError(
                f"Phase estimation of {unitary_params.discriminator()} is currently not supported."
            )
        return unitary_params

    @pydantic.validator("exponentiation_specification")
    def validate_exponentiation_specification(
        cls,
        exponentiation_specification: Optional[ExponentiationSpecification],
        values: Dict[str, Any],
    ) -> Optional[ExponentiationSpecification]:
        if exponentiation_specification is None:
            return exponentiation_specification
        unitary_params = values.get("unitary_params")
        if not isinstance(unitary_params, Exponentiation):
            raise ValueError(
                "exponentiation_specification is only valid for Exponentiation unitary_params."
            )
        if exponentiation_specification.max_depths is not None and len(
            exponentiation_specification.max_depths
        ) != values.get("size"):
            raise ValueError("Length of max_depths must match the provided size.")
        return exponentiation_specification
