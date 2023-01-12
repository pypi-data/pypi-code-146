# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "10/05/2022"


from typing import Optional
from silx.utils.enum import Enum as _Enum
import numpy


class OverlapStichingStrategy(_Enum):
    MEAN = "mean"
    COSINUS_WEIGHTS = "cosinus weights"
    LINEAR_WEIGHTS = "linear weights"
    CLOSEST = "closest"


DEFAULT_OVERLAP_STRATEGY = OverlapStichingStrategy.COSINUS_WEIGHTS

DEFAULT_OVERLAP_HEIGHT = 400


class OverlapKernelBase:
    pass


class ZStichOverlapKernel(OverlapKernelBase):
    """
    class used to define overlap between two scans and create stitch between frames (`stitch` function)
    """

    def __init__(
        self,
        frame_width: int,
        stitching_strategy: OverlapStichingStrategy = DEFAULT_OVERLAP_STRATEGY,
        overlap_height: int = DEFAULT_OVERLAP_HEIGHT,
    ) -> None:
        """ """
        if not isinstance(overlap_height, int) or (overlap_height != -1 and not overlap_height > 0):
            raise TypeError(
                f"overlap_height is expected to be a positive int, {overlap_height} - not {overlap_height} ({type(overlap_height)})"
            )
        if not isinstance(frame_width, int) or not frame_width > 0:
            raise TypeError(
                f"frame_width is expected to be a positive int, {frame_width} - not {frame_width} ({type(frame_width)})"
            )

        self._overlap_height = overlap_height
        self._frame_width = frame_width
        self._stitching_strategy = OverlapStichingStrategy.from_value(stitching_strategy)
        self._weights_img_1 = None
        self._weights_img_2 = None

    @staticmethod
    def __check_img(img, name):
        if not isinstance(img, numpy.ndarray) and img.ndim == 2:
            raise ValueError(f"{name} is expected to be 2D numpy array")

    @property
    def overlap_height(self) -> int:
        return self._overlap_height

    @overlap_height.setter
    def overlap_height(self, height: int):
        if not isinstance(height, int):
            raise TypeError(f"height expects a int ({type(height)} provided instead)")
        if not height >= 0:
            raise ValueError(f"height is expected to be positive")
        self._overlap_height = height
        # update weights if needed
        if self._weights_img_1 is not None or self._weights_img_2 is not None:
            self.compute_weights()

    @property
    def img_2(self) -> numpy.ndarray:
        return self._img_2

    @property
    def weights_img_1(self) -> Optional[numpy.ndarray]:
        return self._weights_img_1

    @property
    def weights_img_2(self) -> Optional[numpy.ndarray]:
        return self._weights_img_2

    @property
    def stitching_strategy(self) -> OverlapStichingStrategy:
        return self._stitching_strategy

    def compute_weights(self):
        if self.stitching_strategy is OverlapStichingStrategy.MEAN:
            weights_img_1 = numpy.ones(self._overlap_height) * 0.5
            weights_img_2 = weights_img_1[::-1]
        elif self.stitching_strategy is OverlapStichingStrategy.CLOSEST:
            n_item = self._overlap_height // 2 + self._overlap_height % 2
            weights_img_1 = numpy.concatenate(
                [
                    numpy.ones(n_item),
                    numpy.zeros(self._overlap_height - n_item),
                ]
            )
            weights_img_2 = weights_img_1[::-1]
        elif self.stitching_strategy is OverlapStichingStrategy.LINEAR_WEIGHTS:
            weights_img_1 = numpy.linspace(1.0, 0.0, self._overlap_height)
            weights_img_2 = weights_img_1[::-1]
        elif self.stitching_strategy is OverlapStichingStrategy.COSINUS_WEIGHTS:
            angles = numpy.linspace(0.0, numpy.pi / 2.0, self._overlap_height)
            weights_img_1 = numpy.cos(angles) ** 2
            weights_img_2 = numpy.sin(angles) ** 2
        else:
            raise NotImplementedError(f"{self.stitching_strategy} not implemented")

        self._weights_img_1 = weights_img_1.reshape(-1, 1) * numpy.ones(self._frame_width).reshape(1, -1)
        self._weights_img_2 = weights_img_2.reshape(-1, 1) * numpy.ones(self._frame_width).reshape(1, -1)

    def stitch(self, img_1, img_2, check_input=True) -> tuple:
        """Compute overlap region from the defined strategy"""
        if check_input:
            self.__check_img(img_1, "img_1")
            self.__check_img(img_2, "img_2")

            if img_1.shape != img_2.shape:
                raise ValueError(
                    f"both images are expected to be of the same shape to apply stitch ({img_1.shape} vs {img_2.shape})"
                )

        if self.weights_img_1 is None or self.weights_img_2 is None:
            self.compute_weights()

        return (
            img_1 * self.weights_img_1 + img_2 * self.weights_img_2,
            self.weights_img_1,
            self.weights_img_2,
        )
