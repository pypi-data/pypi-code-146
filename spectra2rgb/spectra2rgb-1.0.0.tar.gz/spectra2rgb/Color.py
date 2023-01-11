from spectra2rgb import RGB


class Color:
    VIOLET = 380
    RED = 750

    def __init__(self, wavelength):
        self.__wavelength = wavelength

    @property
    def rgb(self):
        red = 0
        green = 0
        blue = 0
        if Color.VIOLET <= self.__wavelength < 440:
            attenuation = 0.3 + 0.7 * (self.__wavelength - 380) / (440 - 380)
            red = ((-(self.__wavelength - 440) / (440 - 380)) * attenuation)
            green = 0.0
            blue = 1.0 * attenuation
        elif 440 <= self.__wavelength < 490:
            red = 0.0
            green = (self.__wavelength - 440) / (490 - 440)
            blue = 1.0
        elif 490 <= self.__wavelength <= 510:
            red = 0.0
            green = 1.0
            blue = -(self.__wavelength - 510) / (510 - 490)
        elif 510 <= self.__wavelength < 580:
            red = (self.__wavelength - 510) / (580 - 510)
            green = 1.0
            blue = 0.0
        elif 580 <= self.__wavelength < 645:
            red = 1.0
            green = -(self.__wavelength - 645) / (645 - 580)
            blue = 0.0
        elif 645 <= self.__wavelength <= Color.RED:
            attenuation = 0.3 + 0.7 * (750 - self.__wavelength) / (750 - 645)
            red = 1.0 * attenuation
            green = 0.0
            blue = 0.0
        return RGB(red, green, blue)

    @property
    def hexcode(self):
        return self.rgb.to_hexcode()

    def __eq__(self, other):
        if isinstance(other, Color):
            return self.__wavelength == other.__wavelength
        return False

    def __str__(self):
        return f'Color(λ={self.__wavelength}nm)'
