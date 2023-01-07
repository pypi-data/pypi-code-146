from pygame.color import Color
import glob
from pathlib import Path

import pygame
from pygame import Surface

from robingame.utils import limit_value


def init_display() -> Surface:
    if not pygame.display.get_init():
        pygame.display.init()
        return pygame.display.set_mode((1, 1))
    else:
        return pygame.display.get_surface()


def load_image(filename, colorkey=None) -> Surface:
    init_display()
    try:
        image = pygame.image.load(filename)
    except pygame.error:
        print("Unable to load image:", filename)
        raise

    # colorkey needs to be set before .convert_alpha() is called, because Surfaces with a
    # per-pixel transparency (i.e. after convert_alpha) ignore colorkey.
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

    image = image.convert_alpha()
    return image


def not_empty(surface: Surface) -> bool:
    """Check if a surface has any non-zero pixels. `Surface.get_bounding_rect()` returns the
    smallest rectangle on the surface containing data. If the surface is empty, it will return
    Rect(0, 0, 0, 0), for which `any` returns False"""
    return any(surface.get_bounding_rect())


def empty_image(*args, **kwargs) -> Surface:
    img = Surface(*args, **kwargs).convert_alpha()
    img.fill((0, 0, 0, 0))
    return img


def relative_folder(current_file: str, folder: str) -> Path:
    return Path(current_file).parent.absolute() / folder


def pad_alpha(colour_tuple):
    if len(colour_tuple) == 3:
        # if no alpha channel supplied, assume it's full opacity
        return (*colour_tuple, 255)
    elif len(colour_tuple) == 4:
        return colour_tuple
    else:
        raise Exception("bogus colour, man")


def brighten_color(color: Color, amount: int) -> Color:
    color = Color(color)
    r = limit_value(color.r + amount, between=(0, 255))
    g = limit_value(color.g + amount, between=(0, 255))
    b = limit_value(color.b + amount, between=(0, 255))
    return Color(r, g, b, color.a)


def brighten(image: Surface, amount: int):
    width, height = image.get_size()
    # surface.copy() inherits surface's colorkey; preserving transparency
    new_image = image.copy()

    # iterate over all the pixels in the old surface, and write a pixel to the new surface in the
    # corresponding position. If the colour of the present pixel has an entry in the
    # color_mapping dict, then write the new colour instead of the old one.
    for x in range(width):
        for y in range(height):
            color = image.get_at((x, y))[:]
            new_color = brighten_color(color, amount)
            if new_color:
                new_image.set_at((x, y), pygame.Color(*new_color))
            else:
                new_image.set_at((x, y), pygame.Color(*color))

    return new_image


def scale_image(image: Surface, scale: float):
    x_scale = image.get_rect().width * scale
    y_scale = image.get_rect().height * scale
    image = pygame.transform.scale(image, (x_scale, y_scale))
    return image


def scale_images(images: [Surface], scale: float) -> [Surface]:
    return [scale_image(image, scale) for image in images]


def flip_image(image: Surface, flip_x=False, flip_y=False):
    return pygame.transform.flip(image, bool(flip_x), bool(flip_y))


def flip_images(images: [Surface], flip_x=False, flip_y=False):
    return [flip_image(image, flip_x, flip_y) for image in images]


def recolor_image(surface: Surface, color_mapping: dict) -> [Surface]:

    # make sure the colourmap has alpha channel on all colours
    color_mapping = {pad_alpha(k): pad_alpha(v) for k, v in color_mapping.items()}
    width, height = surface.get_size()
    # surface.copy() inherits surface's colorkey; preserving transparency
    new_surface = surface.copy()

    # iterate over all the pixels in the old surface, and write a pixel to the new surface in the
    # corresponding position. If the colour of the present pixel has an entry in the
    # color_mapping dict, then write the new colour instead of the old one.
    for x in range(width):
        for y in range(height):
            color = surface.get_at((x, y))[:]
            new_color = color_mapping.get(color)
            if new_color:
                new_surface.set_at((x, y), pygame.Color(*new_color))
            else:
                new_surface.set_at((x, y), pygame.Color(*color))

    return new_surface


def recolor_images(images: [Surface], colormap: dict) -> [Surface]:
    return [recolor_image(image, colormap) for image in images]


def load_spritesheet(
    filename: Path | str,
    image_size: (int, int) = None,
    colorkey=None,
    num_images: int = 0,
) -> [Surface]:
    """Load the image file. Don't call this until pygame.display has been initiated. Split
    the spritesheet into images and return a list of images.

    If image_size is None, load the whole spritesheet as one sprite.
    """
    filename = Path(filename)
    if not filename.exists():
        raise FileNotFoundError(f"Couldn't find {filename}")
    sheet = load_image(filename.as_posix(), colorkey)

    if image_size:
        width, height = image_size
        num_horizontal = sheet.get_rect().width // width
        num_vertical = sheet.get_rect().height // height
        rects = [
            pygame.Rect((width * i, height * j, width, height))
            for j in range(num_vertical)
            for i in range(num_horizontal)
        ]
        images = [sheet.subsurface(rect) for rect in rects]
        images = list(filter(not_empty, images))
        if num_images:
            images = images[:num_images]
    else:
        images = [sheet]
    return images


def load_image_sequence(filename: Path | str, colorkey=None, num_images: int = 0) -> [Surface]:
    """Load a sequence of images."""
    filename = Path(filename)
    parent_folder = filename.parent
    pattern = filename.stem
    files = glob.glob(f"{parent_folder}/{pattern}*")
    if not files:
        raise FileNotFoundError(f"Couldn't find {filename}")
    images = [load_image(file, colorkey) for file in files]
    if num_images:
        images = images[:num_images]
    return images
