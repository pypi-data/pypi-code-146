import random
import enum
from collections import namedtuple
from math import sin
from typing import TYPE_CHECKING, Tuple, Any

import numpy
import pygame
from pygame.surface import Surface


if TYPE_CHECKING:
    from robingame.objects.entity import Entity

Point = namedtuple("Point", ["x", "y"])


def touching(entity1: "Entity", entity2: "Entity") -> bool:
    """Determine whether entity1 is touching entity2. This function is directional by
    design---i.e. it checks whether
        (a) entity1.touchbox collides with entity2.rect
        it does *not* check whether
        (b) entity2.touchbox collides with entity1.rect.

    This is because in most cases the entities will have touchboxes with the same width
    buffer. If this is the case then (a) cannot be true without (b) also being true,
    and we needn't bother doing both calculations.

    Also, I want to allow for the possibility of unequal touchbox buffer widths; in
    this case, the order *will* matter. The entity with the larger touchbox buffer will
    "touch" the other entity, but not vice versa."""
    return entity1.touchbox.colliderect(entity2.rect)


def get_overlap_between_objects(obj1, obj2):
    """Get the x and y overlap between obj1 and obj2.rect"""
    x_overlap = min(obj1.rect.right, obj2.rect.right) - max(obj1.rect.left, obj2.rect.left)
    y_overlap = min(obj1.rect.bottom, obj2.rect.bottom) - max(obj1.rect.top, obj2.rect.top)
    return x_overlap, y_overlap


def un_overlap(movable_object, immovable_object):
    """Move movable_object outside boundaries of immovable_object."""
    x_overlap, y_overlap = get_overlap_between_objects(movable_object, immovable_object)
    if x_overlap > y_overlap:
        if movable_object.centroid.y >= immovable_object.centroid.y:
            movable_object.rect.top = immovable_object.rect.bottom
        else:
            movable_object.rect.bottom = immovable_object.rect.top
    else:
        if movable_object.centroid.x >= immovable_object.centroid.x:
            movable_object.rect.left = immovable_object.rect.right
        else:
            movable_object.rect.right = immovable_object.rect.left


# need these helper functions because pygame.mask.Mask methods aren't actually
# implemented as they are described in the docs...
def maskFromSurface(surface, threshold=127):
    # return pygame.mask.from_surface(surface, threshold)

    mask = pygame.mask.Mask(surface.get_size())
    key = surface.get_colorkey()
    if key:
        for y in range(surface.get_height()):
            for x in range(surface.get_width()):
                if surface.get_at((x, y)) != key:
                    mask.set_at((x, y), 1)
    else:
        for y in range(surface.get_height()):
            for x in range(surface.get_width()):
                if surface.get_at((x, y))[3] > threshold:
                    mask.set_at((x, y), 1)
    return mask


def mask_to_surface(mask, set_color=None):
    set_color = set_color if set_color else pygame.color.THECOLORS["magenta"]
    width, height = mask.get_size()
    surface = pygame.Surface((width, height)).convert_alpha()
    surface.fill((0, 0, 0, 0))
    for y in range(height):
        for x in range(width):
            if mask.get_at((x, y)):
                surface.set_at((x, y), set_color)
    return surface


def outline_image(surface: Surface):
    mask = maskFromSurface(surface)
    return mask.outline()


def ticks_to_frames(tick, ticks_per_frame):
    return tick // ticks_per_frame


