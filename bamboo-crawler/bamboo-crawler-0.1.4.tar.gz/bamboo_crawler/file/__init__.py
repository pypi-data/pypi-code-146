import pathlib

from ..interfaces.context import Context
from ..interfaces.inputter import Inputter


class FileInputter(Inputter[str]):
    def __init__(self, filepath: str) -> None:
        self.path = pathlib.Path(filepath).resolve()

    def read(self) -> Context[str]:
        return Context(self.path.open().read())
