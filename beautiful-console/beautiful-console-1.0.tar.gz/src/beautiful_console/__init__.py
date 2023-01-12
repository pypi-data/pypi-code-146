from .data import *
from .utils import *


@end_point
def beautiful_console(text, text_color=None, text_style=None, text_highlight_color=None, text_blink=False,
                            continuous_color=None, continuous_style=None, continuous_highlight_color=None, continuous_blink=False, 
                            text_color_degree=0, text_highlight_color_degree=0, continuous_color_degree=0, continuous_highlight_color_degree=0, 
                            get_input=False):
    beautiful_text = ""

    if text_color is not None:
        try:
            beautiful_text += f"{text_colors[text_color][text_color_degree]};"
        except KeyError:
            raise AttributeError("\"%s\" doesn't exist in defined colors." % text_color)
        except (IndexError, TypeError):
            raise AttributeError("Color degree can only be 0 or 1.")

    if text_style is not None:
        try:
            beautiful_text += f"{styles[text_style]};"
        except KeyError:
            raise AttributeError("\"%s\" doesn't exist in defined styles." % text_style)

    if text_highlight_color is not None:
        try:
            beautiful_text += f"{highlight_colors[text_highlight_color][text_highlight_color_degree]};"
        except KeyError:
            raise AttributeError("\"%s\" doesn't exist in defined highlight colors." % text_highlight_color)
        except (IndexError, TypeError):
            raise AttributeError("Highlight color degree can only be 0 or 1.")

    if text_blink is True:
        beautiful_text += f"{blink_code};"

    beautiful_text = beautiful_text[:len(beautiful_text) - 1]
    beautiful_text = f"\u001b[{beautiful_text}m{text}\u001b[0m"

    if get_input is True:
        continuous_text = ""

        if continuous_color is not None:
            try:
                continuous_text += f"{text_colors[continuous_color][continuous_color_degree]};"
            except KeyError:
                raise AttributeError("\"%s\" doesn't exist in defined colors." % continuous_color)
            except (IndexError, TypeError):
                raise AttributeError("Color degree can only be 0 or 1.")

        if continuous_style is not None:
            try:
                continuous_text += f"{styles[continuous_style]};"
            except KeyError:
                raise AttributeError("\"%s\" doesn't exist in defined styles." % continuous_style)

        if continuous_highlight_color is not None:
            try:
                continuous_text += f"{highlight_colors[continuous_highlight_color][continuous_highlight_color_degree]};"
            except KeyError:
                raise AttributeError("\"%s\" doesn't exist in defined highlight colors." % continuous_highlight_color)
            except (IndexError, TypeError):
                raise AttributeError("Highlight color degree can only be 0 or 1.")

        if continuous_blink is True:
            continuous_text += f"{blink_code};"

        continuous_text = continuous_text[:len(continuous_text) - 1]
        beautiful_text += f"\u001b[{continuous_text}m"

    return beautiful_text