def draw_arrow(surface, origin, angle_deg, color=None, length=50):
    """angle needs to be in degrees"""
    arrow_xy = arrow_coords(length, length // 10, length // 4)
    r = rotation_matrix(angle_deg)
    arrow_xy = arrow_xy.dot(r)
    arrow_xy += numpy.array(origin)
    pygame.draw.polygon(surface, color, arrow_xy, 2)


def draw_rect(surface, color, rect, width=0):
    # make a surface with exactly the same dimensions as the screen
    surface_with_alpha = pygame.Surface((surface.get_width(), surface.get_height())).convert_alpha()
    surface_with_alpha.fill((0, 0, 0, 0))
    # pygame.draw *does* respect alpha values when you're not plotting to screen
    pygame.draw.rect(surface_with_alpha, color, rect, width)
    # now blit the whole surface to the screen
    surface.blit(surface_with_alpha, (0, 0))

    # todo: now generalise this so that it can do pygame's other draw utils. Can i make a
    #  decorator for pygame's draw functions? Or a wrapper around the whole pygame.draw module?


def rotation_matrix(angle_deg):
    angle_rad = numpy.deg2rad(angle_deg)
    rotation_matrix = numpy.array(
        [
            (numpy.cos(angle_rad), -numpy.sin(angle_rad)),
            (numpy.sin(angle_rad), numpy.cos(angle_rad)),
        ]
    )
    return rotation_matrix


def arrow_coords(length, width, head_length):
    return numpy.array(
        [
            (0, 0),
            (length, 0),
            (length - head_length, width),
            (length - head_length, -width),
            (length, 0),
        ]
    )


def count_edges(values):
    rising_edges = 0
    falling_edges = 0
    for ii, value in enumerate(values):
        if ii == 0:
            previous_value = value
        if value and not previous_value:
            rising_edges += 1
        if not value and previous_value:
            falling_edges += 1
        previous_value = value
    return rising_edges, falling_edges


def pulsing_value(tick, min, max, freq, func=None):
    func = func if func else sin
    A = (max - min) / 2
    B = (max + min) / 2
    return A * func(tick * freq) + B


def mouse_hovering_over(element):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return element.rect.collidepoint(mouse_x, mouse_y)


class MyEnumMeta(enum.EnumMeta):
    """
    Incredibly, enum.Enum does not have a __contains__ method, so we can't do stuff like:
    class Colours(Enum):
        ...
    assert "red" in Colours
    """

    def __contains__(cls, member):
        return any(x.value == member for x in cls)


class Enum(enum.Enum, metaclass=MyEnumMeta):
    pass


def circle_surf(radius, color):
    radius = int(radius)
    surf = Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf


def random_float(min, max):
    assert min < max
    spread = max - min
    value = min + random.random() * spread
    return value


def random_int(min, max):
    return random.randint(min, max)


def limit_value(value, between: Tuple[Any, Any]):
    _min, _max = between
    return max(_min, min(value, _max))


def unzip(zipped):
    return tuple(zip(*zipped))


Coord = tuple[int, int]


class SparseMatrix(dict):
    """
    Dictionary of the form {(x, y): value}. Can be used to simulate an infinite grid.
    Each entry represents a cell with width and height of 1 (i.e. NOT a dimensionless point)
    """

    Limit = tuple[int, int] | tuple[None, None]

    @property
    def limits(self) -> tuple[Limit, Limit]:
        """The min and max x/y coords of all entries"""
        if self:
            xs, ys = unzip(self.keys())
            xlim = min(xs), max(xs)
            ylim = min(ys), max(ys)
        else:
            xlim = ylim = None, None
        return xlim, ylim

    @property
    def size(self) -> (int, int):
        if self:
            xlim, ylim = self.limits
            width = xlim[1] - xlim[0] + 1
            height = ylim[1] - ylim[0] + 1
        else:
            width = height = 0
        return width, height

    @property
    def xlim(self) -> Limit:
        xlim, _ = self.limits
        return xlim

    @property
    def ylim(self) -> Limit:
        _, ylim = self.limits
        return ylim

    @property
    def width(self) -> int:
        width, _ = self.size
        return width

    @property
    def height(self) -> int:
        _, height = self.size
        return height

    def copy(self) -> "SparseMatrix":
        return SparseMatrix(super().copy())

    def scale_to_screen(self, screen_size: (int, int)) -> (float, int, int):
        """
        Calculate the scaling factor and x/y offset required to blit a group of pixels
        representing self onto a screen
        """
        screen_width, screen_height = screen_size
        self_width, self_height = self.size
        xlim, ylim = self.limits
        x_scaling = screen_width // self_width
        y_scaling = screen_height // self_height
        scaling = max(1, min(x_scaling, y_scaling))

        x_offset = screen_width // 2 - (xlim[0] + self_width // 2) * scaling
        y_offset = screen_height // 2 - (ylim[0] + self_height // 2) * scaling
        return scaling, x_offset, y_offset

    def screen_coords(self, xy, scaling, x_offset, y_offset) -> tuple[int, int]:
        """
        Convert col/row number (xy) into screen coordinates (in pixels)
        """
        x, y = xy
        screen_x = x_offset + x * scaling
        screen_y = y_offset + y * scaling
        return screen_x, screen_y


def draw_text(s: str, surface: Surface, position, font, color, antialias=False):
    text_bitmap = font.render(s, antialias, color)
    surface.blit(text_bitmap, position)
