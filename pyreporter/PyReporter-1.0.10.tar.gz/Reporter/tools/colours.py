import enum


# Colour: Object for colours
class Colour():
    """
    A colour

    Attributes
    ----------
    name: :class:`str`
        The name of the colour

    hex: :class:`str`
        the hexadecimal number for the colour
    """
    def __init__(self, name: str, hex: str):
        self.name = name
        self.hex = hex


# ColourList: Enumeration of colours
class ColourList(enum.Enum):
    """
    Available colours to use
    """

    Red = Colour("red", "FF0000");
    """
    Red
    """

    DarkRed = Colour("dark-red", "8B0000")
    """
    Dark Red
    """

    LightRed = Colour("light-red", "F08080")
    """
    Light Red
    """

    Orange = Colour("orange", "FFC000")
    """
    Orange
    """

    DarkOrange = Colour("dark-orange", "FF8C00")
    """
    Dark Orange
    """

    LightOrange = Colour("light-orange", "FFD966")
    """
    Light Orange
    """

    Yellow = Colour("yellow", "FFFF00")
    """
    Yellow
    """

    LightYellow = Colour("light-yellow", "FFFFE0")
    """
    Light Yellow
    """

    DarkYellow = Colour("dark-yellow", "CC9900")
    """
    Dark Yellow
    """

    Green = Colour("green", "008000")
    """
    Green
    """

    DarkGreen = Colour("dark-green", "00B050")
    """
    Dark Green
    """

    LightGreen = Colour("light-green", "A9D08E")
    """
    Light Green
    """

    Blue = Colour("blue", "00B0F0")
    """
    Blue
    """

    LightBlue = Colour("light-blue", "BDD7EE")
    """
    Light Blue
    """

    DarkBlue = Colour("dark-blue", "4472C4")
    """
    Dark Blue
    """

    Purple = Colour("purple", "FF3399")
    """
    Purple
    """

    DarkPurple = Colour("dark-purple", "8B008B")
    """
    Dark Purple
    """

    LightPurple = Colour("light-purple", "FF99FF")
    """
    Light Purple
    """

    Grey = Colour("grey", "808080")
    """
    Grey
    """

    DarkGrey = Colour("dark-grey", "A9A9A9")
    """
    Dark Grey
    """

    LightGrey = Colour("light-grey", "D3D3D3")
    """
    Light Grey
    """

    Brown = Colour("brown", "A52A2A")
    """
    Brown
    """

    DarkBrown = Colour("dark-brown", "800000")
    """
    Dark Brown
    """

    LightBrown = Colour("light-brown", "CC6600")
    """
    Light Brown
    """

    RedOrange = Colour("red-orange", "FF6600")
    """
    Red Orange
    """

    DarkRedOrange = Colour("dark-red-orange", "B34700")
    """
    Dark Red Orange
    """

    LightRedOrange = Colour("light-red-orange", "FFB380")
    """
    Light Red Orange
    """

    YellowOrange = Colour("yellow-orange", "FFCC00")
    """
    Yellowish Orange
    """

    DarkYellowOrange = Colour("dark-yellow-orange", "CCA300")
    """
    Dark Yellowish Orange
    """

    LightYellowOrange = Colour("light-yellow-orange", "FFE066")
    """
    Light Yellowish Orange
    """

    Lime = Colour("lime", "CCFF33")
    """
    Lime
    """

    DarkLime = Colour("dark-lime", "66CC00")
    """
    Dark Lime
    """

    LightLime = Colour("light-lime", "BFFF80")
    """
    Light Lime
    """

    Turquoise = Colour("turquoise", "40E0D0")
    """
    Turquoise
    """

    DarkTurquoise = Colour("dark-turquoise", "00CED1")
    """
    Dark Turquoise
    """

    LightTurquoise = Colour("light-turquoise", "AFEEEE")
    """
    Light Turquoise
    """

    BluePurple = Colour("blue-purple", "6666FF")
    """
    Bluish Purple
    """

    DarkBluePurple = Colour("dark-blue-purple", "7300E6")
    """
    Dark Bluish Purple
    """

    LightBluePurple = Colour("light-blue-purple", "D9B3FF")
    """
    Light Bluish Purple
    """

    Pink = Colour("pink", "F8CBAD")
    """
    Pink
    """

    DarkPink = Colour("dark-pink", "FF1493")
    """
    Dark Pink
    """

    LightPink = Colour("light-pink", "FFB6C1")
    """
    Light Pink
    """

    White = Colour("white", "FFFFFF")
    """
    White
    """

    Black = Colour("black", "000000")
    """
    Black
    """
