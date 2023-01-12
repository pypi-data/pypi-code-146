import abc
from typing import Optional

from bin.models.bin_base_model import BinBaseModel
from bin.process.process import Process
from bin.process.process_result import ProcessResult


class UpResult(BinBaseModel):
    name: str
    has_succeeded: bool
    details: Optional[str]

    def with_details(self, details: str) -> "UpResult":
        return UpResult(name=self.name, has_succeeded=self.has_succeeded, details=details)

    @classmethod
    def failed(cls, name: str) -> "UpResult":
        return cls(name=name, has_succeeded=False)

    @classmethod
    def succeeded(cls, name: str) -> "UpResult":
        return cls(name=name, has_succeeded=True)

    @classmethod
    def from_process_result(cls, name: str, process_result: ProcessResult) -> "UpResult":
        return cls(name=name, has_succeeded=process_result.has_succeeded())


class UpSubcommand(abc.ABC):
    @abc.abstractmethod
    def run(self, process: Process) -> UpResult:
        pass
