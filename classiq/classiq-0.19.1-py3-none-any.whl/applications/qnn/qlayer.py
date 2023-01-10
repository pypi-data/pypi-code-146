from typing import Callable, Optional, Tuple

import torch
import torch.nn as nn
from torch import Tensor
from torch.nn.parameter import Parameter

from classiq.interface.generator.result import GeneratedCircuit

from classiq.applications.qnn.circuit_utils import (
    extract_parameters,
    map_parameters,
    validate_circuit,
)
from classiq.applications.qnn.gradients.quantum_gradient import EXECUTE_FUNCTION
from classiq.applications.qnn.gradients.simple_quantum_gradient import (
    SimpleQuantumGradient,
)
from classiq.applications.qnn.torch_utils import iter_inputs_weights
from classiq.exceptions import ClassiqTorchError


class QLayerFunction(torch.autograd.Function):
    @staticmethod
    def forward(  # type: ignore[override]
        ctx,
        inputs: Tensor,
        weights: Tensor,
        circuit: GeneratedCircuit,
        execution_function: EXECUTE_FUNCTION,
    ) -> Tensor:
        """
        This function receives:
            inputs: a 2D Tensor of floats - (batch_size, in_features)
            weights: a 2D Tensor of floats - (out_features, in_features)
            qcode: a string of parametric OpenQASM3 code
                (or a `QASM3Parser` object, which is like a parsed OpenQASM)
            execution_function: a function taking `qcode, arguments`,
                and returning a result (of type Tensor)
                where `arguments` is of type `EXECUTE_FUNCTION`
                    (from `classiq.applications.qnn.gradients`)
        """
        validate_circuit(circuit)

        # save for backward
        ctx.save_for_backward(inputs, weights)
        ctx.execution_function = execution_function
        ctx.circuit = circuit
        ctx.quantum_gradient = SimpleQuantumGradient(execution_function, circuit)

        ctx.batch_size, ctx.num_in_features = inputs.shape
        ctx.num_out_features, ctx.num_weights = weights.shape

        def _execute(inputs_: Tensor, weights_: Tensor) -> Tensor:
            return execution_function(
                circuit,
                map_parameters(
                    circuit,
                    inputs_,
                    weights_,
                ),
            )

        return iter_inputs_weights(
            _execute,
            inputs,
            weights,
            expected_shape=(ctx.batch_size, ctx.num_out_features),
        )

    @staticmethod
    def backward(  # type: ignore[override]
        ctx, grad_output: Tensor
    ) -> Tuple[Optional[Tensor], Optional[Tensor], None, None]:
        inputs, weights = ctx.saved_tensors

        grad_weights = grad_inputs = grad_qcode = grad_execution_function = None

        if ctx.needs_input_grad[1]:
            grad_weights = iter_inputs_weights(
                ctx.quantum_gradient.gradient,
                inputs,
                weights,
                expected_shape=(ctx.batch_size, ctx.num_weights),
            )

            grad_weights = grad_weights * grad_output

        if any(ctx.needs_input_grad[i] for i in (0, 2, 3)):
            raise ClassiqTorchError(
                f"Grad required for unknown type: {ctx.needs_input_grad}"
            )

        return grad_inputs, grad_weights, grad_qcode, grad_execution_function


CalcNumOutFeatures = Callable[[GeneratedCircuit], int]


def calc_num_out_features_single_output(circuit: GeneratedCircuit) -> int:
    return 1


# Todo: extend the input to allow for multiple `qcode` - one for each output
#   thus allowing (something X n) instead of (something X 1) output
class QLayer(nn.Module):
    def __init__(
        self,
        circuit: GeneratedCircuit,
        execution_function: EXECUTE_FUNCTION,
        head_start: Optional[float] = None,
        calc_num_out_features: CalcNumOutFeatures = calc_num_out_features_single_output,
    ):
        validate_circuit(circuit)

        super().__init__()

        self._execution_function = execution_function
        self._head_start = head_start

        self.circuit = circuit

        weights, _ = extract_parameters(circuit)
        self.in_features = len(weights)
        self.out_features = calc_num_out_features(circuit)

        self._initialize_parameters()

    def _initialize_parameters(self) -> None:
        shape = (self.out_features, self.in_features)
        if self._head_start is None:
            value = torch.rand(shape)
        else:
            value = torch.zeros(shape) + self._head_start

        self.weight = Parameter(value)

    def forward(self, x: Tensor) -> Tensor:
        return QLayerFunction.apply(
            x, self.weight, self.circuit, self._execution_function
        )
