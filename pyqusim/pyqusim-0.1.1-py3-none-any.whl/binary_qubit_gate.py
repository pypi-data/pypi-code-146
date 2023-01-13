import numpy as np
import numpy.typing as npt

from quantalpy.runnable import Runnable
from quantalpy.unary_qubit_gate import UnaryQubitGate
from quantalpy.qpu import QPU
from quantalpy.utils import export


@export
class BinaryQubitGate(Runnable):
    def __init__(self, matrix: npt.ArrayLike, indices: tuple[int, int]) -> None:
        self.matrix = np.asarray(matrix, dtype=complex)
        self.indices = indices

    def run(self, qpu: QPU) -> None:
        qpu.apply_binary_qubit_operator(indices=self.indices, matrix=self.matrix)


@export
class ControlledQubitGate(BinaryQubitGate):
    def __init__(self, gate: UnaryQubitGate, control: int) -> None:
        matrix = np.block(
            [[np.eye(2), np.zeros((2, 2))], [np.zeros((2, 2)), gate.matrix]]
        )
        super().__init__(matrix=matrix, indices=(control, gate.index))
