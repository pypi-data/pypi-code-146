"""@Author: Rayane AMROUCHE

Datastorage Class.
"""

import json
from typing import Any


class DataStorage(dict):
    """A dictionary that can be accessed through attributes."""

    def __dir__(self):
        return sorted(set(dir(super()) + list(self.keys())))

    def __getattr__(self, __name: str) -> Any:
        return self[__name]

    def __repr__(self) -> str:
        try:
            res = json.dumps(self, indent=4, skipkeys=True)
        except TypeError as _:
            res = super().__repr__()
        return res
