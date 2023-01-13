from abc import ABC, abstractmethod

from pyqusim.qpu import QPU
import pyqusim.typing as pqst


class Runnable(ABC):
    @property
    def ends_with_measure(self) -> bool:
        return False

    @abstractmethod
    def run(self, qpu: QPU) -> pqst.MeasureOutcome | None:
        pass
