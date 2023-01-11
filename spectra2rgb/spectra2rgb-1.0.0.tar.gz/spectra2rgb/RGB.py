import numpy as np


class RGB:
    def __init__(self, red, green, blue):
        self.__red = red
        self.__green = green
        self.__blue = blue

    def __eq__(self, other):
        if isinstance(other, RGB):
            return self.__red == other.__red \
                and self.__green == other.__green \
                and self.__blue == self.__blue
        return False

    def __str__(self):
        return f'RGB(R={self.__red}, G={self.__green}, B={self.__blue})'

    def intensities(self, data, _slice):
        rgb_intensities = np.zeros(_slice.rgb_shape)
        rgb_intensities[_slice.at(0)] = self.__red * data
        rgb_intensities[_slice.at(1)] = self.__green * data
        rgb_intensities[_slice.at(2)] = self.__blue * data
        return rgb_intensities

    def to_hexcode(self):
        rgb_scaled = (int(self.__red * 255), int(self.__green * 255), int(self.__blue * 255))
        return ('#%02x%02x%02x' % rgb_scaled).upper()
