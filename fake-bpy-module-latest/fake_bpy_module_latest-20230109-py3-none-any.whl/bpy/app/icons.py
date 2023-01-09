import sys
import typing

GenericType = typing.TypeVar("GenericType")


def new_triangles(range: typing.Tuple, coords: typing.Sequence[bytes],
                  colors: typing.Sequence[bytes]) -> int:
    ''' Create a new icon from triangle geometry.

    :param range: Pair of ints.
    :type range: typing.Tuple
    :param coords: Sequence of bytes (6 floats for one triangle) for (X, Y) coordinates.
    :type coords: typing.Sequence[bytes]
    :param colors: Sequence of ints (12 for one triangles) for RGBA.
    :type colors: typing.Sequence[bytes]
    :rtype: int
    :return: Unique icon value (pass to interface ``icon_value`` argument).
    '''

    pass


def new_triangles_from_file(filename: str) -> int:
    ''' Create a new icon from triangle geometry.

    :param filename: File path.
    :type filename: str
    :rtype: int
    :return: Unique icon value (pass to interface ``icon_value`` argument).
    '''

    pass


def release(icon_id):
    ''' Release the icon.

    '''

    pass
