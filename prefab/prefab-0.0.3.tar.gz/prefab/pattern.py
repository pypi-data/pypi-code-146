"""Class for creating randomized patterns for training dataset.
"""

import numpy as np
import scipy
import scipy.fft  # pylint: disable=E0611

from prefab.processor import binarize_hard


class Pattern():
    """Class for creating randomized patterns for training dataset.
    """
    # pylint: disable=E1101
    def __init__(self, height, width, cutoff):
        self.height = height
        self.width = width
        self.cutoff = cutoff
        self.pattern = self.generate_pattern()

    def generate_pattern(self):
        """Generate randomized pattern.
        """
        self.pattern = np.random.uniform(low=0, high=1,
                                         size=(self.height, self.width))
        self._transform()
        self._reduce_transform()
        self._inv_transform()
        self.pattern = binarize_hard(self.pattern)
        return self.pattern

    def _transform(self):
        self.pattern = scipy.fft.fft2(self.pattern)
        self.pattern = scipy.fft.fftshift(self.pattern)

    def _reduce_transform(self):
        filter_margin_x = int((self.width-self.width*self.cutoff)/2)
        filter_margin_y = int((self.height-self.height*self.cutoff)/2)
        radius_x = range(filter_margin_x, self.width-filter_margin_x)
        radius_y = range(filter_margin_y, self.height-filter_margin_y)
        lp_filter = np.zeros_like(self.pattern)
        lp_filter[radius_y[0]:radius_y[-1], radius_x[0]:radius_x[-1]] = 1
        self.pattern *= lp_filter

    def _inv_transform(self):
        self.pattern = scipy.fft.ifftshift(self.pattern)
        self.pattern = scipy.fft.ifft2(self.pattern)
        self.pattern = self.pattern.real

    def scramble(self, slice_size):
        """Scramble the randomized pattern to create more sharps.
        """
        slices = np.lib.stride_tricks.sliding_window_view(self.pattern,
                                                          slice_size)
        slices = slices[::slice_size[0], ::slice_size[1]]
        slices = slices.reshape(-1, *slice_size)
        slices_rng = np.random.default_rng().permutation(slices, axis=0)

        pattern_rng = np.zeros_like(self.pattern)
        idx = 0
        y_range = range(0, self.pattern.shape[0]-slice_size[0]+1,
                        slice_size[0])
        x_range = range(0, self.pattern.shape[1]-slice_size[1]+1,
                        slice_size[1])
        for k in y_range:
            for j in x_range:
                pattern_rng[k:k+slice_size[0], j:j+slice_size[1]] = \
                    slices_rng[idx]
                idx += 1
        self.pattern = pattern_rng
