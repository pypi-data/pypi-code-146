import enum
import itertools
from typing import List, Union

import pydantic

from classiq.interface.generator import function_params
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import (
    DEFAULT_INPUT_NAME,
    DEFAULT_OUTPUT_NAME,
)
from classiq.interface.helpers.custom_pydantic_types import PydanticNonNegIntTuple

ConnectivityMap = List[PydanticNonNegIntTuple]


class SupportedConnectivityMaps(str, enum.Enum):
    FULL = "full"
    LINEAR = "linear"
    CIRCULAR = "circular"
    PAIRWISE = "pairwise"


ConnectivityMapType = Union[ConnectivityMap, SupportedConnectivityMaps, None]

_NUM_QUBITS_NOT_PROVIDED_ERROR = (
    "Either num_qubits or connectivity_map in the form of a list must be provided"
)


class HardwareEfficientAnsatz(function_params.FunctionParams):
    connectivity_map: ConnectivityMapType = pydantic.Field(
        default=None,
        description="Hardware's connectivity map, in the form [ [x0, x1], [x1, x2],...]. "
        "If none specified - use connectivity map from the model hardware settings. "
        "If none specified as well, all qubit pairs will be connected.",
    )
    num_qubits: pydantic.PositiveInt = pydantic.Field(
        default=None,
        description="Number of qubits in the ansatz.",
    )
    reps: pydantic.PositiveInt = pydantic.Field(
        default=1, description="Number of layers in the Ansatz"
    )

    one_qubit_gates: Union[str, List[str]] = pydantic.Field(
        default=["x", "ry"],
        description='List of gates for the one qubit gates layer, e.g. ["x", "ry"]',
    )
    two_qubit_gates: Union[str, List[str]] = pydantic.Field(
        default=["cx"],
        description='List of gates for the two qubit gates entangling layer, e.g. ["cx", "cry"]',
    )
    parameter_prefix: str = pydantic.Field(
        default="param_",
        description="Prefix for the generated parameters",
    )

    @pydantic.validator("num_qubits", pre=True, always=True)
    def validate_num_qubits(cls, num_qubits, values):
        connectivity_map = values.get("connectivity_map")
        conn_map_is_not_list = (
            isinstance(connectivity_map, SupportedConnectivityMaps)
            or connectivity_map is None
        )

        if num_qubits is None and conn_map_is_not_list:
            raise ValueError(_NUM_QUBITS_NOT_PROVIDED_ERROR)
        if num_qubits is None:
            return len(set(itertools.chain.from_iterable(connectivity_map)))
        if conn_map_is_not_list:
            return num_qubits

        invalid_qubits = {
            qubit
            for qubit in itertools.chain.from_iterable(connectivity_map)
            if qubit >= num_qubits
        }
        if invalid_qubits:
            raise ValueError(
                f"Invalid qubits: {invalid_qubits} "
                f"out of range specified by num_qubits: [0, {num_qubits - 1}]"
            )
        return num_qubits

    def _create_ios(self) -> None:
        self._inputs = {
            DEFAULT_INPUT_NAME: RegisterUserInput(
                name=DEFAULT_INPUT_NAME, size=self.num_qubits
            )
        }
        self._outputs = {
            DEFAULT_OUTPUT_NAME: RegisterUserInput(
                name=DEFAULT_OUTPUT_NAME, size=self.num_qubits
            )
        }
