import numpy as np
import numpy.typing as npt

from quantalpy.runnable import Runnable
from quantalpy.qpu import QPU
from quantalpy.utils import export


@export
class UnaryQubitGate(Runnable):
    def __init__(self, matrix: npt.ArrayLike, index: int) -> None:
        self.matrix = np.asarray(matrix, dtype=complex)
        self.index = index

    def run(self, qpu: QPU) -> None:
        qpu.apply_unary_qubit_operator(index=self.index, matrix=self.matrix)


@export
class Hadamard(UnaryQubitGate):
    def __init__(self, index: int) -> None:
        had = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        super().__init__(matrix=had, index=index)


@export
class PhaseShift(UnaryQubitGate):
    def __init__(self, phi: float, index: int) -> None:
        had = np.array([[1, 0], [0, np.exp(1j * phi)]])
        super().__init__(matrix=had, index=index)
