import cv2
import numpy as np


def px_to_int(pixel_value):
    """Takes a pixel string in the format '123px' and returns the int number.

    Parameters:
        pixel_value (str):
            The pixel value, written in the format '123px'.

    Returns:
        int:
            The number extracted from the pixel value.
    """
    if not pixel_value:
        return 0
    elif isinstance(pixel_value, str):
        pixel_value = int(pixel_value.strip("px"))
    else:
        pixel_value = int(pixel_value)
    return pixel_value


def make_white_image(height, width):
    """Generate a white background of appropriate height/width and return.

    This white background also has an alpha channel added for easier merging with
    other images with alpha channels.

    Parameters:
        height (int):
            The height of the image to generate, in pixels.
        width (int):
            The width of the image to generate, in pixels.

    Returns:
        ndarray:
            An opencv compatible representation of the white image.
    """
    white_background = np.zeros([height, width, 3], dtype=np.uint8)
    white_background.fill(255)
    b_channel, g_channel, r_channel = cv2.split(white_background)
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
    white_background = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    return white_background


def make_transparent_image(height, width):
    """Generate a transparent background of appropriate height/width and return.

    Parameters:
        height (int):
            The height of the image to generate, in pixels.
        width (int):
            The width of the image to generate, in pixels.

    Returns:
        ndarray:
            An opencv compatible representation of the transparent image.
    """
    transparent_background = np.zeros([height, width, 4], dtype=np.uint8)
    return transparent_background


def flatten(data):
    """Take a nested list and return a generator that will output each element, in order.

    Args:
        data (list):
            The list of nested lists.

    Returns:
        generator:
            A generator that will return each number in the flat list.
    """
    for entry in data:
        if isinstance(entry, list):
            yield from flatten(entry)
        else:
            yield entry
