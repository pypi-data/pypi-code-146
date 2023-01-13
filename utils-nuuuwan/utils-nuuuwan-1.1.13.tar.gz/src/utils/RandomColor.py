import random

PRECISION = 2


class RandomColor:
    @staticmethod
    def _8bit():
        return random.randint(0, 255)

    @staticmethod
    def _360():
        return random.randint(0, 355)

    @staticmethod
    def _float():
        return random.random()

    @staticmethod
    def _percent():
        return random.randint(0, 100)

    @staticmethod
    def rgb(r=None, g=None, b=None, a=None):
        r = r if r else RandomColor._8bit()
        g = g if g else RandomColor._8bit()
        b = b if b else RandomColor._8bit()
        a = a if a else RandomColor._float()
        return f'rgba({r:d},{g:d},{b:d},{a:.2f})'

    @staticmethod
    def hsla(h=None, s=None, light=None, a=None):
        h = h if h else RandomColor._360()
        s = s if s else RandomColor._percent()
        light = light if light else RandomColor._percent()
        a = a if a else RandomColor._float()
        return f'hsla({h:d},{s:d}%,{light:d}%,{a:.2f})'
