"""MPLRawData video reader"""
from typing import Tuple, List, Union
from overrides import overrides
import numpy as np

from .mpl_video_backend import MPLVideoBackend, MPLFrame

ReadReturnType = Tuple[np.ndarray, int, List[int], int]

# pylint: disable=super-init-not-called
class MPLRawDataBackend(MPLVideoBackend):
    """MPLRawData backend implmenetation"""

    def __init__(self, raw_data: Union[List, np.ndarray]):
        assert isinstance(raw_data, (List, np.ndarray))
        assert len(raw_data) > 0
        self.raw_data = np.array(raw_data).astype(np.uint8)
        assert len(self.raw_data.shape) == 4 and self.raw_data.shape[-1] == 3

    @staticmethod
    @overrides
    def supported_formats() -> List[str]:
        return []

    @property
    @overrides
    def path_in_supported_format(self) -> bool:
        return False

    @overrides
    def __getitem__(self, key: Union[int, slice]) -> Union[MPLFrame, List[MPLFrame]]:
        return self.raw_data[key]

    @overrides
    def __len__(self) -> int:
        return len(self.raw_data)
