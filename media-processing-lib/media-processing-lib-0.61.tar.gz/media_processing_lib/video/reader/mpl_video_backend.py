"""MPLVideo backend -- module that defines a backend suitable for MPLVideo data reader"""
from abc import ABC, abstractmethod
from typing import Union, List
from pathlib import Path
import numpy as np

MPLFrame = np.ndarray

class MPLVideoBackend(ABC):
    """MPLVideo backend implmenetation"""

    def __init__(self, path: Path):
        self.path = Path(path)
        assert self.path_in_supported_format

    @staticmethod
    @abstractmethod
    def supported_formats() -> List[str]:
        """Supported formats"""

    @abstractmethod
    def __len__(self) -> int:
        """Gets the length of the backend"""

    @abstractmethod
    def __getitem__(self, key: Union[int, slice]) -> Union[MPLFrame, List[MPLFrame]]:
        """Gets the item(s) at key"""

    @property
    def path_in_supported_format(self) -> bool:
        """Returns if the path is a valid video according to this backend"""
        return self.path.suffix in type(self).supported_formats(), f"Got {self.path.suffix}"
