"""MPLImagesPathBackend video reader"""
from functools import lru_cache
from typing import Tuple, List, Union
from pathlib import Path
from overrides import overrides
import numpy as np
from natsort import natsorted

from .mpl_video_backend import MPLVideoBackend, MPLFrame
from ...image import image_read
from ...logger import logger

ReadReturnType = Tuple[np.ndarray, int, List[int], int]

class MPLImagesPathBackend(MPLVideoBackend):
    """MPLImagesPathBackend backend implmenetation"""

    def __init__(self, path: str, img_lib: str = "opencv", pattern: str = "*"):
        self.files = [Path(x).absolute() for x in natsorted([str(x) for x in Path(path).glob(pattern)])]
        assert len(self.files) > 0, f"Found no files in '{path}' for pattern '{pattern}'"
        super().__init__(path)
        self.img_lib = img_lib

    @staticmethod
    @overrides
    def supported_formats() -> List[str]:
        return [".png"]

    @property
    @overrides
    def path_in_supported_format(self) -> bool:
        if not self.path.is_dir():
            logger.info(f"Expected directory, found '{self.path}'")
            return False
        for file in self.files:
            if file.suffix not in self.supported_formats():
                logger.info(f"Expected an image, found '{file}'")
                return False
        return True

    @lru_cache
    @overrides
    def __getitem__(self, key: Union[int, slice]) -> Union[MPLFrame, List[MPLFrame]]:
        assert isinstance(key, int), f"Got {type(key)}"
        assert key < len(self), f"Out of bounds: frame {key} >= {len(self)}"
        res = image_read(self.files[key], img_lib=self.img_lib)
        return res

    @overrides
    def __len__(self) -> int:
        return len(self.files)
