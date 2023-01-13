import pythreejs as p3
from typing import Tuple


def value_to_string(val, precision: int = 3) -> str:
    """
    Convert a number to a human readable string.

    Parameters
    ----------
    val:
        The input number.
    precision:
        The number of decimal places to use for the string output.
    """
    if (not isinstance(val, float)) or (val == 0):
        text = str(val)
    elif (abs(val) >= 10.0**(precision+1)) or \
         (abs(val) <= 10.0**(-precision-1)):
        text = "{val:.{prec}e}".format(val=val, prec=precision)
    else:
        text = "{}".format(val)
        if len(text) > precision + 2 + (text[0] == '-'):
            text = "{val:.{prec}f}".format(val=val, prec=precision)
    return text


def make_sprite(string: str,
                position: Tuple[float, float, float],
                color: str = "black",
                size: float = 1.0) -> p3.Sprite:
    """
    Make a text-based sprite for axis tick.
    """
    sm = p3.SpriteMaterial(map=p3.TextTexture(string=string,
                                              color=color,
                                              size=60,
                                              squareTexture=False),
                           transparent=True)
    return p3.Sprite(material=sm, position=position, scale=[size, size, size])
