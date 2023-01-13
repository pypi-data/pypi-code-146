from pyqusim.qpu import QPU
from pyqusim.runnable import Runnable
import pyqusim.typing as pqst
from pyqusim.utils import export


@export
class Measure(Runnable):
    def __init__(self, index: pqst.Indices) -> None:
        self.index = index

    @property
    def ends_with_measure(self) -> bool:
        return True

    def run(self, qpu: QPU) -> pqst.MeasureOutcome:
        indices = qpu.get_qubit_indices(self.index)
        outcomes = tuple(qpu.measure(i) for i in indices)
        if len(outcomes) == 1:
            return outcomes[0]
        return outcomes
