"""Utility functions for modifying color formats."""


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB to hex color format.

    :param r: Red value.
    :param g: Green value.
    :param b: Blue value.

    :return: Hex color format.
    """
    return f'#{r:X}{g:X}{b:X}'

def hex_to_rgb(hex: str) -> tuple:
    """Convert hex to RGB color format.

    :param hex: Hex color format.

    :return: RGB color format.
    """
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
