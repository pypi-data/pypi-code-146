from quantalpy.qpu import QPU
from quantalpy.runnable import Runnable
import quantalpy.typing as qpt


class Measure(Runnable):
    def __init__(self, index: int | slice) -> None:
        self.index = index

    @property
    def ends_with_measure(self) -> bool:
        return True

    def run(self, qpu: QPU) -> qpt.MeasureOutcome | None:
        if isinstance(self.index, int):
            return qpu.measure(index=self.index)
        else:
            return tuple(
                qpu.measure(index=i) for i in range(*self.index.indices(qpu.n_qubits))
            )
