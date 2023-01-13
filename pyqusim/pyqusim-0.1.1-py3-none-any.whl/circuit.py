from collections import defaultdict
from quantalpy.runnable import Runnable
from quantalpy.qpu import QPU
from quantalpy.ctx import ContextMixin
from quantalpy.utils import export

import quantalpy.typing as qpt


@export
class Circuit(ContextMixin, Runnable):
    def __init__(self, gates: list[Runnable] | None = None) -> None:
        self.gates = gates or []

    @property
    def ends_with_measure(self) -> bool:
        if not self.gates:
            return False
        return self.gates[-1].ends_with_measure

    def run(self, qpu: QPU) -> qpt.MeasureOutcome | None:
        result = None
        for gate in self.gates:
            result = gate.run(qpu=qpu)
        return result

    def run_multiple(
        self, qpu: QPU, n: int, normalize: bool = True
    ) -> dict[qpt.MeasureOutcome, int]:
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
