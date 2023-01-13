from collections import defaultdict
from pyqusim.runnable import Runnable
from pyqusim.qpu import QPU
from pyqusim.ctx import ContextMixin
from pyqusim.utils import export

import pyqusim.typing as pqst


@export
class Circuit(ContextMixin, Runnable):
    def __init__(self, gates: list[Runnable] | None = None) -> None:
        self.gates = gates or []

    @property
    def ends_with_measure(self) -> bool:
        if not self.gates:
            return False
        return self.gates[-1].ends_with_measure

    def run(self, qpu: QPU) -> pqst.MeasureOutcome | None:
        result = None
        for gate in self.gates:
            result = gate.run(qpu=qpu)
        return result

    def run_multiple(
        self, qpu: QPU, n: int, normalize: bool = True
    ) -> dict[pqst.MeasureOutcome, int]:
        if not self.ends_with_measure:
            raise RuntimeError(
                "Method can only be called if the circuit ends with a measurement"
            )
        results = defaultdict(int)
        for i in range(n):
            qpu.reset()
            results[self.run(qpu)] += 1
        qpu.reset()
        if normalize:
            return {k: v / n for k, v in results.items()}
        return dict(results)
