#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .draw_mesh import draw_mesh
from .filled import filled
from .marker import marker
from .marker_symbol import marker_symbol
from .marker_size import marker_size
from .wireframe import wireframe
from .color import color
class display_options(Group):
    """
    'display_options' child.
    """

    fluent_name = "display-options"

    child_names = \
        ['draw_mesh', 'filled', 'marker', 'marker_symbol', 'marker_size',
         'wireframe', 'color']

    draw_mesh: draw_mesh = draw_mesh
    """
    draw_mesh child of display_options.
    """
    filled: filled = filled
    """
    filled child of display_options.
    """
    marker: marker = marker
    """
    marker child of display_options.
    """
    marker_symbol: marker_symbol = marker_symbol
    """
    marker_symbol child of display_options.
    """
    marker_size: marker_size = marker_size
    """
    marker_size child of display_options.
    """
    wireframe: wireframe = wireframe
    """
    wireframe child of display_options.
    """
    color: color = color
    """
    color child of display_options.
    """
