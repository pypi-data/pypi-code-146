import numpy as np

from pyqusim.ctx import ContextMixin
from pyqusim.utils import export
import pyqusim.typing as pqst

PROJECTORS = [
    np.array([[1, 0], [0, 0]], dtype=complex),
    np.array([[0, 0], [0, 1]], dtype=complex),
]


@export
class QPU(ContextMixin):
    def __init__(self, n_qubits: int) -> None:
        self._n_qubits = n_qubits
        self._amplitudes = None
        self.reset()

    def get_qubit_indices(self, indices: pqst.Indices) -> tuple[int]:
        match indices:
            case int():
                return (indices,)
            case slice():
                return tuple(range(*indices.indices(self.n_qubits)))
            case _:
                return tuple(indices)

    @property
    def n_qubits(self) -> int:
        return self._n_qubits

    def reset(self) -> None:
        self._amplitudes = np.zeros(shape=tuple(2 for _ in range(self.n_qubits)))
        self._amplitudes[tuple(0 for _ in range(self.n_qubits))] = 1

    @staticmethod
    def unary_qubit_operation(
        state: np.ndarray[complex], index: int, matrix: np.ndarray[(2, 2), complex]
    ) -> np.ndarray[complex]:
        aux = np.tensordot(matrix, state, axes=(1, index))
        return np.moveaxis(aux, 0, index)

    def apply_unary_qubit_operator(
        self, index: int, matrix: np.ndarray[(2, 2), complex]
    ) -> None:
        self._amplitudes = self.unary_qubit_operation(
            state=self._amplitudes, matrix=matrix, index=index
        )

    @staticmethod
    def binary_qubit_operator(
        state: np.ndarray[complex],
        indices: tuple[int, int],
        matrix: np.ndarray[(4, 4), complex],
    ) -> np.ndarray[complex]:
        matrix = matrix.reshape((2, 2, 2, 2))
        aux = np.tensordot(matrix, state, axes=((2, 3), indices))
        return np.moveaxis(aux, (0, 1), indices)

    def apply_binary_qubit_operator(
        self, indices: tuple[int, int], matrix: np.ndarray[(4, 4), complex]
    ) -> None:
        self._amplitudes = self.binary_qubit_operator(
            state=self._amplitudes, matrix=matrix, indices=indices
        )

    def measure(self, index: int) -> int:
        result_zero_state = self.unary_qubit_operation(
            matrix=PROJECTORS[0], state=self._amplitudes, index=index
        )
        prop_zero = np.linalg.norm(result_zero_state.flatten()) ** 2
        outcome = np.random.choice([0, 1], p=[prop_zero, 1 - prop_zero])
        match outcome:
            case 0:
                self._amplitudes = result_zero_state / np.linalg.norm(
                    result_zero_state.flatten()
                )
            case 1:
                result_one_state = self.unary_qubit_operation(
                    matrix=PROJECTORS[1], state=self._amplitudes, index=index
                )
                self._amplitudes = result_one_state / np.linalg.norm(
                    result_one_state.flatten()
                )
        return outcome
