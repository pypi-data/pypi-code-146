import typing as t

from quantalpy.qpu import QPU
from quantalpy.runnable import Runnable
import quantalpy.typing as qpt
from quantalpy.utils import export


@export
class Measure(Runnable):
    def __init__(self, index: int | slice | t.Iterable[int]) -> None:
        self.index = index

    @property
    def ends_with_measure(self) -> bool:
        return True

    def run(self, qpu: QPU) -> qpt.MeasureOutcome:
        match self.index:
            case int():
                return qpu.measure(index=self.index)
            case slice():
                return tuple(
                    qpu.measure(index=i)
                    for i in range(*self.index.indices(qpu.n_qubits))
                )
            case _:
                return tuple(qpu.measure(i) for i in self.index)
