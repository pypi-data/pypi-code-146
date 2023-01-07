from __future__ import annotations
from math import sqrt
from dataclasses import dataclass, fields
from typing import Any


@dataclass(frozen=True)
class RGB:
    r: int
    g: int
    b: int

    def __post_init__(self):
        for color in fields(self):
            value = getattr(self, color.name)
            if not isinstance(value, int):
                raise ValueError("All colors must be integer.")
            if value < 0 or value > 255:
                raise ValueError("RGB colors must be in range 0 - 255")

    def euclidean_distance(self, other: RGB) -> float:
        """
        Calculate the euclidean distance between the color and other color

        Args:
            other (RGB): RGB color of the format (int, int, int)

        Returns:
            float: Euclidean distance between the two colors
        """
        distance: float = 0.0
        for color in fields(self):
            value_self = getattr(self, color.name)
            value_other = getattr(other, color.name)
            distance += (value_self - value_other) ** 2
        return sqrt(distance)

    @staticmethod
    def validate_color(color: Any) -> None:
        if isinstance(color, str):
            color = color.replace("#", "")
            if len(color) != 6:
                raise ValueError("Format of color should be of type hex #FFFFFF")
        elif isinstance(color, tuple):
            if len(color) != 3:
                raise ValueError("Format of tuple should be (int, int, int)")
            for col in color:
                if not isinstance(col, int):
                    raise ValueError("Format of tuple should be (int, int, int)")
        else:
            raise ValueError(
                'Format of color should be either hex string, ie: "#FFFFFF" or RGB tuple, ie: (255, 255, 255)'
            )

    @staticmethod
    def color_hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
        """
        Helper function that converts a color in hex format '#FFFFFF' to RGB format (255,255,255)

        Args:
            hex_color (str): Color in hex format. ie:'#FFFFFF'

        Returns:
            tuple[int, int, int]: Color in RGB format. ie: (255,255,255)
        """
        hex_color = hex_color.replace("#", "")
        hex_color_list = [hex_color[:2], hex_color[2:4], hex_color[4:]]
        for color in hex_color_list:
            try:
                int(color, 16)
            except ValueError:
                raise ValueError("Each hex color value must be in range 00-FF")
        return tuple(map(lambda x: int(x, 16), hex_color_list))
