import pickle
from math import sqrt
from pathlib import Path
from typing import Optional

from colorise_terminal.rgb import RGB

# Escape sequence
esc = "\033["
# Reset all colors sequence
reset = esc + "0m"
# Text color
txt_color = esc + "38;5;{}m"
# Bold color text
bold_color = esc + "1;38;5;{}m"
# Bold text without color
bold_text = esc + "1m"
# Background color
background_color = esc + "48;5;{}m"

with open(Path(__file__).parent / "colors_dict.pkl", "rb") as f:
    colors_dictionary = pickle.load(f)


def cprint(
    *values: str,
    text_color: Optional[str | tuple[int, int, int]] = None,
    bg_color: Optional[str | tuple[int, int, int]] = None,
    bold: bool = False,
    sep: str = " ",
    end: str = "\n",
    file=None,
    flush: bool = False
) -> None:
    """
    Print the values to a stream, with the possibility of change the text color,
    the background color and text bold.

    Args:
        text_color (Optional[str  |  tuple[int, int, int]], optional):
            Color of the text to print, it could be in hex string format:'#FFFFFF' ;or in RGB tuple
            of int format: (255, 255, 255). Defaults to None.
        bg_color (Optional[str  |  tuple[int, int, int]], optional):
            Color of the text background, it could be in hex string format:'#FFFFFF' ;or in RGB tuple
            of int format: (255, 255, 255). Defaults to None.
        bold (bool, optional): Text in bold format. Defaults to False.
        sep (str, optional): String inserted between values. Defaults to " ".
        end (str, optional): String appended after the last value. Defaults to a newline.
        file (optional): A file-like object (stream). Defaults to the current sys.stdout.
        flush (bool, optional): Whether to forcibly flush the stream. Defaults to False.
    """
    # If user doesn't provide text color, bg color or bold, just use the default print function.
    if not text_color and not bg_color and not bold:
        print(*values, sep=sep, end=end, file=file, flush=flush)
        return

    background_color_int: Optional[int] = None
    text_color_int: Optional[int] = None

    if bg_color:
        RGB.validate_color(bg_color)
        if isinstance(bg_color, str):
            bg_color = RGB.color_hex_to_rgb(bg_color)
        background_color_int = _get_minor_distance_color(RGB(*bg_color), colors_dictionary)

    if text_color:
        RGB.validate_color(text_color)
        if isinstance(text_color, str):
            text_color = RGB.color_hex_to_rgb(text_color)
        text_color_int = _get_minor_distance_color(RGB(*text_color), colors_dictionary)

    print(
        bold_text if bold and not text_color else "",
        (bold_color if bold else txt_color).format(text_color_int) if text_color_int else "",
        background_color.format(background_color_int) if background_color_int else "",
        sep.join(values),
        reset,
        sep="",
        end=end,
        file=file,
        flush=flush,
    )


def _get_minor_distance_color(selected_color: RGB, colors_dict: dict[RGB, int]) -> int:
    """
    Returns the code of the closest color to that selected by the user

    Args:
        selected_color (tuple[int, int, int]): Color in RGB format. ie: (255, 255, 255)
        colors_dict (dict[str, int]): Map of color in RGB format and it's color code

    Returns:
        int: Code of the selected color
    """
    closest_color = 0
    minor_distance = float("+inf")
    for k, v in colors_dict.items():
        distance = selected_color.euclidean_distance(k)
        if distance < minor_distance:
            minor_distance = distance
            closest_color = v
    return closest_color


if __name__ == "__main__":
    cprint("Test", text_color="#FF0000")
