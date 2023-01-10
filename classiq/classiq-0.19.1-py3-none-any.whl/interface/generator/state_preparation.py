from __future__ import annotations

from collections.abc import Sequence
from enum import Enum
from numbers import Number
from typing import Any, Collection, Dict, Optional, Tuple, Union

import numpy as np
import pydantic
from numpy.typing import ArrayLike

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import (
    DEFAULT_INPUT_NAME,
    DEFAULT_OUTPUT_NAME,
    FunctionParams,
)
from classiq.interface.generator.preferences.optimization import (
    StatePrepOptimizationMethod,
)
from classiq.interface.generator.range_types import NonNegativeFloatRange, Range
from classiq.interface.generator.validations.validator_functions import (
    validate_amplitudes,
    validate_probabilities,
)
from classiq.interface.helpers.custom_pydantic_types import PydanticProbabilityFloat

from classiq.exceptions import ClassiqError

_MAX_SUPPORTED_QUBITS_FOR_PMF: int = 16


class Metrics(str, Enum):
    KL = "KL"
    L2 = "L2"
    L1 = "L1"
    MAX_PROBABILITY = "MAX_PROBABILITY"
    LOSS_OF_FIDELITY = "LOSS_OF_FIDELITY"

    @classmethod
    def from_sp_optimization_method(
        cls, sp_opt_method: StatePrepOptimizationMethod
    ) -> Metrics:
        try:
            return Metrics(sp_opt_method.value)
        except ValueError:
            raise ValueError(f"Failed to convert {sp_opt_method} to an error metric")


class PMF(pydantic.BaseModel):
    pmf: Tuple[PydanticProbabilityFloat, ...]
    _validate_amplitudes = pydantic.validator("pmf", allow_reuse=True)(
        validate_probabilities
    )

    class Config:
        frozen = True


class GaussianMoments(pydantic.BaseModel):
    mu: float
    sigma: pydantic.PositiveFloat

    class Config:
        frozen = True


class GaussianMixture(pydantic.BaseModel):
    gaussian_moment_list: Tuple[GaussianMoments, ...]

    class Config:
        frozen = True


class HardwareConstraints(pydantic.BaseModel):
    # this will be moved to model preferences
    # it will be a dictionary of gates and their corresponding errors
    two_qubit_gate_error: Optional[PydanticProbabilityFloat]

    class Config:
        frozen = True


PossibleProbabilities = Union[PMF, GaussianMixture]
PydanticObjectNonNegativeFloatRange = Dict[str, Any]

FlexibleNonNegativeFloatRange = Optional[
    Union[Number, PydanticObjectNonNegativeFloatRange, ArrayLike, NonNegativeFloatRange]
]
FlexiblePossibleProbabilities = Union[
    PossibleProbabilities, ArrayLike, dict, Collection[float]
]

FlexibleAmplitudes = Union[ArrayLike, Collection[float]]


