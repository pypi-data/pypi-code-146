#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .color_mode import color_mode
from .driver_options import driver_options
from .invert_background import invert_background
from .landscape import landscape
from .x_resolution import x_resolution
from .y_resolution import y_resolution
from .dpi import dpi
from .use_window_resolution import use_window_resolution
from .standard_resolution import standard_resolution
from .jpeg_hardcopy_quality import jpeg_hardcopy_quality
from .preview import preview
from .save_picture import save_picture
from .list_color_mode import list_color_mode
class picture(Group):
    """
    Enter the hardcopy/save-picture options menu.
    """

    fluent_name = "picture"

    child_names = \
        ['color_mode', 'driver_options', 'invert_background', 'landscape',
         'x_resolution', 'y_resolution', 'dpi', 'use_window_resolution',
         'standard_resolution', 'jpeg_hardcopy_quality']

    color_mode: color_mode = color_mode
    """
    color_mode child of picture.
    """
    driver_options: driver_options = driver_options
    """
    driver_options child of picture.
    """
    invert_background: invert_background = invert_background
    """
    invert_background child of picture.
    """
    landscape: landscape = landscape
    """
    landscape child of picture.
    """
    x_resolution: x_resolution = x_resolution
    """
    x_resolution child of picture.
    """
    y_resolution: y_resolution = y_resolution
    """
    y_resolution child of picture.
    """
    dpi: dpi = dpi
    """
    dpi child of picture.
    """
    use_window_resolution: use_window_resolution = use_window_resolution
    """
    use_window_resolution child of picture.
    """
    standard_resolution: standard_resolution = standard_resolution
    """
    standard_resolution child of picture.
    """
    jpeg_hardcopy_quality: jpeg_hardcopy_quality = jpeg_hardcopy_quality
    """
    jpeg_hardcopy_quality child of picture.
    """
    command_names = \
        ['preview', 'save_picture', 'list_color_mode']

    preview: preview = preview
    """
    preview command of picture.
    """
    save_picture: save_picture = save_picture
    """
    save_picture command of picture.
    """
    list_color_mode: list_color_mode = list_color_mode
    """
    list_color_mode command of picture.
    """
