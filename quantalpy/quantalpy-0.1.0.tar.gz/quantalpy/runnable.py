from abc import ABC, abstractmethod

from quantalpy.qpu import QPU
import quantalpy.typing as qpt


class Runnable(ABC):
    @property
    def ends_with_measure(self) -> bool:
        return False

    @abstractmethod
    def run(self, qpu: QPU) -> qpt.MeasureOutcome | None:
        pass
