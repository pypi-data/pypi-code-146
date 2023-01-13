import numpy as np
import numpy.typing as npt

from pyqusim.runnable import Runnable
from pyqusim.unary_qubit_gate import UnaryQubitGate
from pyqusim.qpu import QPU
from pyqusim.utils import export


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
        self.controlled = gate
        self.control_index = control

    def __repr__(self) -> str:
        gate_repr = repr(self.controlled)
        if gate_repr.endswith(">"):
            gate_repr = gate_repr[:-1]
        return f"{gate_repr} controlled at {self.control_index}>"
