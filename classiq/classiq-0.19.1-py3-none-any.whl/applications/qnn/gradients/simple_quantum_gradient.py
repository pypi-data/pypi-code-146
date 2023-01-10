import torch
from torch import Tensor

from classiq.interface.generator.result import GeneratedCircuit

from classiq.applications.qnn.gradients.quantum_gradient import (
    EXECUTE_FUNCTION,
    QuantumGradient,
)

#
# Gradient consts
#
EPSILON = 1e-2


class SimpleQuantumGradient(QuantumGradient):
    def __init__(
        self,
        execute: EXECUTE_FUNCTION,
        circuit: GeneratedCircuit,
        epsilon: float = EPSILON,
        *args,
        **kwargs
    ):
        super().__init__(execute, circuit)
        self._epsilon = epsilon

    def _single_gradient(
        self, inputs: Tensor, weights: Tensor, weight_index: int, *args, **kwargs
    ) -> Tensor:
        epsilon = torch.zeros_like(weights)
        epsilon[weight_index] = self._epsilon

        value_plus = self.execute(inputs, weights + epsilon)
        value_minus = self.execute(inputs, weights - epsilon)

        return (value_plus - value_minus) / (2 * self._epsilon)

    def gradient(self, inputs: Tensor, weights: Tensor, *args, **kwargs) -> Tensor:
        return torch.tensor(
            [
                self._single_gradient(inputs, weights, i, *args, **kwargs)
                for i in range(len(weights))
            ]
        )