class StatePreparation(FunctionParams):
    def __init__(
        self,
        depth_range: FlexibleNonNegativeFloatRange = None,
        cnot_count_range: FlexibleNonNegativeFloatRange = None,
        **kwargs,
    ) -> None:
        super().__init__(
            depth_range=self._initialize_flexible_non_negative_float_range(depth_range),
            cnot_count_range=self._initialize_flexible_non_negative_float_range(
                cnot_count_range
            ),
            **kwargs,
        )

    amplitudes: Optional[Tuple[float, ...]] = pydantic.Field(
        description="vector of probabilist", default=None
    )
    probabilities: Optional[Union[PMF, GaussianMixture]] = pydantic.Field(
        description="vector of amplitudes", default=None
    )
    depth_range: NonNegativeFloatRange = NonNegativeFloatRange(
        lower_bound=0, upper_bound=1e100
    )
    cnot_count_range: NonNegativeFloatRange = NonNegativeFloatRange(
        lower_bound=0, upper_bound=1e100
    )
    error_metric: Dict[Metrics, NonNegativeFloatRange] = pydantic.Field(
        default_factory=lambda: {
            Metrics.L2: NonNegativeFloatRange(lower_bound=0, upper_bound=1e100)
        }
    )
    num_qubits: int = pydantic.Field(
        description="number of qubits to use in the function", default=None
    )
    is_uniform_start: bool = True
    hardware_constraints: HardwareConstraints = pydantic.Field(
        default_factory=HardwareConstraints
    )

    # The order of validations is important, first, the amplitudes, second the
    # probabilities and then num_qubits and error_metric.

    @pydantic.validator("amplitudes", always=True, pre=True)
    def _initialize_amplitudes(
        cls,
        amplitudes: Optional[FlexibleAmplitudes],
    ) -> Optional[Tuple[float, ...]]:
        if amplitudes is None:
            return None
        amplitudes = np.array(amplitudes).squeeze()
        if amplitudes.ndim == 1:
            return validate_amplitudes(tuple(amplitudes))

        raise ValueError(
            "Invalid amplitudes were given, please ensure the amplitude is a vector of float in the form of either tuple or list or numpy array"
        )

    @pydantic.validator("probabilities", always=True, pre=True)
    def _initialize_probabilities(
        cls,
        probabilities: Optional[FlexiblePossibleProbabilities],
    ) -> Optional[Union[PMF, GaussianMixture, dict]]:
        if probabilities is None:
            return None
        if isinstance(probabilities, PossibleProbabilities.__args__):  # type: ignore[attr-defined]
            return probabilities
        if isinstance(probabilities, dict):  # a pydantic object
            return probabilities
        probabilities = np.array(probabilities).squeeze()
        if probabilities.ndim == 1:
            return PMF(pmf=probabilities.tolist())

        raise ValueError(
            "Invalid probabilities were given, please ensure the probabilities is a vector of float in the form of either tuple or list or numpy array"
        )

    @pydantic.validator("error_metric", always=True, pre=True)
    def _validate_error_metric(
        cls, error_metric: Dict[Metrics, NonNegativeFloatRange], values: Dict[str, Any]
    ) -> Dict[Metrics, NonNegativeFloatRange]:
        if (
            values.get("amplitudes") is not None
            and error_metric is not None
            and (Metrics.KL in error_metric or Metrics.LOSS_OF_FIDELITY in error_metric)
        ):
            raise ValueError(
                "KL and LOSS_OF_FIDELITY are not supported as error metric in case of amplitudes preparation"
            )
        if values.get("hardware_constraints") is None:
            return error_metric
        error_metrics = {
            error_metric
            for error_metric in error_metric.keys()
            if error_metric is not Metrics.LOSS_OF_FIDELITY
        }
        if error_metrics:
            raise ValueError(
                "Enabling hardware constraints requires the use of only the loss of fidelity as an error metric"
            )
        return error_metric

    @pydantic.validator("num_qubits", always=True, pre=True)
    def _validate_num_qubits(
        cls, num_qubits: Optional[int], values: Dict[str, Any]
    ) -> int:
        assert isinstance(num_qubits, int) or num_qubits is None
        probabilities: Optional[Union[PMF, GaussianMixture]] = values.get(
            "probabilities"
        )
        amplitudes = values.get("amplitudes")
        if isinstance(probabilities, GaussianMixture):
            if num_qubits is None:
                raise ValueError("num_qubits must be set when using gaussian mixture")
            return num_qubits

        if probabilities is not None:
            num_state_qubits = len(probabilities.pmf).bit_length() - 1
        elif amplitudes:
            num_state_qubits = len(amplitudes).bit_length() - 1
        else:
            raise ValueError(
                "Can't validate num_qubits without valid probabilities or amplitudes"
            )

        if num_qubits is None:
            num_qubits = max(
                2 * num_state_qubits - 2, 1
            )  # Maximum with MCMT auxiliary requirements
        if num_qubits < num_state_qubits:
            raise ValueError(
                f"Minimum of {num_state_qubits} qubits needed, got {num_qubits}"
            )
        return num_qubits

    @staticmethod
    def _initialize_flexible_non_negative_float_range(
        attribute_value: FlexibleNonNegativeFloatRange,
    ) -> NonNegativeFloatRange:
        if attribute_value is None:
            return NonNegativeFloatRange(lower_bound=0, upper_bound=1e100)
        elif isinstance(attribute_value, Number):
            return NonNegativeFloatRange(lower_bound=0, upper_bound=attribute_value)
        # This should be `isinstance(obj, NonNegativeFloatRange)`, but mypy...
        elif isinstance(attribute_value, Range):
            return attribute_value
        elif isinstance(attribute_value, dict):  # a pydantic object
            return attribute_value  # type: ignore[return-value]
        elif isinstance(attribute_value, Sequence):
            if len(attribute_value) == 1:
                return NonNegativeFloatRange(
                    lower_bound=0, upper_bound=attribute_value[0]
                )
            elif len(attribute_value) == 2:
                return NonNegativeFloatRange(
                    lower_bound=attribute_value[0], upper_bound=attribute_value[1]
                )
        raise ValueError("Invalid NonNegativeFloatRange was given")

    @pydantic.root_validator
    def _validate_either_probabilities_or_amplitudes(
        cls,
        values: Dict[str, Any],
    ) -> Optional[Union[PMF, GaussianMixture, dict]]:
        amplitudes = values.get("amplitudes")
        probabilities = values.get("probabilities")
        if amplitudes is not None and probabilities is not None:
            raise ValueError(
                "StatePreparation can't get both probabilities and amplitudes"
            )
        return values

    def _non_gaussian_num_qubits(self) -> int:
        if isinstance(self.probabilities, PMF):
            return len(self.probabilities.pmf).bit_length() - 1
        elif self.amplitudes:
            return len(self.amplitudes).bit_length() - 1
        raise ClassiqError("Badly initialized StatePreparation")

    def num_state_qubits(self) -> int:
        if isinstance(self.probabilities, GaussianMixture):
            return self.num_qubits
        return self._non_gaussian_num_qubits()

    def num_rotated_qubits(self) -> int:
        if isinstance(self.probabilities, GaussianMixture):
            return min(_MAX_SUPPORTED_QUBITS_FOR_PMF, self.num_qubits)
        return self._non_gaussian_num_qubits()

    def _create_ios(self) -> None:
        self._inputs = dict()
        self._outputs = {
            DEFAULT_OUTPUT_NAME: RegisterUserInput(
                name=DEFAULT_OUTPUT_NAME, size=self.num_state_qubits()
            )
        }
        self._create_zero_input_registers({DEFAULT_INPUT_NAME: self.num_state_qubits()})
