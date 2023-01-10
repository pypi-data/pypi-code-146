import abc
from typing import Callable

from torch import Tensor

from classiq.interface.generator.result import GeneratedCircuit

from classiq.applications.qnn.circuit_utils import (
    QASM3_ARGUMENTS_TENSOR,
    extract_parameters,
    map_parameters,
    validate_circuit,
)

EXECUTE_FUNCTION = Callable[[GeneratedCircuit, QASM3_ARGUMENTS_TENSOR], Tensor]


class QuantumGradient(abc.ABC):
    def __init__(
        self, execute: EXECUTE_FUNCTION, circuit: GeneratedCircuit, *args, **kwargs
    ):
        self._execution_function = execute

        validate_circuit(circuit)
        self.circuit = circuit
        self._parameters_names = extract_parameters(circuit)

    def execute(self, inputs: Tensor, weights: Tensor) -> Tensor:
        return self._execution_function(
            self.circuit, map_parameters(self._parameters_names, inputs, weights)
        )

    @abc.abstractmethod
    def gradient(self, inputs: Tensor, weights: Tensor, *args, **kwargs) -> Tensor:
        raise NotImplementedError
