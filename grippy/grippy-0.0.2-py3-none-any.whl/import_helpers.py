from importlib.machinery import ModuleSpec, PathFinder
from types import ModuleType
from typing import Sequence


class GrippyLoader(PathFinder):
    def __init__(self, import_path):
        self.import_path = import_path

    def find_spec(
        self,
        fullname: str,
        path: Sequence[bytes | str] | None,
        target: ModuleType | None = None
    ) -> ModuleSpec | None:
        return super().find_spec(
            fullname, [str(self.import_path)], target
        )
