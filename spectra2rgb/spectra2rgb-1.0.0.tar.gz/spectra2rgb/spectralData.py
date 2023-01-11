from spectra2rgb import Colors
from spectra2rgb import Slice


class SpectralData:
    def __init__(self, array, axis, inverse=False):
        self.__array = array
        self.__colors = Colors(array.shape[axis], inverse)
        self.__slice = Slice(array.shape, axis)

    def to_rgb(self):
        return self.__colors.rgb_intensities(self.__array, self.__slice)

    @property
    def colors(self):
        return self.__colors
